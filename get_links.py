import os
import shutil
import tempfile
import pandas as pd
from io import StringIO

csv_path  = r'PATH'
excel_out = r'C:\Users\Admin\Downloads\publication_URL.xlsx'
MAX_EXCEL_ROWS = 1_048_576  # макс. строк на лист
CHUNK_SIZE     = MAX_EXCEL_ROWS

tmp_path = os.path.join(tempfile.gettempdir(), 'temp_data.csv')
shutil.copy2(csv_path, tmp_path)
try:
    df = pd.read_csv(tmp_path,
                     engine='python',
                     skip_blank_lines=True,
                     encoding='utf-8')
except PermissionError:
    with open(tmp_path, 'r', encoding='utf-8', errors='ignore') as f:
        df = pd.read_csv(StringIO(f.read()),
                         skip_blank_lines=True)
if df.shape[1] < 58:
    raise IndexError("В CSV меньше 58 столбцов — не найден столбец BF/publication URL")
series = df.iloc[:, 57].dropna().reset_index(drop=True)

with pd.ExcelWriter(
    excel_out,
    engine='xlsxwriter',
    engine_kwargs={'options': {'strings_to_urls': False}}
) as writer:
    total = len(series)
    for part, start in enumerate(range(0, total, CHUNK_SIZE), start=1):
        chunk = series.iloc[start:start + CHUNK_SIZE]
        sheet_name = f'part{part}'
        chunk.to_frame(name='publication URL') \
             .to_excel(writer,
                       sheet_name=sheet_name,
                       index=False)
        print(f'— Лист {sheet_name}: строки {start + 1}–{start + len(chunk)} записаны')

print("✅ Все ссылки успешно записаны:")
print(f"  • Excel: {excel_out} (разбито на {part} листов, гиперссылки выключены)")
