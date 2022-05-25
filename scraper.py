import requests
from bs4 import BeautifulSoup
import re


URL = "https://apex.dumps.host/?class=CBaseEntity"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all('tbody', class_='bg-gray-50 dark:bg-gray-700 divide-y divide-gray-200 dark:divide-gray-500')

def get_offsets():
    offset_name = "m_iTeamNum"
    result_list = get_results()
    for result in result_list:
        if result == offset_name:
            offset = result_list.index('m_iTeamNum') + 2
            print("offset Name: ",result,"\noffset value: ",result_list[offset])

def get_results():
    for result in results:
        list = re.sub(r"(\n)+", r"\n", re.sub(r"{3, }", "", result.get_text())).split()
    return list

get_offsets()
