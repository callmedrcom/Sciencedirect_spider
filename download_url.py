import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
#
# url = 'https://www.sciencedirect.com/science/article/pii/S2666651020300012'
def download_url(url):
    headers = {
        'user-agent': '(Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    bsObj = BeautifulSoup(res.text, 'lxml')
    content = bsObj.findAll('script', {'type': 'application/json'})[0].text
    content_json = json.loads(content)
    info_dict = {}
    info_dict['volume_num'] = int(content_json['article']['vol-first'])
    info_dict['doi'] = content_json['article']['doi']
    info_dict['affiliation'] = ''
    affs = content_json['authors']['affiliations']
    firstaff = next(iter(affs))
    firstaff= affs.get(firstaff)
    num_aff = len(affs)
    for l in range(len(firstaff)):
        try:
            info_dict['affiliation'] = info_dict['affiliation'] + firstaff['$$'][num_aff][
                '$$'][l]['_'] + ','
        except:
            info_dict['affiliation'] = info_dict['affiliation'] + firstaff['$$'][num_aff]['_'] + ','
    info_dict['title'] = content_json['article']['titleString']

    # keywords
    try:
        keywords_div = bsObj.findAll('div', class_="keywords-section")[0].findAll('div', class_='keyword')
        keywords_list = [keyword.text for keyword in keywords_div]
        kw = ''
        for keyword in keywords_list:
            kw = kw + keyword + ';'
        info_dict['kw_num'] = len(keywords_list)
    except:
        keywords_list = ['no key words']
        info_dict['kw_num'] = 0

    info_dict['abstract'] = bsObj.findAll('div', {'class': 'abstract author'})[0].text

    return info_dict
