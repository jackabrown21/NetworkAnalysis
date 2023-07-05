import requests
from xml.etree import ElementTree
import pandas as pd


#Takes list of URLs, yields content of each filing
def get_filings(filing_urls):
    for url in filing_urls:
        response = requests.get(url)
        if response.status_code == 200:
            yield response.content

#Takes the context of an XML file and parses for useful information
def parse_xml(xml_content):
    root = ElementTree.fromstring(xml_content)
    for info_table in root.findall('infoTable'):
        # The "useful information" being extracted
        yield {
            'nameOfIssuer': info_table.find('nameOfIssuer').text,
            'titleOfClass': info_table.find('titleOfClass').text,
            'cusip': info_table.find('cusip').text,
            'value': info_table.find('value').text,
            'sshPrnamt': info_table.find('sshPrnamt').text,
            'investmentDiscretion': info_table.find('investmentDiscretion').text,
            'votingAuthority': info_table.find('votingAuthority').text,
            
        }

#Saves data from list of dictionaries to a CSV file with specified filename
def save_data(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def main():
    filing_urls = [...]
    data = []
    for xml_content in get_filings(filing_urls):
        data.extend(parse_xml(xml_content))
    save_data(data, 'data.csv')

if __name__ == '__main__':
    main()
