from pylibdmtx.pylibdmtx import encode
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def generate_datamatrix(data):
    """Генерация DataMatrix кода."""
    encoded = encode(data.encode('utf-8'), scheme='ascii')
    image = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

def generate_barcode(data):
    """Генерация баркода."""
    barcode = Code128(data, writer=ImageWriter())
    buffer = io.BytesIO()
    barcode.write(buffer)
    buffer.seek(0)
    return buffer

def create_pdf_with_codes(barcode_data, datamatrix_codes, text1, text2):
    buffer = io.BytesIO()  # Создаем объект BytesIO для сохранения PDF
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Регистрация шрифта
    pdfmetrics.registerFont(TTFont('Roboto', 'Roboto-Regular.ttf'))
    c.setFont("Roboto", 12)

    # Определение количества секций на странице и высоты каждой секции
    num_sections_per_page = 7
    section_height = height / num_sections_per_page

    # Переменная для отслеживания текущей высоты, с которой начинается следующая секция
    current_height = height + section_height / 1.6

    for index, datamatrix_data in enumerate(datamatrix_codes):
        if index % num_sections_per_page == 0 and index != 0:
            c.showPage()  # Начать новую страницу, если текущая заполнена
            pdfmetrics.registerFont(TTFont('Roboto', 'Roboto-Regular.ttf'))
            c.setFont("Roboto", 12)
            current_height = height + section_height / 1.6  # Сброс высоты для новой страницы

        # Расчет позиции текущей секции
        y_position = current_height - section_height + (section_height / 4)

        # Добавление текста
        c.drawString(15, y_position, text1)
        c.drawString(15, y_position - 20, text2)
        c.drawString(15, y_position - 85, '----------------------------------------------')

        # Генерация и добавление баркода
        barcode_image = generate_barcode(barcode_data)
        c.drawImage(ImageReader(barcode_image), 15, y_position - 80, width=60, height=50, mask='auto')

        # Генерация и добавление DataMatrix кода
        datamatrix_image = generate_datamatrix(datamatrix_data)
        c.drawImage(ImageReader(datamatrix_image), 100, y_position - 80, width=50, height=50, mask='auto')

        # Обновление текущей высоты
        current_height -= section_height

    c.save()  # Завершение работы с PDF
    buffer.seek(0)  # Перемещаем указатель в начало буфера

    return buffer
