import csv
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

def get_safe_filename(url):
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return f'{url_hash}.xml'

def get_headers():
    return {
        'User-Agent': os.getenv('USER_AGENT'),
        'Accept-Encoding': os.getenv('ACCEPT_ENCODING'),
        'Host': os.getenv('HOST'),
        'From': os.getenv('FROM')
    }

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
    headers = get_headers()
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

def download_files_from_links(links, directory):
    headers = get_headers()
    if not os.path.exists(directory):
        os.makedirs(directory)

    for link in links:
        try:
            filename = get_safe_filename(link)
            filepath = os.path.join(directory, filename)
            if not os.path.exists(filepath):
                response = requests.get(link, headers=headers)
                response.raise_for_status()
                with open(filepath, 'wb') as file:
                    file.write(response.content)
                print(f'Successfully downloaded file: {filepath}')
            else:
                print(f'File already exists: {filepath}')
        except requests.exceptions.RequestException as err:
            print(f'Failed to download file from link: {link}')
            print(f'Error: {err}')

def main():

    # Dictionary of companies and their respective CIK numbers
    investment_firms = {
    "FiduciaryManagementInc": 764532,
    "SoutheasternAssetManagement": 807985,
    "PolenCapital": 1034524,
    "TweedyBrowne": 732905,
    "Dodge&Cox": 200217,
    "HarrisAssociates": 813917,
    "RuaneCuniff&Goldfarb": 1720792,
    "ArielInvestments": 936753,
    "GardnerRusso&Quinn": 860643,
    "FirstEagleInvestmentManagement": 1325447,
    "VulcanValuePartners": 1556785,
    "DavisSelectedAdvisors": 1036325
}

    # Assuming that the CSV files are named after the companies and are located in 'data/raw/companies_since_2014_csvs'
    base_file_path = 'data/raw/companies_since_2014_csvs/'

    for company_name, cik in investment_firms.items():
        company_file_path = base_file_path + company_name + '.csv'
        sec_filings_htm_urls = read_csv_and_generate_urls(company_file_path, cik)

        huge_list_of_lists_of_every_single_link_on_every_single_filing = []
        for i in sec_filings_htm_urls:
            huge_list_of_lists_of_every_single_link_on_every_single_filing.append(get_links(i))

        final_list_of_every_single_xml_file_to_download = []
        for list in huge_list_of_lists_of_every_single_link_on_every_single_filing:
            final_list_of_every_single_xml_file_to_download.append(get_the_xml_link_we_want_to_download(list))

        # Create and save each XML to a folder in data/raw with the name of the company as the name of the folder
        download_files_from_links(final_list_of_every_single_xml_file_to_download, directory=f'data/raw/{company_name}')

if __name__ == "__main__":
    main()
    