import pandas as pd
import xml.etree.ElementTree as ET

pd.set_option("display.max_rows", None)

def process_xml_file(filepath):
    data = []
    
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    for info_table in root.findall(".//{http://www.sec.gov/edgar/document/thirteenf/informationtable}infoTable"):
        name_of_issuer = info_table.findtext(".//{http://www.sec.gov/edgar/document/thirteenf/informationtable}nameOfIssuer")
        title_of_class = info_table.findtext(".//{http://www.sec.gov/edgar/document/thirteenf/informationtable}titleOfClass")
        cusip = info_table.findtext(".//{http://www.sec.gov/edgar/document/thirteenf/informationtable}cusip")
        value = info_table.findtext(".//{http://www.sec.gov/edgar/document/thirteenf/informationtable}value")
        ssh_prnamt = info_table.findtext(".//{http://www.sec.gov/edgar/document/thirteenf/informationtable}sshPrnamt")
        investment_discretion = info_table.findtext(".//{http://www.sec.gov/edgar/document/thirteenf/informationtable}investmentDiscretion")

        data.append({
            "Name of Issuer": name_of_issuer,
            "Title of Class": title_of_class,
            "CUSIP": cusip,
            "Value": value,
            "SSH Prnamt": ssh_prnamt,
            "Investment Discretion": investment_discretion
        })

    df = pd.DataFrame(data)
    return df

# Provide the filepath of the XML file
filepath = "data/raw/SoutheasternAssetManagement/13f122.xml"

# Process the XML file and create a pandas DataFrame
df = process_xml_file(filepath)

# Print the DataFrame
print(df)
df.to_csv('data/output/outputfile.csv', index=False)
