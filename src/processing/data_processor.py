import csv
from bs4 import BeautifulSoup
import os

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
    # Specify your directory with all of the raw XMLs
    input_base_dir = 'data/raw'

    # Specify your the directory where you would like all of the new folders with their CSVs inside to be saved
    output_base_dir = 'data/processed'

    for company_name in os.listdir(input_base_dir):
        input_company_dir = os.path.join(input_base_dir, company_name)

        if not os.path.isdir(input_company_dir):
            continue

        output_company_dir = os.path.join(output_base_dir, company_name)

        os.makedirs(output_company_dir, exist_ok=True)

        for file_name in os.listdir(input_company_dir):
            if file_name.endswith('.xml'):
                output_file_name = file_name.replace('.xml', '.csv')

                input_file_path = os.path.join(input_company_dir, file_name)
                output_file_path = os.path.join(output_company_dir, output_file_name)

                process_file(input_file_path, output_file_path)

if __name__ == "__main__":
    main()