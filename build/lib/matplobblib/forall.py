import numpy as np
from  inspect import getsource
####################################################################################
# rrstr (Округление до n знаков)
####################################################################################
def one_rrstr(x,n=0): # округление до n знаков после запятой
    if n == 0:
        return str(x)
    fmt = '{:.'+str(n)+'f}'
    return fmt.format(x).replace('.',',')

def rrstr(x,n):
    rrstr1 = np.vectorize(one_rrstr)
    res = rrstr1(x,n)
    if res.size ==1:
        return str(res)
    return res
####################################################################################
# show_img показывает фотографию в ячейке вывода
####################################################################################
def show_img(filename):
    from IPython.display import display, Image
    try:
        img = Image(filename=filename)
        display(img)
    except:
        print('Неправильное имя файла')
    return filename
####################################################################################
# show_images показывает несколько фотографий 
# в ячейке вывода по названиям в итерируемом аргументе  
####################################################################################
def show_images(filenames):
    return np.vectorize(show_img)(filenames)
####################################################################################
# save_pdf_as_images (Сохраняет каждую страничку pdf как png файл)
####################################################################################    
def save_pdf_as_images(pdf_path, output_folder = None, dpi=100):
    from pdf2image import convert_from_path
    import os
    
    if output_folder == None:
        output_folder = pdf_path[:-4]
        
    outpaths = []
    # Создаем папку для сохранения, если её нет
    os.makedirs(output_folder, exist_ok=True)

    # Конвертируем PDF в список изображений
    pages = convert_from_path(pdf_path, dpi=dpi)

    # Сохраняем каждую страницу как изображение
    for page_number, page in enumerate(pages, start=1):
        output_path = os.path.join(output_folder, f"page_{page_number}.png")
        page.save(output_path, "PNG")
        print(f"Страница {page_number} сохранена как {output_path}")
        outpaths.append(output_path)
    return outpaths
####################################################################################