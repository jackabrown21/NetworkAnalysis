# Read the XML files, extract the necessary data, store in pandas DataFrame

import pandas as pd
from bs4 import BeautifulSoup
import os

def scrape_13f(file):
    date = file
    html = open(file).read()
    soup = BeautifulSoup(html, 'lxml')
    rows = soup.find_all('tr')[11:]
    positions = []
    for row in rows:
        dic = {}
        position = row.find_all('td')
        dic["NAME_OF_ISSUER"] = position[0].text
        dic["TITLE_OF_CLASS"] = position[1].text
        dic["CUSIP"] = position[2].text
        try:
            dic["VALUE"] = int(position[3].text.replace(',', ''))*1000
        except ValueError:
            dic["VALUE"] = 0
        dic["SHARES"] = int(position[4].text.replace(',', ''))
        dic["DATE"] = date.strip(".html")
        positions.append(dic)

    df = pd.DataFrame(positions)
    return df

folder_path = "data/raw/SoutheasternAssetManagement"
file_list = os.listdir(folder_path)
for file in file_list:
    file_path = os.path.join(folder_path, file)
    print(scrape_13f(file_path))
