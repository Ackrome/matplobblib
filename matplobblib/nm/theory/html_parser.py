import os
import re
import shutil
import copy
from bs4 import BeautifulSoup, Tag, NavigableString
from urllib.parse import urlparse
from pathlib import Path

def sanitize_filename(name: str, default_name_prefix: str = "section", max_length: int = 50) -> str:
    """
    Очищает строку для использования в качестве имени файла.
    Удаляет недопустимые символы и заменяет пробелы на подчеркивания.
    """
    if not name:
        name = default_name_prefix
    
    # Удаляем символы, которые могут вызвать проблемы в именах файлов
    name = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', name)
    # Заменяем пробелы и некоторые другие символы на одно подчеркивание
    name = re.sub(r'[\s./\\]+', '_', name)
    # Удаляем ведущие/завершающие подчеркивания
    name = name.strip('_')

    if not name: # Если имя стало пустым после очистки
        name = default_name_prefix

    # Обрезаем до максимальной длины
    final_name = name[:max_length].rstrip('_')
    if not final_name: # Если и после обрезки пусто
        return default_name_prefix
    return final_name

def save_h1_sections_for_browser_view(html_file_path: str, output_directory: str):
    """
    Читает HTML-файл, находит все заголовки H1 и сохраняет каждую секцию
    (H1 + последующий контент до следующего H1) как отдельный HTML-файл
    в указанную папку вывода. Пути к изображениям корректируются.

    :param html_file_path: Строка с путем к исходному HTML-файлу.
    :param output_directory: Строка с путем к папке, куда будут сохранены HTML-фрагменты.
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{html_file_path}' не найден.")
        return
    except Exception as e:
        print(f"Ошибка при чтении файла '{html_file_path}': {e}")
        return

    # Очистка или создание папки для вывода
    if os.path.exists(output_directory):
        try:
            shutil.rmtree(output_directory) # Удаляем папку со всем содержимым
            print(f"Папка '{output_directory}' очищена.")
        except Exception as e:
            print(f"Ошибка при удалении папки '{output_directory}': {e}")
            return
    try:
        os.makedirs(output_directory)
        print(f"Создана папка для вывода: '{output_directory}'")
    except Exception as e:
        print(f"Ошибка при создании папки '{output_directory}': {e}")
        return

    soup = BeautifulSoup(html_content, 'lxml') # или 'html.parser'
    h1_tags = soup.find_all('h1')

    if not h1_tags:
        print(f"В HTML-документе '{html_file_path}' не найдены заголовки первого уровня (<h1>).")
        return
    
    saved_sections_content = []
    print(f"\nСохранение секций из '{html_file_path}' в папку '{output_directory}':\n")
    source_html_directory = os.path.dirname(os.path.abspath(html_file_path))
    
    for i, current_h1_tag in enumerate(h1_tags):
        current_h1_text = current_h1_tag.get_text(strip=True)
        
        base_filename_segment = sanitize_filename(current_h1_text, default_name_prefix=f"section_h1")
        target_filename = f"{base_filename_segment}_{i+1}.html"
        target_filepath = os.path.join(output_directory, target_filename)

        section_elements = []
        sibling_element = current_h1_tag
        while sibling_element:
            if isinstance(sibling_element, Tag) and sibling_element.name == 'h1' and sibling_element != current_h1_tag:
                break
            section_elements.append(sibling_element)
            sibling_element = sibling_element.next_sibling

        # Временный контейнер для сборки HTML-кода секции с модификациями
        snippet_container = BeautifulSoup('<div></div>', 'lxml').div

        for original_element in section_elements:
            copied_element = copy.deepcopy(original_element) # Глубокое копирование для безопасного изменения

            if isinstance(copied_element, Tag): # Обрабатываем теги (NavigableString не содержит вложенных тегов)
                for image_tag in copied_element.find_all('img', recursive=True):
                    image_source_attribute = image_tag.get('src')
                    if image_source_attribute:
                        parsed_image_source = urlparse(image_source_attribute)
                        # Обрабатываем только локальные пути, не являющиеся data URI или внешними URL
                        if parsed_image_source.scheme.lower() not in ['data', 'http', 'https', 'ftp', 'file']:
                            # src - это локальный путь (относительный или абсолютный)
                            if os.path.isabs(image_source_attribute):
                                # Уже абсолютный путь файловой системы
                                absolute_image_path = os.path.normpath(image_source_attribute)
                            else:
                                # Относительный путь, разрешаем относительно директории исходного HTML
                                absolute_image_path = os.path.normpath(os.path.join(source_html_directory, image_source_attribute))
                            
                            # Убеждаемся, что путь стал абсолютным после нормализации
                            absolute_image_path = os.path.abspath(absolute_image_path)
                            image_tag['src'] = Path(absolute_image_path).as_uri() # Преобразуем в file:/// URI
            
            snippet_container.append(copied_element)
        
        current_section_body_html = snippet_container.decode_contents() # Получаем HTML из контейнера

        # Формируем полную HTML-страницу для фрагмента
        page_title_text = current_h1_text if current_h1_text else f'Секция {i+1}'
        final_html_output = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title_text}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 20px; line-height: 1.6; color: #333; }}
        h1 {{ color: #111; border-bottom: 2px solid #eee; padding-bottom: 0.3em; margin-top: 0; }}
        img {{ max-width: 100%; height: auto; display: block; margin: 1em 0; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        p {{ margin: 1em 0; }}
        div, section, article {{ margin-bottom: 1em; }}
        /* Вы можете добавить сюда больше стилей или ссылку на CSS из оригинального документа, если это необходимо */
    </style>
</head>
<body>
{current_section_body_html}
</body>
</html>"""

        try:
            with open(target_filepath, 'w', encoding='utf-8') as output_file_stream:
                output_file_stream.write(final_html_output)
            print(f"Сохранена секция: '{target_filepath}' (Заголовок: {current_h1_text if current_h1_text else 'Без заголовка'})")
        
            saved_sections_content.append(final_html_output)
        except Exception as e:
            print(f"Ошибка при сохранении файла '{target_filepath}': {e}")
    
    print(f"\nГотово. HTML-фрагменты сохранены в '{output_directory}'. Откройте их в браузере для просмотра.")
    
    with open(os.path.join(output_dir,'index.html'), 'w', encoding='utf-8') as output_file_stream:
        output_file_stream.write(html_content)
    
    return saved_sections_content

html_path = r"C:\Users\ivant\Desktop\proj\matplobblib\htmls\NM\index.html" # путь
output_dir = r"C:\Users\ivant\Desktop\proj\matplobblib\matplobblib\nm\theory\htmls" # папка вывода

outputs = save_h1_sections_for_browser_view(html_path, output_dir)

