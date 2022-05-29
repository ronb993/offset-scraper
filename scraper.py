# more to add to this, only using this for testing purposes
import requests, re, dHook
from bs4 import BeautifulSoup
from table2ascii import table2ascii as t2a, PresetStyle
import itertools

offsets = ['m_localOrigin',
        'm_iTeamNum',
        'm_iName',
        'm_lifeState',
        'm_ammoPoolCapacity',
        'm_bleedoutState',
        'level_name',
        'cl_entitylist',
        'local_player']

URLS=['https://apex.dumps.host/?class=CBaseEntity',
    'https://apex.dumps.host/?class=CPlayer',
    'https://apex.dumps.host/offsets']

def sendDiscord(msg, url: str):
    if not url:
        return
    data = {"content": f"```\n{msg}\n```"}
    requests.post(url, json=data)


def get_results():
    new_list = []
    url_one = []
    url_two = []
    url_three = []
    for URL in URLS:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all('tbody', class_='bg-gray-50 dark:bg-gray-700 divide-y divide-gray-200 dark:divide-gray-500')
        for result in results:
            list = re.sub(r"(\n)+", r"\n", re.sub(r"{3, }", "", result.get_text())).split()
            new_list.append(list)
    for (a, b, c) in itertools.zip_longest(new_list[0], new_list[1], new_list[2]):
        url_one.append(a), url_two.append(b), url_three.append(c)
    url_one.extend(url_two)
    url_one.extend(url_three)
    return url_one

def get_OffsetsList():
    myOffsets = {}
    results = get_results()
    for result in results:
        for offset in offsets:
            if result == offset:
                offsetIndex = results.index(offset) + 2
                offsetValue = results[offsetIndex]
                myOffsets[offset] = offsetValue
    return myOffsets

def checkResults():
    x = get_OffsetsList()
    if x['m_localOrigin'] == '0x58':
        ch_1 = 'no'
    else:
        ch_1 = 'yes'
    if x['m_iTeamNum'] == '0x448':
       ch_2 = 'no'
    else:
        ch_2 = 'yes'
    if x['m_iName'] == '0x589':
        ch_3 = 'no'
    else:
        ch_3 = 'yes'
    if x['m_lifeState'] == '0x798':
        ch_4 = 'no'
    else:
        ch_4 = 'yes'
    if x['m_bleedoutState'] == '0x2728':
        ch_5 = 'no'
    else:
        ch_5 = 'yes'

    myResults = t2a( # todo add dictionary values here to reflect the table
        header=["Offset", "Value", "Change?"],
        body=[["localOrigin", x['m_localOrigin'], ch_1],
        ["iTeamNum", x['m_iTeamNum'], ch_2],
        ["iName", x['m_iName'], ch_3],
        ["lifeState", x['m_lifeState'], ch_4],
        ["bleedOut", x['m_bleedoutState'], ch_5]],
        column_widths=[13] * 3,
        style=PresetStyle.ascii_box 
    )
    return myResults

#get_OffsetsList()
checkResults()
sendDiscord(checkResults(), dHook.url) #todo fix table, it looks funky when window isnt maximized
