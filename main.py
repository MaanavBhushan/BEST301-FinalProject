import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import webbrowser
from quote import quote
import random


def save_to_excel(title, author, date, link, synopsis, summarization):
    global excel_title
    with open(excel_title, 'a', encoding='utf-8') as f:
        fieldnames = ['Title', 'Synopsis', 'Summarization', 'Author', 'Date', 'Link']
        writer = csv.DictWriter(f, lineterminator='\n', fieldnames=fieldnames)
        writer.writerow({'Title': title, 'Synopsis': synopsis, 'Summarization': summarization, 'Author': author, 'Date': date, 'Link': link})


# get_keyword = input("Put in search keyword: ")
get_keyword = "biomass"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get('https://afdc.energy.gov/publications/search/')

driver.implicitly_wait(3)
text_input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[1]/div/div[1]/form/input[3]')
text_input.send_keys(get_keyword)
search_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[1]/div/div[1]/form/input[4]')
search_button.click()
display_100 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/label/select/option[4]')
display_100.click()

driver.implicitly_wait(5)
table = driver.find_elements(By.CLASS_NAME, 'odd')
table = table + driver.find_elements(By.CLASS_NAME, 'even')
excel_number = datetime.now().strftime("%b-%m-%Y_at_%H_%M_%S")
excel_title = "literature_" + get_keyword + "_" + excel_number + ".csv"
with open(excel_title, "w", encoding="utf-8") as f:
    fieldnames = ['Title', 'Synopsis', 'Summarization', 'Author', 'Date', 'Link']
    writer = csv.DictWriter(f, lineterminator='\n', fieldnames=fieldnames)
    writer.writeheader()


for row in table:
    row.find_element(By.XPATH, "td").click()
    title = row.find_element(By.XPATH, 'td[1]').text
    author = row.find_element(By.XPATH, 'td[2]').text
    date = row.find_element(By.XPATH, 'td[3]').text
    expansion = driver.find_element(By.CLASS_NAME, 'description')
    link_xpath = expansion.find_element(By.XPATH, "td/p[1]/a")
    link = link_xpath.get_attribute("href")
    synopsis = expansion.find_element(By.XPATH, 'td/p[2]').text

    # Gets random quote from Greta Thunberg
    res = quote('Greta Thunberg')
    quotation = res[random.randint(0, 19)]['quote'] + " -Greta Thunberg"

    # save all the info into an excel sheet
    save_to_excel(title, author, date, link, synopsis, quotation)

# Load the Excel data into a Table
df = pd.read_csv(excel_title, encoding='iso-8859-1')

# Generate the HTML representation of the Table
html = df.to_html()
f = open("DataTable.html", "w", encoding="utf-8")
f.write(html)

webbrowser.open_new_tab('DataTable.html')

time.sleep(1000)

