import os

import requests

from ..forall import get_task_from_func, getsource, getsource_no_docstring, invert_dict


PROXYAPI_BASE_URL = "https://api.proxyapi.ru/openai/v1"
DEFAULT_MODEL = "gpt-5-mini"


def call_model(
    prompt,
    api_key=None,
    model=DEFAULT_MODEL,
    system=None,
    temperature=None,
    max_output_tokens=None,
    timeout=60,
    base_url=PROXYAPI_BASE_URL,
    return_json=False,
    **kwargs
):
    """
    Вызов ProxyAPI для OpenAI-совместимой языковой модели и возврат сгенерированного текста.

    Функция по умолчанию обращается к OpenAI-совместимому эндпоинту Responses API:
    https://api.proxyapi.ru/openai/v1/responses. Ключ ProxyAPI можно передать
    напрямую через api_key или сохранить в переменной окружения PROXYAPI_API_KEY
    либо PROXYAPI_KEY.

    Параметры
    ----------
    prompt : str or list
        Строка пользовательского запроса или структура input, совместимая с Responses API.
    api_key : str, optional
        Ключ ProxyAPI. Если не указан, берется из PROXYAPI_API_KEY или PROXYAPI_KEY.
    model : str, optional
        Название модели для запроса к ProxyAPI. По умолчанию "gpt-5-mini".
    system : str, optional
        Системная инструкция, передаваемая в поле instructions Responses API.
    temperature : float, optional
        Температура генерации. Если None, параметр не отправляется.
    max_output_tokens : int, optional
        Максимальное количество токенов ответа. Если None, параметр не отправляется.
    timeout : int or float, optional
        Таймаут HTTP-запроса в секундах.
    base_url : str, optional
        Базовый OpenAI-совместимый URL ProxyAPI.
    return_json : bool, optional
        Если True, возвращает исходный JSON-ответ вместо извлеченного текста.
    **kwargs
        Дополнительные параметры Responses API.

    Возвращает
    -------
    str or dict
        Текст ответа модели или исходный JSON при return_json=True.

    Исключения
    ------
    ValueError
        Если ключ ProxyAPI не передан и не найден в переменных окружения.
    RuntimeError
        Если ProxyAPI вернул HTTP-ошибку или ответ без текста.
    """
    if api_key is None:
        api_key = os.environ.get("PROXYAPI_API_KEY") or os.environ.get("PROXYAPI_KEY")

    if not api_key:
        raise ValueError("Нужен ключ ProxyAPI. Передайте api_key или задайте PROXYAPI_API_KEY.")

    payload = {
        "model": model,
        "input": prompt,
    }

    if system is not None:
        payload["instructions"] = system
    if temperature is not None:
        payload["temperature"] = temperature
    if max_output_tokens is not None:
        payload["max_output_tokens"] = max_output_tokens

    for key, value in kwargs.items():
        if value is not None:
            payload[key] = value

    response = requests.post(
        base_url.rstrip("/") + "/responses",
        headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )

    try:
        data = response.json()
    except ValueError:
        data = {"error": response.text}

    if not response.ok:
        error = data.get("error") if isinstance(data, dict) else None
        if isinstance(error, dict):
            message = error.get("message") or str(error)
        elif error:
            message = str(error)
        else:
            message = response.text
        raise RuntimeError("Запрос к ProxyAPI завершился со статусом {}: {}".format(response.status_code, message))

    if return_json:
        return data

    if isinstance(data, dict):
        output_text = data.get("output_text")
        if output_text:
            return output_text

        parts = []
        for item in data.get("output", []):
            if not isinstance(item, dict):
                continue
            for content in item.get("content", []):
                if isinstance(content, dict) and content.get("text"):
                    parts.append(content["text"])

        if parts:
            return "\n".join(parts)

    raise RuntimeError("Ответ ProxyAPI не содержит текст. Используйте return_json=True для просмотра JSON.")


NLP = [call_model]

files_dict = {
    "Вызовы языковых моделей": NLP,
}

names = list(files_dict.keys())
modules = list(files_dict.values())

funcs_dicts = [dict([(get_task_from_func(i), i) for i in module]) for module in modules]
funcs_dicts_ts = [dict([(get_task_from_func(i, True), i) for i in module]) for module in modules]
funcs_dicts_full = [dict([(i.__name__, getsource(i)) for i in module]) for module in modules]
funcs_dicts_full_nd = [dict([(i.__name__, getsource_no_docstring(i)) for i in module]) for module in modules]

themes_list_funcs = dict([(names[i], list(funcs_dicts[i].values())) for i in range(len(names))])
themes_list_dicts = dict([(names[i], funcs_dicts[i]) for i in range(len(names))])
themes_list_dicts_full = dict([(names[i], funcs_dicts_full[i]) for i in range(len(names))])
themes_list_dicts_full_nd = dict([(names[i], funcs_dicts_full_nd[i]) for i in range(len(names))])


def description(
    dict_to_show=themes_list_funcs,
    key=None,
    show_only_keys: bool = False,
    show_keys_second_level: bool = True,
    n_symbols: int = 32,
    to_print: bool = True,
    show_doc=False
):
    """
    Отображает информацию о доступных функциях и темах в модуле NLP.

    Функция повторяет интерфейс description() из модуля NM:
    можно показать все темы, функции внутри одной темы или исходный код
    выбранной функции.

    Параметры
    ----------
    dict_to_show : str or dict, optional
        Словарь для отображения или название темы. По умолчанию themes_list_funcs.
    key : hashable, optional
        Имя функции для фильтрации, например "call_model".
    show_only_keys : bool, optional
        Если True, показывает только названия тем.
    show_keys_second_level : bool, optional
        Если True, показывает имена функций внутри тем.
    n_symbols : int, optional
        Максимальное количество символов описания для вывода.
    to_print : bool, optional
        Если True, печатает результат. Иначе возвращает строку.
    show_doc : bool, optional
        Если True и key задан, выводит исходный код функции с docstring.

    Возвращает
    -------
    str or None
        Форматированный текст при to_print=False, иначе None.
    """
    if type(dict_to_show) == str and key is None:
        dict_to_show = themes_list_dicts[dict_to_show]
        dict_to_show = invert_dict(dict_to_show)
        text = ""
        length1 = 1 + max([len(x.__name__) for x in list(dict_to_show.keys())])

        for key in dict_to_show.keys():
            text += f"{key.__name__:<{length1}}"

            if not show_only_keys:
                text += ": "
                text += f"{dict_to_show[key]};\n" + " " * (length1 + 2)
            text += "\n"

        if to_print:
            return print(text)
        return text

    elif type(dict_to_show) == str and key in themes_list_dicts_full[dict_to_show].keys():
        if show_doc:
            return print(themes_list_dicts_full[dict_to_show][key])
        return print(themes_list_dicts_full_nd[dict_to_show][key])

    text = ""
    length1 = 1 + max([len(x) for x in list(dict_to_show.keys())])

    for key in dict_to_show.keys():
        text += f"{key:^{length1}}"
        if not show_only_keys:
            text += ": "
            for f in dict_to_show[key]:
                text += f"{f.__name__}"
                if show_keys_second_level:
                    text += ": "
                    try:
                        func_text = invert_dict(themes_list_dicts[key])[f]
                        func_text_len = len(func_text)
                        if func_text_len < n_symbols:
                            text += func_text.replace("\n", "\n" + " " * (length1 + len(f.__name__)))
                        else:
                            text += func_text[:n_symbols].replace(
                                "\n",
                                "\n" + " " * (length1 + len(f.__name__))
                            ) + "..."
                    except:
                        pass
                text += ";\n" + " " * (length1 + 2)
        text += "\n"

    if to_print:
        return print(text)
    return text


__all__ = ["call_model", "description", "NLP"]
