from selenium import webdriver
from selenium.webdriver.common.by import By
import mysql.connector
import pandas as pd
driver = webdriver.Chrome()
driver.get("https://www.bseindia.com/markets/equity/EQReports/bulk_deals.aspx")

data = []

# elements= driver.find_element(By.XPATH, "/html/body/form/div[4]/div/div/div[3]/div/div/table/tbody/tr/td/div/table")
# print(elements.text)

rows= driver.find_elements(By.XPATH, "/html/body/form/div[4]/div/div/div[3]/div/div/table/tbody/tr/td/div/table")

for row in rows:  
    cells = row.find_elements(By.XPATH,".//td")
    row_data = {
        'Deal Date': cells[0].text,
        'Security Code': int(cells[1].text),
        'Security Name': cells[2].text,
        'Client Name': cells[3].text,
        'Deal Type': cells[4].text,
        'Quantity': int(cells[5].text.replace(',', '')),
        'Price': float(cells[6].text)
    }
    data.append(row_data)

df = pd.DataFrame(data)
print(df)

db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='******',
    database='Scraping'
)

cursor = db_connection.cursor()

create_table_query = '''
CREATE TABLE scraped_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `Deal Date` DATE,
    `Security Code` INT,
    `Security Name` VARCHAR(255),
    `Client Name` VARCHAR(255),
    `Deal Type` VARCHAR(1),
    `Quantity` INT,
    `Price` FLOAT
)
'''

cursor.execute(create_table_query)

insert_data_query = "INSERT INTO scraped_data (`Deal Date`, `Security Code`, `Security Name`, `Client Name`, `Deal Type`, `Quantity`, `Price`) VALUES (%s, %s, %s, %s, %s, %s, %s)"

for _, row in df.iterrows():
    data_to_insert = (
        pd.to_datetime(row['Deal Date']).date(),
        row['Security Code'],
        row['Security Name'],
        row['Client Name'],
        row['Deal Type'],
        row['Quantity'],
        row['Price']
    )
    cursor.execute(insert_data_query, data_to_insert)