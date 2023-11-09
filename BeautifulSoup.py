#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import re
import pprint
html_doc = """
<html>s
	<head>
		<title>The Dormouse's story</title></head>
	<body>
		<p class="title"><b>The Dormouse's story</b></p>
		<p class="story">Once upon a time there were three little sisters; and their names were
		<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
		<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
		<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
		and they lived at the bottom of a well.</p>

		<p class="story">...</p>
</body>
</html>
"""


# In[4]:


# html_doc을 파싱하기위한 soup 객체 생성
soup = BeautifulSoup(html_doc, 'html.parser')
pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(soup)
# 아래와 같다.
# print(soup.prettify())
# soup.text
# print(soup.find('a').text)  # find  find_all  select   select_one
# print(re.findall(r'<a.+>(.+)</a>',html_doc)) # 위의 명령을 정규표현식으로~
# soup.title
# soup.title.name
# soup.title.string
# soup.title.parent.name
# soup.p.name
# soup.p
# soup.p['class'] # class는 속성이다!!
# soup.a
# soup.find_all('a') # soup.find_all('a').text를 하면 a태그의 모든 text가 보인다?? NO!!!

## a태그의 모든 text 뽑아내려면 반복문 사용하면 가능! "soup.find_all('a')" 가 객체가 반복자료형이기 때문에 가능하다!
 # 반복자료형이라는 것이 리스트 형태인지 그렇다면 아래에 ,로 구분이 안되는데???????★
## a_text = [i.text for i in soup.find_all('a')]
## a_text
    
## soup.find_all('a',{'id':'link2'})   # soup.find_all('태그명',{'속성':'값'})
# soup.find(id="link3")   # soup.select('a[id=link2]')   #  soup.select('태그명[속성=값]')
# for link in soup.find_all('a'):
#     print(link.get('href'))
# print(soup.get_text())

# soup


# In[167]:


# 뉴스 항목 중 한 가지 선택하여 뉴스기사(목록) 가져오기
import requests
daum_news_url = 'https://news.daum.net/'
daum_news_data = requests.get(daum_news_url).text
data_html = BeautifulSoup(daum_news_data,'html.parser') # 가지고 온 정보의 .contents & .text가 html형식이므로(url이 왭페이지이기 때문) html로 parser해준다!!
# print(data_html.prettify)

# print(data_html)
# data_html.link['href']
# /html/body/div[2]/main/section/div/div[1]/div[1]/ul/li[2]/div/div/strong/a/text()
for i in data_html.select('div>div>strong>a'):
    print(i.text.strip())

# 질문 사진 있음 <a>태그에 안들어가있는 헤드라인이 있음


# In[140]:


# 첫 번째 제목에 해당하는 내용 출력
# url = data_html.select_one('div>div>strong>a').attrs['href']
# response = requests.get(url).text
# source = BeautifulSoup(response,'html.parser')

# # /html/body/div[1]/main/section/div/article/div[2]/div[2]/section/p[1]
# for i in source.select('html>body>div>main>section>div>article>div>div>section>p'):
#     print(i.text.strip())


# In[166]:


# 제목에 해당하는 내용 출력해보기
for i in data_html.select('div>div>strong>a'):
    url = i.attrs['href']
    response = requests.get(url).text
    data = BeautifulSoup(response,'html.parser')
    for j in data.select('html>body>div>main>section>div>article>div>div>section>p'):
        print(j.text.strip())


# In[199]:


# 해당 내용 .txt파일로 쓰기(해당 폴더에 만들어보기)
import os
os.chdir('C:/Users/LG/Desktop/python강의자료/')

f = open('daumnews_20230724','w')

for i in data_html.select('div>div>strong>a'):
    f.write('기사제목 : ' + i.text.strip() + '\n\n' + '기사내용' + '\n')
    url = i.get('href') # i.attr['href']도 가능
    result = requests.get(url).text
    article = BeautifulSoup(result,'html.parser')
    
    for j in article.select('html>body>div>main>section>div>article>div>div>section>p'):
        f.write(j.text.strip() + '\n')
    f.write('='*15 + '\n\n\n')

f.close()


# In[155]:


import requests,re
import pandas as pd
from bs4 import BeautifulSoup as bs
daum=requests.get('https://news.daum.net/').text  
soup = bs(daum, 'html.parser') 
for i in soup.select('a[class="link_gnb"]'):
    print(i.get('href'))
   


# In[173]:


import requests,re
import pandas as pd
from bs4 import BeautifulSoup as bs
daum=requests.get('https://news.daum.net/').text  
soup = bs(daum, 'html.parser') 
soup.select('a[class="link_gnb"]')
    


# In[198]:



# 사회,정치,경제,국제,문화,IT,연재,포토,팩트체크 화면으로 접속하여 첫 번째 기사 제목 .txt파일로 내보내기

import requests,re,os,sys
import pandas as pd
from bs4 import BeautifulSoup as bs

os.chdir('C:/Users/LG/Desktop/python강의자료/')

f = open('article_title.txt','w')
daum=requests.get('https://news.daum.net/').text  
soup = bs(daum, 'html.parser') 
for i in soup.select('a[class="link_gnb"]'):
    f.write(i.text + '\n')
    if re.match('/+',i.get('href')):
        url_a = daum_news_url + i.get('href')
    else:
        url_a = i.get('href')
    
    f.write('주소 :' + url_a + '\n')
    
    page_a = requests.get(url_a).text
    page_ht = BeautifulSoup(page_a,'html.parser')
    
    try : 
        k = page_ht.select_one('html>body>div>main>section>div>div>ul>li>div>div>strong>a')
        f.write('메인기사 : ' + k.text + '\n\n')
    
    except: f.write('\n\n')
        
f.close()
  


# In[197]:


# 사회,정치,경제,국제,문화,IT,연재,포토,팩트체크 화면으로 접속하여 첫 번째 기사 제목 .csv파일로 내보내기

import requests,re,os,sys
import pandas as pd
from bs4 import BeautifulSoup as bs

os.chdir('C:/Users/LG/Desktop/python강의자료/')

article_list = [['분야','주소','기사제목']]
daum=requests.get('https://news.daum.net/').text  
soup = bs(daum, 'html.parser') 
for i in soup.select('a[class="link_gnb"]'):
   
    if re.match('/+',i.get('href')):
        url_a = daum_news_url + i.get('href')
    else:
        url_a = i.get('href')

    page_a = requests.get(url_a).text
    page_ht = BeautifulSoup(page_a,'html.parser')
    
    try : 
        k = page_ht.select_one('html>body>div>main>section>div>div>ul>li>div>div>strong>a')
        article_list.append([i.text,url_a,k.text])
    
    except: 
        article_list.append([i.text,url_a,''])
        
article_df = pd.DataFrame(article_list)
article_df.columns = ['분야', '주소', '기사제목']
article_df = article_df[1:]
article_df

article_df.to_csv('daum.csv',encoding='cp949')

