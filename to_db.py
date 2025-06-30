import pandas as pd
import os
import sqlite3
from urllib.parse import urlparse, parse_qs

excel_path = r"C:\Users\Admin\Desktop\HelperParser\extracted_ab_bf.xlsx"
folder_path = r"C:\Users\Admin\Desktop\HelperParser\logo"
db_path = os.path.join(folder_path, 'company_images.db')

df = pd.read_excel(excel_path, dtype=str)
df = df.fillna('')

mapping = {}
for _, row in df.iterrows():
    link = row['BF']
    company = row['AB']
    if not link:
        continue
    parsed = urlparse(link)
    params = parse_qs(parsed.query)
    # ищем параметр DocNumber
    num_list = params.get('DocNumber') or params.get('docnumber')
    if num_list:
        number = num_list[0]
        mapping[number] = company

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS company_images (
        company TEXT,
        image_number TEXT
    );
''')
conn.commit()

for fname in os.listdir(folder_path):
    fpath = os.path.join(folder_path, fname)
    if not os.path.isfile(fpath):
        continue
    name, ext = os.path.splitext(fname)
    if not name:
        continue
    image_number = name
    company = mapping.get(image_number)
    if company:
        cur.execute(
            'INSERT INTO company_images (company, image_number) VALUES (?, ?);',
            (company, image_number)
        )

conn.commit()
conn.close()
print(f"База данных: {db_path}")
