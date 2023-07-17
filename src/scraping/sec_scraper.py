import csv
import requests
from bs4 import BeautifulSoup
import os

def generate_urls(cik, accession_number):
    list_of_urls = []
    base_url = "https://www.sec.gov/Archives/edgar/data/"
    acc_no_dash = accession_number.replace('-', '')
    x = base_url + str(cik) + '/' + acc_no_dash + '/' + accession_number + '-index.htm'
    list_of_urls.append(x)
    return list_of_urls

def read_csv_and_generate_urls(file_path, cik):
    sec_filing_urls = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            url = generate_urls(cik, row['Accession number'])
            sec_filing_urls += url
    return sec_filing_urls

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
    
def get_the_xml_link_we_want_to_download(link_list):
    the_xmls_on_that_page = []
    for link in link_list:
        if link.endswith("xml"):
            the_xmls_on_that_page.append(link)
    return "https://www.sec.gov/" + the_xmls_on_that_page[-1]

import os
import requests

import os
import requests

def download_files_from_links(links, directory='data/raw/SoutheasternAssetManagement'):
    headers = {
        'User-Agent': 'Jack Brown jackabrown21@gmail.com',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'www.sec.gov',
        'From': 'jackabrown21@gmail.com'
    }
    if not os.path.exists(directory):
        os.makedirs(directory)

    for link in links:
        try:
            filename = link.split('/')[-1]
            filepath = os.path.join(directory, filename)
            # Only download the file if it does not already exist
            if not os.path.exists(filepath):
                response = requests.get(link, headers=headers)
                response.raise_for_status() # This line will raise an exception if the request is not successful
                with open(filepath, 'wb') as file:
                    file.write(response.content)
                print(f'Successfully downloaded file: {filepath}')
            else:
                print(f'File already exists: {filepath}')
        except requests.exceptions.RequestException as err:
            print(f'Failed to download file from link: {link}')
            print(f'Error: {err}')

def main():
    # Put in the file path of the CSV you have set up
    file_path = 'data/raw/SoutheasternAssetManagementSince2014.csv'

    # Put in the CIK number of the data of the company inside that CSV
    cik = 807985

    sec_filings_htm_urls = read_csv_and_generate_urls(file_path, cik)

    huge_list_of_lists_of_every_single_link_on_every_single_filing = []
    for i in sec_filings_htm_urls:
        huge_list_of_lists_of_every_single_link_on_every_single_filing.append(get_links(i))

    final_list_of_every_single_xml_file_to_download = []
    for list in huge_list_of_lists_of_every_single_link_on_every_single_filing:
        final_list_of_every_single_xml_file_to_download.append(get_the_xml_link_we_want_to_download(list))
    

    # What get's printed is the link of every single XML that you want to download
    #print(final_list_of_every_single_xml_file_to_download)

    # Change the directory to wherever you want each of these files to be saved
    download_files_from_links(final_list_of_every_single_xml_file_to_download, directory='data/raw/SoutheasternAssetManagement')

if __name__ == "__main__":
    main()
    