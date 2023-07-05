import os
import pandas as pd
from src.scraping.sec_scraper import parse_xml, save_data

def test_parse_xml():
    with open('test/test_file.xml', 'r') as file:
        xml_content = file.read()
        data = list(parse_xml(xml_content))
        assert len(data) == 1
        assert data[0] == {
            'nameOfIssuer': 'Test Company',
            'titleOfClass': 'COM',
            'cusip': '012345678',
            'value': '100000',
            'sshPrnamt': '5000',
            'investmentDiscretion': 'SOLE',
        }

def test_save_data():
    data = [{'nameOfIssuer': 'Test Company', 'titleOfClass': 'COM', 'cusip': '012345678'}]
    save_data(data, 'test_output.csv')
    df = pd.read_csv('test_output.csv')
    assert not df.empty
    assert df.loc[0, 'nameOfIssuer'] == 'Test Company'
    os.remove('test_output.csv')
