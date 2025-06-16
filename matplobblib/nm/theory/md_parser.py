import argparse
import os
import re

def generate_base_filename(heading_text, unique_id, find_num = True):
    """
    Генерирует безопасное базовое имя файла из текста заголовка.
    heading_text: Текст строки заголовка (например, "# Мой Заголовок").
    unique_id: Счетчик для генерации уникальных имен типа "section_X", если заголовок пуст или становится пустым.
    Возвращает: Строку с базовым именем файла (без расширения).
    """
    # Удаляем ведущие '#' и пробелы
    text = heading_text.lstrip('# ').strip()

    # Если текст заголовка пуст (например, строка была только "# ")
    if not text:
        return f"section_{unique_id}"

    # Заменяем пробелы на подчеркивания
    text = text.replace(' ', '_')

    # Удаляем символы, не подходящие для имен файлов (оставляем буквы, цифры, _, ., -)
    text = re.sub(r'[^\w_.-]', '', text)

    # Схлопываем множественные подчеркивания в одно
    text = re.sub(r'_+', '_', text)

    # Удаляем ведущие/завершающие символы _, ., -
    text = re.sub(r'^[_.-]+|[_.-]+$', '', text)

    # Если имя файла стало пустым или состоит только из точки после очистки
    if not text or text == '.':
        return f"section_{unique_id}"

    if find_num:
        text = text.split('.')
        
        return text[0], '.'.join(text[1:])
    
    return text

def split_markdown_by_h1(input_filepath, output_dir="."):
    """
    Разделяет Markdown-файл на части по заголовкам первого уровня (H1).
    """
    others_list = []
    if not os.path.isfile(input_filepath):
        print(f"Ошибка: Файл '{input_filepath}' не найден или не является файлом.")
        return

    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Создана директория: '{output_dir}'")
        elif not os.path.isdir(output_dir):
            print(f"Ошибка: Путь вывода '{output_dir}' существует, но не является директорией.")
            return
    except OSError as e:
        print(f"Ошибка при создании/проверке директории вывода '{output_dir}': {e}")
        return

    try:
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
    except IOError as e:
        print(f"Ошибка чтения файла '{input_filepath}': {e}")
        return

    current_h1_content = []
    current_h1_title_line = None  # Хранит полную строку H1 для генерации имени файла
    files_written_count = 0       # Счетчик для уникальных имен файлов (section_X)

    for line in lines:
        stripped_line = line.strip()
        # Заголовок H1: начинается с "# " и не является H2, H3 и т.д.
        is_h1 = stripped_line.startswith("# ") and not stripped_line.startswith("##")

        if is_h1:
            if current_h1_title_line and current_h1_content:
                files_written_count += 1
                num, others = generate_base_filename(current_h1_title_line, files_written_count,find_num=True)
                others_list.append(others)
                
                filename_candidate = num + ".md"
                output_path = os.path.join(output_dir, filename_candidate)
                
                # Обработка коллизий имен файлов
                collision_count = 1
                temp_filename_base = num
                while os.path.exists(output_path):
                    collision_count += 1
                    filename_candidate = f"{num}_{collision_count}.md"
                    output_path = os.path.join(output_dir, filename_candidate)
                
                try:
                    with open(output_path, 'w', encoding='utf-8') as outfile:
                        outfile.writelines(current_h1_content)
                    print(f"Создан файл: '{output_path}'")
                except IOError as e:
                    print(f"Ошибка записи файла '{output_path}': {e}")
                
                

            current_h1_title_line = stripped_line
            current_h1_content = [line]  # Начинаем новый раздел с H1
        elif current_h1_title_line is not None: # Если мы уже внутри раздела H1
            current_h1_content.append(line)

    # Запись последнего собранного раздела
    if current_h1_title_line and current_h1_content:
        files_written_count += 1
        num, others = generate_base_filename(current_h1_title_line, files_written_count,find_num=True)
        
        filename_candidate = num + ".md"
        output_path = os.path.join(output_dir, filename_candidate)

        collision_count = 1
        temp_filename_base = num
        while os.path.exists(output_path):
            collision_count += 1
            filename_candidate = f"{temp_filename_base}_{collision_count}.md"
            output_path = os.path.join(output_dir, filename_candidate)
            
        try:
            with open(output_path, 'w', encoding='utf-8') as outfile:
                outfile.writelines(current_h1_content)
            print(f"Создан файл: '{output_path}'")
        except IOError as e:
            print(f"Ошибка записи файла '{output_path}': {e}")
        
        others_list.append(others)


    if files_written_count == 0:
        if lines: # Файл не пуст, но H1 не найдены
            print(f"В файле '{input_filepath}' не найдено заголовков первого уровня ('# Заголовок'). Файлы не созданы.")
        else: # Исходный файл пуст
            print(f"Файл '{input_filepath}' пуст. Файлы не созданы.")
    else:
        
        try:
            with open(os.path.join(output_dir, 'h1_names.md'), 'w', encoding='utf-8') as outfile:
                    outfile.writelines('|||||'.join(others_list))
            print(f"Создан файл: '{output_path}'")
        except Exception as e:
            print(e)




def main():
    parser = argparse.ArgumentParser(
        description="Разделяет Markdown файл на части по заголовкам первого уровня (H1).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input_file", help="Путь к исходному Markdown файлу.")
    parser.add_argument("-o", "--output_dir", default=".", help="Директория для сохранения разделенных файлов (по умолчанию: текущая директория).\nЕсли директория не существует, она будет создана.")
    args = parser.parse_args()
    split_markdown_by_h1(args.input_file, args.output_dir)



if __name__ == "__main__":
    # main()
    split_markdown_by_h1(r"C:\Users\ivant\Downloads\ЧМ_ТЕОР.md",r"C:\Users\ivant\Desktop\proj\matplobblib\matplobblib\nm\theory\ipynbs")