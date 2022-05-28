# more to add to this, only using this for testing purposes
import requests
from bs4 import BeautifulSoup
import re

# Current Offset values
levelName = '0x135cd80'
clEntityList = '0x19fbcd8'
localPlayer = '0x1daca88'
localOrigin = '0x58'
iTeamNum = '0x448'
iName = '0x589'
lifeState = '0x798'
viewAngles = '0x2588'
bleedoutState = '0x2728'

URLS={
    'CBaseEntity' : 'https://apex.dumps.host/?class=CBaseEntity',
    'cPlayer' : 'https://apex.dumps.host/?class=CPlayer',
    'offsets' : 'https://apex.dumps.host/offsets'
}

cbaseOffsets={
    'localOrigin' : 'm_localOrigin', # must add (0x100)
    'iTeamNum' : 'm_iTeamNum',
    'iName' : 'm_iName'
}

cplayerOffsets={
    'lifeState' : 'm_lifeState',
    'viewAngles' : 'm_ammoPoolCapacity', # subtract (0x14)
    'bleedoutState' : 'm_bleedoutState'
}

coreOffsets={
    'levelName' : 'level_name',
    'clEntityList' : 'cl_entitylist',
    'localPlayer' : 'local_player'
}

page = requests.get(URLS['CBaseEntity'])
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all('tbody', class_='bg-gray-50 dark:bg-gray-700 divide-y divide-gray-200 dark:divide-gray-500')

def get_cbaseOffsets():
    #todo - create for loop for dict values
    offset_one = cbaseOffsets['localOrigin']
    offset_two = cbaseOffsets['iTeamNum']
    offset_three = cbaseOffsets['iName']
    result_list = get_results()
    for result in result_list:
        if result == offset_one:
            offset = result_list.index(offset_one) + 2
            newOffset = result_list[offset]
            if newOffset == localOrigin:
                print(cbaseOffsets['localOrigin'], "offset has not changed")
            else:
                print(cbaseOffsets['localOrigin'], "offset has changed")
        elif result == offset_two:
            offset = result_list.index(offset_two) + 2
            newOffset = result_list[offset]
            if newOffset == iTeamNum:
                print(cbaseOffsets['iTeamNum'], "offset has not changed")
            else:
                print(cbaseOffsets['iTeamNum'], "offset has changed")

        elif result == offset_three:
            offset = result_list.index(offset_three) + 2
            newOffset = result_list[offset]
            if newOffset == iName:
                print(cbaseOffsets['iName'], "offset has not changed")
            else:
                print(cbaseOffsets['iName'], "offset has changed")


# Todo - add functions for cplayer and coreoffsets, then return all values to a list
#def get_cplayerOffsets():
#def get_coreOffsets():




def get_results():
    for result in results:
        list = re.sub(r"(\n)+", r"\n", re.sub(r"{3, }", "", result.get_text())).split()
    return list

get_cbaseOffsets()
