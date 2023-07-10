from sec_edgar_downloader import Downloader
import os
import xml.etree.ElementTree as ET

def parse_xml(xml_path):
    # similar to your existing parse_xml, but operates on a file
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    for info_table in root.findall('{http://www.sec.gov/edgar/thirteenffiler}infoTable'):
        issuer = info_table.find('{http://www.sec.gov/edgar/thirteenffiler}nameOfIssuer').text
        title = info_table.find('{http://www.sec.gov/edgar/thirteenffiler}titleOfClass').text
        value = info_table.find('{http://www.sec.gov/edgar/thirteenffiler}value').text
        print(f"Issuer: {issuer}, Title: {title}, Value: {value}")

def main():
    dl = Downloader("data/raw")
    
    CIK_SE = "0000807985"  
    CIK_FMI = "0000764532"  
    CIK_PC = "0001034524"  

    dl.get("13F-HR", CIK_SE, amount=1)  # get the latest filing
    dl.get("13F-HR", CIK_FMI, amount=1)  # get the latest filing
    dl.get("13F-HR", CIK_PC, amount=1)  # get the latest filing

    for root_dir, dirs, files in os.walk("data/raw"):
        for file in files:
            if file.endswith('.xml'):
                parse_xml(os.path.join(root_dir, file))

if __name__ == '__main__':
    main()
