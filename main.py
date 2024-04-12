from fastapi import FastAPI, UploadFile, File
from feature_convert.work_with_exel import find_info_from_exel
from feature_convert.create_pdf import create_pdf_with_codes
from feature_convert.work_with_pdf import extract_text_and_barcodes_from_pdf, FullInfo
from fastapi.responses import StreamingResponse
import shutil

app = FastAPI()

@app.post('/pdf')
def generate_pdf(pdf_file: UploadFile = File(...), excel_file: UploadFile = File(...)):
    with open("temp_pdf_file.pdf", "wb") as buffer:
        shutil.copyfileobj(pdf_file.file, buffer)

    with open("temp_excel_file.xlsx", "wb") as buffer:
        shutil.copyfileobj(excel_file.file, buffer)

    # pdf_path = '/Users/iliamorozov/Downloads/Waldberies/order_36bada20_1d3a_4bc7_aade_bfcd28e17e21_gtin_04680607271797_quantity.pdf'
    page_data = extract_text_and_barcodes_from_pdf("temp_pdf_file.pdf")
    exl_data = find_info_from_exel("temp_excel_file.xlsx", page_data.articul, page_data.size)
    full_info = FullInfo(page_data.articul, page_data.size, page_data.barcodes, exl_data.brend, exl_data.name_atribut, exl_data.chrt_id, exl_data.color, exl_data.barcode)
    pdf = create_pdf_with_codes(str(full_info.barcode), full_info.barcodes, f"Артикул {str(full_info.articul)}", f"Размер {str(full_info.size)}")

    def iterfile():
        yield pdf.getvalue()

    # Возвращаем PDF в ответе с соответствующим Content-Type
    return StreamingResponse(iterfile(), media_type='application/pdf', headers={"Content-Disposition": "attachment;filename=my_pdf.pdf"})
