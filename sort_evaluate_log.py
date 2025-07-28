import csv
from glob import glob
from utils.tools import make_choices
import os

log_files = glob('./data/evaluate_log' + '/*.csv')

selected_csv = make_choices(log_files)[0]

print(selected_csv)

with open(selected_csv, newline='') as f:
    reader = list(csv.reader(f))
    header = reader[0]
    rows = reader[1:]

sorted_rows = sorted(rows, key=lambda x: float(x[3]))

basename = os.path.basename(selected_csv)

with open(f'{selected_csv}', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(sorted_rows)



