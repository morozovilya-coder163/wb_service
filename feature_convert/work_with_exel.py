import pandas as pd

class ExelData:
    def __init__(self, brend, name_atribut, chrt_id, color, barcode):
        self.brend = brend
        self.name_atribut = name_atribut
        self.chrt_id = chrt_id
        self.color = color
        self.barcode = barcode

def find_info_from_exel(exel_path, article_number, size):
    df = pd.read_excel(exel_path, engine='openpyxl')

    # Ищем строку с данным артикулом
    row = df[(df['Артикул WB'] == article_number) & (df['Размер'] == size)]
    if not row.empty:
        brend = row.iloc[0]['Бренд']
        name_atribut = row.iloc[0]['Предмет']
        chrt_id = row.iloc[0]['Код размера (chrt_id)']
        color = row.iloc[0]['Артикул продавца']
        barcode = row.iloc[0]['Баркод']
        exel_data = ExelData(brend, name_atribut, chrt_id, color, barcode)

    return exel_data    
