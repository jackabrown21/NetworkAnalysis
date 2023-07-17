import csv
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

def generate_url(cik, accession_number):
    list_of_urls = []
    base_url = "https://www.sec.gov/Archives/edgar/data/"
    acc_no_dash = accession_number.replace('-', '')
    x = base_url + str(cik) + '/' + acc_no_dash + '/' + accession_number + '-index.htm'
    list_of_urls.append(x)
    return list_of_urls

list_of_htm_urls = []

with open('data/raw/SoutheasternAssetManagementSince2014.csv', 'r') as file:
    reader = csv.DictReader(file)
    count = 0
    for row in reader:
        count += 1
        url = generate_url(807985, row['Accession number'])
        list_of_htm_urls += url

def get_links(url):
    headers = {
        'User-Agent': 'Jack Brown jackabrown21@gmail.com',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'www.sec.gov',
        'From': 'jackabrown21@gmail.com'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        page_content = response.content
        soup = BeautifulSoup(page_content, 'html.parser')
        links = soup.find_all('a')
        page_links = []
        for link in links:
            href = link.get('href')
            if href:
                page_links.append(href)
        return page_links

every_link_on_that_page = []
for x in list_of_htm_urls[0:1]:
    every_link_on_that_page += get_links(x)

def the_xml_link_we_want_to_download(link_list):
    the_xmls_on_that_page = []
    for link in link_list:
        if link.endswith("xml"):
            the_xmls_on_that_page.append(link)
    return "https://www.sec.gov/" + the_xmls_on_that_page[-1]

print(the_xml_link_we_want_to_download(every_link_on_that_page))
