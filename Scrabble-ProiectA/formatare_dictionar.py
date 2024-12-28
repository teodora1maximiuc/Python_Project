from charset_normalizer import detect

diacritic_map = {
    'Ă': 'A',
    'Â': 'A',
    'Î': 'I',
    'Ț': 'T',
    'Ș': 'S',
    'Ã': 'A', 
    'Þ': 'T', 
    'Š': 'S'
}

def replace_diacritics(text):
    for diacritic, replacement in diacritic_map.items():
        text = text.replace(diacritic, replacement)
    return text

file_path = r"C:\\Users\\Raluci\\OneDrive\\Desktop\\python\\Maximiuc_Teodora_3B2\\Scrabble-ProiectA\\ro_RO.dic"

with open(file_path, "rb") as f:
    raw_data = f.read()
    encoding = detect(raw_data)['encoding']

with open(file_path, "r", encoding=encoding) as f:
    data = f.readlines()

for i in range(len(data)):
    line = data[i].strip()
    line = line.upper()
    line = replace_diacritics(line)
    if "/" in line:
        line = line.split("/")[0]
    data[i] = line + '\n'

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(data)
