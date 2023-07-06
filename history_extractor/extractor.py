import json
import os.path
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

with open('all_symbols.json', 'r') as f:
    data = f.read()

data = json.loads(data)
data_keys = list(data.keys())

driver = webdriver.Firefox()
driver.implicitly_wait(1)


def next_page(page):
    try:
        driver.find_element(By.CSS_SELECTOR, f'a[onclick="this.grid.changePage({page});return false;"]').click()
    except:
        try:
            selector = f'a[onclick="this.grid.changePageRelative(this.grid.pagesInGroup);return false;"]'
            driver.find_element(By.CSS_SELECTOR, selector).click()
            driver.find_element(By.CSS_SELECTOR, f'a[onclick="this.grid.changePage({page});return false;"]').click()
        except:
            return False

    return True


def extract_data(text: str, till_date: str):
    rows = text.replace(',', '').split('\n  ')
    del rows[0]

    reached = False
    history = ''
    for row in rows:
        pcs = row.split(' ')

        if till_date and pcs[-1] == till_date:
            reached = True
            break

        history += f"{pcs[-1]}, {pcs[1]}, {pcs[0]}\n"

    return history, reached


for url in data_keys:
    previous_data = ''
    last_date = ''

    file_name = f'../histories/history_{data[url][0]}.csv'
    if os.path.exists(file_name):
        continue
        # with open(file_name, 'r') as f:
        #     previous_data = f.readlines()
        #     if len(previous_data) > 1:
        #         previous_data = previous_data[1:]
        #
        #     if len(previous_data) > 0:
        #         last_date = previous_data[0].split(',')[0]

    with open(file_name, 'w') as f:
        f.write('date, min_price, max_price\n')

    sleep(1)

    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, '.torquoise[onclick="ii.ShowTab(17)"]').click()

    p = 1
    while True:
        t = "\n" + driver.find_element(By.CSS_SELECTOR, 'div.objbox table.obj tbody').text
        with open(file_name, 'a') as f:
            history, reached = extract_data(t, last_date)
            f.write(history)

        if reached:
            break

        p += 1
        if not next_page(p):
            break

    if previous_data:
        with open(file_name, 'a') as f:
            f.write("".join(previous_data))
