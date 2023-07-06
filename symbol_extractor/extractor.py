import json


def convert_letters(text: str):
    replaceable_letters = {
        'ك': 'ک',
        'دِ': 'د',
        'بِ': 'ب',
        'زِ': 'ز',
        'ذِ': 'ذ',
        'شِ': 'ش',
        'سِ': 'س',
        'ى': 'ی',
        'ي': 'ی',
        '١': '۱',
        '٢': '۲',
        '٣': '۳',
        '٤': '۴',
        '٥': '۵',
        '٦': '۶',
        '٧': '۷',
        '٨': '۸',
        '٩': '۹',
        '٠': '۰'
    }

    for ar_letter in replaceable_letters:
        text = text.replace(ar_letter, replaceable_letters[ar_letter])

    return text


def extract_symbol(text):
    href = 'http://old.tsetmc.com/' + text.split('href="')[1].split('" target')[0].replace('&amp;', '&')
    symbol = text.split('>')[1].split('</')[0]
    return href, convert_letters(symbol)


def validate_symbol(text):
    return not (text.find('اخزا') > 0 or text.find('ض') == 0 or text[-1].isdigit() or text[-1] == 'ح')


all_data = {}

with open('data-c.txt', 'r') as f:
    data = f.read()

data = data.split('\n')
i = 0
validated = True
for item in data:
    if not validated:
        validated = True
        continue

    uri, txt = extract_symbol(item)
    if not validate_symbol(txt):
        validated = False
        continue

    if uri not in all_data:
        all_data[uri] = []

    all_data[uri].append(txt)

csv_version = 'url, symbol, company_name\n'
for item in all_data.keys():
    csv_version += f"{item}, {all_data[item][0]}, {all_data[item][1]}\n"

with open('../history_extractor/all_symbols.json', 'w') as f:
    f.write(json.dumps(all_data))

with open('../history_extractor/all_symbols.csv', 'w') as f:
    f.write(csv_version)
