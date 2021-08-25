import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_resi(fname):
    with open(fname, "r") as out:
        hasil = out.read()
        
    return hasil.split('\n')

browser = webdriver.Chrome(executable_path='./chromedriver.exe')
browser.get('https://www.sicepat.com/checkAwb')


resis = get_resi('resi.txt')


c = 0
for resi in resis:
    pathnya = '//input[@name="awbNumber[{}]"]'.format(c)
    try:
        elem = browser.find_element_by_xpath(pathnya)
    except NoSuchElementException as e:
        tambah = browser.find_element_by_xpath('//span[@class="check-awb_addAwb__J1J6U"]')
        tambah.click()
    
    elem = browser.find_element_by_xpath(pathnya)
    elem.send_keys(resi)
        
    c += 1

elem.send_keys(Keys.ENTER)

keys = ['resi', 'type', 'kota', 'penerima', 'tgl', 'track', 'ongkir', 'status']
hasil = []

rows = []

while len(rows) < len(resis):
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//tbody/tr')))
    rows = browser.find_elements_by_xpath('//tbody/tr')


for row in rows:
    tds = row.find_elements_by_xpath('td')
    if(tds.__len__() !=  8):
        continue
    
    item = {}
    
    for c in range(0, len(keys)):
        value = tds[c].text
        key = keys[c]
        
        item[key] = value
    
    hasil.append(item)

with open('hasil.csv', 'w+', newline="") as out:
    writer = csv.DictWriter(out, fieldnames = keys)
    writer.writeheader()
    
    for item in hasil:
        writer.writerow(item)



