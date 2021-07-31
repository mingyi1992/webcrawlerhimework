import requests
from bs4 import BeautifulSoup
import time
import csv
import json

keyword = '資訊分析師'

url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword={}'.format(keyword)

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}

job_datas = []
for p in range(1,16):
    url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90%E5%B8%AB&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=15&asc=0&page='+str(p)+'&mode=s&jobsource=2018indexpoc'
    res = requests.get(url,headers=headers)

    objsoup = BeautifulSoup(res.text,'html.parser')
    jobs=objsoup.select('article[class="b-block--top-bord job-list-item b-clearfix js-job-item"]')

    for job in jobs:
        opening = job['data-job-name']
        company = job['data-cust-name']
        address = job.select('ul[class="b-list-inline b-clearfix"]')[0].select('a')[0]["title"].split('公司住址：')[1]
        salary = job.select('span[class="b-tag--default"]')[0].text
        seniority_level = job.select('ul[class="b-list-inline b-clearfix job-list-intro b-content"]')[0].select('li')[1].text
        edbg = job.select('ul[class="b-list-inline b-clearfix job-list-intro b-content"]')[0].select('li')[2].text
        jobhref = "https"+(job.select('div[class="b-block__left"]')[0].select('a[class="js-job-link"]')[0]['href'])

        n = jobhref.split("?")[0].split("/")[-1]
        urlArticle = "https://www.104.com.tw/job/ajax/content/"+n
        headersArticle = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            "Referer": "https://www.104.com.tw/job/"+n
        }
        resArt = requests.get(urlArticle, headers=headersArticle)

        res_json = json.loads(resArt.text)
        major = res_json['data']['condition']['major']
        if major==[]:
            major="-"
        try:
            languages = res_json['data']['condition']['language'][0]['language']+":"+res_json['data']['condition']['language'][0]['ability']
        except:
            languages = "-"
        try:
            i = res_json['data']['condition']['specialty']
            cache = []
            for j in i:
                cache.append(j['description'])
            description = cache
        except:
            description="-"
        if description==[]:
            description = "-"

        job_data = {'職缺內容' : opening,
                    '公司名稱' : company,
                    '公司地址' : address,
                    '薪資待遇' : salary,
                    '資歷要求' : seniority_level,
                    '學歷要求' : edbg,
                    '網頁連結' : jobhref,
                    '要求科系' : major,
                    '需求語言' : languages,
                    '工具程式' : description
                    }
        job_datas.append(job_data)
        time.sleep(1)

filename = "104.csv"
cloumns_name = ['職缺內容', '公司名稱', '公司地址', '薪資待遇', '資歷要求', '學歷要求', '網頁連結', '要求科系', '需求語言', '工具程式']
with open(filename, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=cloumns_name, delimiter=',')
    writer.writeheader()
    for data in job_datas:
        writer.writerow(data)
