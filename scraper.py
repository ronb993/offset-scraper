# more to add to this, only using this for testing purposes
import requests, re, dHook
from bs4 import BeautifulSoup
from table2ascii import table2ascii as t2a, PresetStyle

URLS={ 'CBaseEntity' : 'https://apex.dumps.host/?class=CBaseEntity',
    'cPlayer' : 'https://apex.dumps.host/?class=CPlayer',
    'offsets' : 'https://apex.dumps.host/offsets'
}

def sendDiscord(msg, url: str):
    if not url:
        return
    data = {"content": f"```\n{msg}\n```"}
    requests.post(url, json=data)


def get_results():
    page = requests.get(URLS['CBaseEntity'])
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all('tbody', class_='bg-gray-50 dark:bg-gray-700 divide-y divide-gray-200 dark:divide-gray-500')
    for result in results:
        list = re.sub(r"(\n)+", r"\n", re.sub(r"{3, }", "", result.get_text())).split()
    return list

def get_cbaseOffsets():
    cbaseOffsets = {}
    result_list = get_results()
    for result in result_list:
        if result == 'm_localOrigin':
            offsetIndex = result_list.index('m_localOrigin') + 2
            offsetValue = result_list[offsetIndex]
            cbaseOffsets['m_localOrigin'] = offsetValue

        elif result == 'm_iTeamNum':
            offsetIndex = result_list.index('m_iTeamNum') + 2
            offsetValue = result_list[offsetIndex]
            cbaseOffsets['m_iTeamNum'] = offsetValue
            
        elif result == 'm_iName':
            offsetIndex = result_list.index('m_iName') + 2
            offsetValue = result_list[offsetIndex]
            cbaseOffsets['m_iName'] = offsetValue

    return cbaseOffsets

def checkResults():
    x = get_cbaseOffsets()
    if x['m_localOrigin'] == '0x58':
        change_one = 'no'
    else:
        change_one = 'yes'
    if x['m_iTeamNum'] == '0x448':
       change_two = 'no'
    else:
        change_two = 'yes'
    if x['m_iName'] == '0x589':
        change_three = 'no'
    else:
        change_three = 'yes'
    myResults = t2a( # todo add dictionary values here to reflect the table
        header=["Offset", "Value", "Change?"],
        body=[["localOrigin", x['m_localOrigin'], change_one], ["iTeamNum", x['m_iTeamNum'], change_two], ["iName", x['m_iName'], change_three]],
        column_widths=[13] * 3,
        style=PresetStyle.ascii_box 
    )
    return myResults

checkResults()
sendDiscord(checkResults(), dHook.url) #todo fix table, it looks funky when window isnt maximized
