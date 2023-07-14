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

pd.set_option('display.max_rows', None)
folder_path = "data/raw/SoutheasternAssetManagement"
file_list = os.listdir(folder_path)
output_folder = "data/output"  # Specify the output folder path

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for file in file_list:
    file_path = os.path.join(folder_path, file)
    df = scrape_13f(file_path)
    output_file = os.path.join(output_folder, f"{file.strip('.xml')}.csv")  # Construct the output file path
    df.to_csv(output_file, index=False)  # Save the DataFrame as a CSV file

    print(f"CSV file saved: {output_file}")
