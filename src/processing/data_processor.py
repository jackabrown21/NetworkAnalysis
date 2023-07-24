import csv
from bs4 import BeautifulSoup

def process_file(file_name, file_to_be_written_to):
    with open(file_name, 'r') as f:
        data = f.read()

    soup = BeautifulSoup(data, "lxml")

    info_table = soup.find_all('infotable')

    data = []

    for info in info_table:
        name_of_issuer = info.find('nameofissuer').text
        title_of_class = info.find('titleofclass').text
        cusip = info.find('cusip').text
        value = info.find('value').text
        sshPrnamt = info.find('sshprnamt').text
        sshPrnamtType = info.find('sshprnamttype').text
        investmentDiscretion = info.find('investmentdiscretion').text
        other_manager = info.find('othermanager').text if info.find('othermanager') else 'NA'
        sole = info.find('sole').text
        shared = info.find('shared').text
        none = info.find('none').text

        data.append([name_of_issuer, title_of_class, cusip, value, sshPrnamt, sshPrnamtType, investmentDiscretion, other_manager, sole, shared, none])

    with open(file_to_be_written_to, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name of Issuer', 'Title of Class', 'CUSIP', 'Value', 'sshPrnamt', 'sshPrnamtType', 'Investment Discretion', 'Other Manager', 'Sole', 'Shared', 'None'])
        writer.writerows(data)

def main():
    # Put the path of the file that you want to be processed as the first argument, and the path of the csv you want it to be saved to as the second argument
    process_file('data/raw/PolenCapitalManagement/1a27bf39005ff6148cc7bbd08b9989ba.xml', "data/processed/PolenCapitalManagement/cashagain.csv")

if __name__ == "__main__":
    main()