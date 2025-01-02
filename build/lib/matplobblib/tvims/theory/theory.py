import os

# Получаем текущую директорию, где запущена программа
current_directory = os.getcwd()

# Список всех файлов и папок в текущей директории
all_items = os.listdir(current_directory)

# Фильтруем только файлы
files = [item for item in all_items if os.path.isfile(os.path.join(current_directory, item))]

# Выводим названия файлов
print("Файлы в директории:")
for file in files:
    #if 'ТЕОР' in file.upper():
        print(file)