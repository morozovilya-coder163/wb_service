import pdfplumber
from PIL import Image
import pyzbar.pyzbar as pyzbar
from pylibdmtx.pylibdmtx import decode
import re
from .work_with_exel import ExelData
import concurrent.futures
import tempfile
import os
import traceback

class PageData:
    def __init__(self, articul, size, barcodes):
        self.articul = articul
        self.size = size
        self.barcodes = barcodes

class FullInfo(PageData, ExelData):
    def __init__(self, articul, size, barcodes, brend, name_atribut, chrt_id, color, barcode):
        PageData.__init__(self, articul, size, barcodes)
        ExelData.__init__(self, brend, name_atribut, chrt_id, color, barcode)   

def extract_text_and_barcodes_from_pdf(pdf_path, dpi=135):
    articul = 0
    size = 0
    barcodes = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, 1):
            if page_number == 1:
                # Получаем текст со страницы
                text = page.extract_text()
                match_articule = re.search(r'Артикул (\d+)', text)
                if match_articule:
                    articul = int(match_articule.group(1))
                match_size = re.search(r'РАЗМЕР\s*(\d{1,2})', text, re.MULTILINE)
                if match_size:
                    size_str = match_size.group()
                    match = re.search(r'РАЗМЕР\s*\n\s*(\d+)', size_str)
                    size = int(match.group(1))


            # Генерируем изображение страницы
            image = page.to_image(resolution=dpi).original

            # Декодируем DataMatrix коды с изображения
            decoded_objects = decode(image)

            barcodes.extend((obj.data.decode('utf-8') for obj in decoded_objects))
            
    page_data = PageData(articul, size, barcodes)
    return page_data
