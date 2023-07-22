from logging import root
import pandas as pd
import xml.etree.ElementTree as ET

pd.set_option("display.max_rows", None)

def process_xml_file(filepath):
    data = []
    
    tree = ET.parse(filepath)
    root = tree.getroot()
    namespace = "{http://www.sec.gov/edgar/document/thirteenf/informationtable}"

    def findtext(elem, tag):
        """Helper function to find text in an element, return empty string if not found"""
        found = elem.find(".//{0}{1}".format(namespace, tag))
        if found is not None:
            return found.text
        else:
            return ""

    for info_table in root.findall(".//{0}infoTable".format(namespace)):
        name_of_issuer = findtext(info_table, "nameOfIssuer")
        title_of_class = findtext(info_table, "titleOfClass")
        cusip = findtext(info_table, "cusip")
        value = findtext(info_table, "value")
        ssh_prnamt = findtext(info_table, "shrsOrPrnAmt/sshPrnamt")
        ssh_prnamt_type = findtext(info_table, "shrsOrPrnAmt/sshPrnamtType")
        put_or_call = findtext(info_table, "putCall")
        investment_discretion = findtext(info_table, "investmentDiscretion")
        other_manager = findtext(info_table, "otherManager")
        voting_authority_sole = findtext(info_table, "votingAuthority/Sole")
        voting_authority_shared = findtext(info_table, "votingAuthority/Shared")
        voting_authority_none = findtext(info_table, "votingAuthority/None")

        data.append({
            "Name of Issuer": name_of_issuer,
            "Title of Class": title_of_class,
            "CUSIP": cusip,
            "Value": value,
            "SSH Prnamt": ssh_prnamt,
            "SSH Prnamt Type": ssh_prnamt_type,
            "Put or Call": put_or_call,
            "Investment Discretion": investment_discretion,
            "Other Manager": other_manager,
            "Voting Authority Sole": voting_authority_sole,
            "Voting Authority Shared": voting_authority_shared,
            "Voting Authority None": voting_authority_none
        })

    df = pd.DataFrame(data)
    return df

# Provide the filepath of the XML file
filepath = "data/raw/SoutheasternAssetManagement/13f122.xml"

# Process the XML file and create a pandas DataFrame
df = process_xml_file(filepath)

# Print the DataFrame
print(df)

# Save the DataFrame to a csv
df.to_csv("data/processed/outputfile2.csv", index=False)
