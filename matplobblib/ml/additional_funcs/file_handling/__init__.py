import fitz 
import os


def pdf_to_png(pdf_path, dpi=110):
    # Создаем выходную папку, если не существует
    output_folder = ''.join(pdf_path.split('.')[:-1])
    os.makedirs(output_folder, exist_ok=True)
    
    # Открываем PDF-документ
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # Получаем изображение страницы с заданным DPI
        pix = page.get_pixmap(dpi=dpi)
        # Сохраняем в формате PNG
        output_path = os.path.join(output_folder, f"page_{page_num+1}.png")
        pix.save(output_path)
        
        #display(Image.open(output_path))
    
    doc.close()

FH = [pdf_to_png]