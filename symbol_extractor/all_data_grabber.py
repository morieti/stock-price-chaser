from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

driver.implicitly_wait(5)
driver.get('http://www.tsetmc.com/Loader.aspx?ParTree=15131F')

sleep(5)

driver.find_element(By.CSS_SELECTOR, ".TopIcon.MwIcon.MwSetting").click()
driver.find_element(By.CSS_SELECTOR, 'div[aria-label="نمایش همه نمادها در دیده بان"]').click()

sleep(1)

driver.find_element(By.CSS_SELECTOR, ".TopIcon.MwIcon.MwSetting").click()
driver.find_element(By.CSS_SELECTOR, 'div[aria-label="گروه بندی گروه های صنعت در دیده بان - خیر"]').click()

sleep(1)

pageSource = driver.execute_script("return document.documentElement.outerHTML;")

with open('data.txt', 'w') as f:
    f.write(pageSource)

driver.close()
