from bs4 import BeautifulSoup
import requests
import sys
from datetime import datetime
import csv
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from collections import defaultdict
from selenium.webdriver import ActionChains
from pandas import DataFrame
import time
import glob
import pandas as pd
import numpy as np
from tag_mapping import tag_mapping
from decimal import Decimal, InvalidOperation

now = datetime.now().date()
header = ['site','title', 'instructor', 'description', 'url', 'price', 'tags', 'rating', 'thumbnail_url', 'is_package', 'is_free', 'enrollment_count']

# 구름에듀
def goorm_crawl():  
    ORIGIN_PATH = 'https://edu.goorm.io'

    def parse_detail(detail_url: str) -> dict:
        """
        url 상세 페이지 파싱 함수
        포함된 정보 : title', 'instructor', 'description', 'url', 'price', 'tag', 'category', 'rating', 'thumbnail_url', 'is_package', 'is_free', 'enrollment_count'
        """

        row_template = dict.fromkeys(header)  # 딕셔너리 초기화
        path_res = requests.get(detail_url)
        path_soup = BeautifulSoup(path_res.content, 'html.parser')

        row_template['url'] = detail_url

        # min 정보 변수
        row_template['site'] = '구름에듀'
        row_template['title'] = path_soup.find('h1').text
        row_template['instructor'] = str(path_soup.find(
            'div', attrs={'class': '_2xx4v5'}).text).replace('캡틴', '')

        row_template['thumbnail_url'] = path_soup.find(
            'div', attrs={'data-mkt-id': 'edu_lectureDetail_img_thumbnail'}).get('style').replace('background-image:url(', '').replace(')', '')
        description = path_soup.find(
            'p', attrs={"class": "RoScUb"}).text
        row_template['description'] = None if description == '' else description

        # Table 파싱
        questions = path_soup.find_all('div', attrs={'class': 'GIADkp'})
        answers = path_soup.find_all(
            'div', attrs={'class': '_2yM5um'})
        
        tags_list = []
        for question, answer in zip(questions, answers):
            tags = ''
            if question.text == '태그':
                tags = answer.text.replace(
                    ' ', '').lower()  # 정해진 규칙이 없어서 dash 로 다중 구분
            if question.text == '난이도':
                tags = answer.text.replace(
                    ' ', '').lower()  # 정해진 규칙이 없어서 dash 로 다중 구분    
            if question.text == '카테고리':
                tags = list(
                    answer.text.replace(' ', '').split(','))[-1].replace('-', ',')
            if tags:
                tags_list.append(tags)
        tags_list.append('구름에듀')
        row_template['tags'] = ','.join(tags_list)
        # 가격 관련 변수
        price = path_soup.find(
            'div', attrs={'data-mkt-id': 'edu_lecture_div_lecturePrice'}).text
        row_template['is_free'] = False if price != '무료' else True
        row_template['price'] = int(
            price.replace(',', '')) if price != '무료' else 0

        # 기타
        row_template['rating'] = float(
            path_soup.find('span', attrs={"class": "_2KWt9f"}).text)
        row_template['is_package'] = False          # groom은 default가 False

        return row_template


    # tsv 파일 쓰기 -> String의 , 공백으로 tsv 저장 -> csv로 변경
    os.makedirs('./result/', exist_ok=True)
    f = open('./result/' + f'{now}_groomedu.csv', 'w', encoding='UTF-8')
    wr = csv.writer(f)
    wr.writerow(header)

    # 동기적으로 실행하기
    q = 1  # QueryString 초기화
    count = 1  # cmd counter
    while True:
        try:
            res = requests.get(
                f'https://edu.goorm.io/category/programming?page={q}&sort=newest')

            print(f'QueryString Page Change : {q}.')
            soup = BeautifulSoup(res.text, 'html.parser')
            link_list = [a['href'] for a in soup.select('a[href]')]
            # 구름에듀는 분야 - 백엔드 & 프론트 & 데엔이 나뉘어져 있지 않아, 분류 기준을 두고 전처리를 다시 해야할 것 같긴하다.
            i = 0
            for link in link_list:
                if link.startswith('/lecture/'):

                    # file 쓰기
                    value_list = list(parse_detail(ORIGIN_PATH + link).values())
                    wr.writerow(value_list)

                    #   추후에 log로 변경하기
                    print(f'[{count}] - {ORIGIN_PATH + link}')
                    count += 1
                    i += 1

            if i == 0:
                print("lecture Content가 더 이상 찾을 수 없습니다.")
                break
            q += 1

        except Exception as e:
            print('requests : ', e)
            break

    print('------구름에듀 - 저장이 완료되었습니다.------')
    f.close()  # 파일 종료

# 프로그래머스
def programmers_crawl():
    '''
    # 프로그래머스 크롤링
    ***
    link : https://school.programmers.co.kr/learn?page=1
    절차 :

    1. 태그 수집 작업 : 필터의 체크박스를 선택하고, 선택했을 때 나오는 강의의 태그에 체크박스 항목명을 추가한다.
        - Python 체크박스 클릭, Python 강의의 tags에 Python 추가
    2. 전체 강의의 데이터 수집 : 전체항목 페이지에서 페이지를 넘겨가며 항목의 상세 데이터를 가져온다.

    '''

    # 강의의 태그를 설정하기 위한 dict 선언
    # 강의 : [태그 리스트]
    courses = defaultdict(set)

    # 1. 태그 수집하기
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        driver.get("https://school.programmers.co.kr/learn")
        
        # 더보기 버튼 클릭
        more_btn = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[1]/div/div[2]/div[1]/div/div/button')
        more_btn.click()
        
        # 체크박스리스트 가져오기 (section1 : 언어, section2 : 난이도)
        lang_ul = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[1]/div/div[2]/div[1]/div/div/ul')
        level_ul = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[1]/div/div[2]/div[2]/div/div/ul')
        
        for i, ul in enumerate([lang_ul, level_ul]):
            ui_id = i + 1
            checkboxes = []
            for i in range(1, len(ul.find_elements(By.TAG_NAME, "li")) + 1):       
                checkbox = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[1]/div/div[2]/div[{ui_id}]/div/div/ul/li[{i}]/label')
                checkboxes.append(checkbox)

            # 하나씩 클릭하면서 가져오기
            for checkbox in checkboxes:
                
                # 체크하기
                checkbox.click()
                time.sleep(1)

                # 현재 체크한 항목명(tag) 가져오기
                tag = checkbox.text.lower()
                if ui_id == 2:
                    tag = tag[:3].strip() # 부제목 잘라주기

                # 페이지별로 탐색
                while True:  
                    time.sleep(1)

                    # 강의 없으면 패스
                    try:
                        driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/div')
                        break
                    except NoSuchElementException:
                        
                        # 강의 섹션
                        section = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]')
                        for si in range(1, len(section.find_elements(By.TAG_NAME, "a")) + 1):
                            course_title = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{si}]/div[2]/div[1]/h3').text
                            courses[course_title].add(tag)

                        # 다음 페이지 없으면 나가기
                        next_btn = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/div/button[3]')
                        if not next_btn.is_enabled():
                            break
                        else:
                            next_btn.click()

                # 체크 없애기
                checkbox.click()
                time.sleep(2)      
    print("태그 수집 완료")                          

    # 2. 전체 강의 가져오기
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        # 파일 쓰기
        f = open('./result/' + f'{now}_programmers.csv', 'w', encoding='UTF-8')
        cssWriter = csv.writer(f)
        cssWriter.writerow(header)
        
        # 프로그래머스 접속
        driver.get("https://school.programmers.co.kr/learn") 

        # 페이지별로 탐색
        while True:
            
            # 강의 섹션
            section = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]')
            for si in range(1, len(section.find_elements(By.TAG_NAME, "a")) + 1):
                
                # 모집 마감 제외
                try:
                    badge = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{si}]/div[2]/div[1]/div/span')
                    if badge.text == '모집 마감':
                        continue
                except NoSuchElementException:
                    badge = None
                course_btn = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{si}]')
                title = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{si}]/div[2]/div[1]/h3').text

                # 기본 강의정보 수집
                try:
                    price = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{si}]/div[2]/div[2]/div[1]/strong').text
                    price = price.replace("₩", "").replace(",", "")
                    price = 0 if price == "무료" else int(price)
                    is_free = price == 0
                except NoSuchElementException:
                    price = None
                try:
                    thumbnail_url = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{si}]/div[1]/img').get_attribute("src")
                except NoSuchElementException:
                    thumbnail_url = None
                try:
                    url = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{si}]').get_attribute("href")
                except NoSuchElementException:
                    url = None
                try:
                    rating = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{si}]/div[2]/div[2]/div[2]').text
                except NoSuchElementException:
                    rating = None
                
                # 상세 강의정보 수집
                course_btn.click()
                driver.implicitly_wait(3)
                
                # 수강생 수
                enrollment_count = None
                ul = driver.find_element(By.XPATH, '//*[@id="overview-fixed-menu"]/div/ul')
                for li in ul.find_elements(By.TAG_NAME, "li"):
                    if '명' in li.text:
                        enrollment_count = int(li.text[:li.text.index('명')].replace(',', ''))
                        break
                # 강사
                try:
                    instructor = driver.find_element(By.CLASS_NAME, "name").text
                except NoSuchElementException:
                    instructor = None
                
                if not instructor:
                    try:
                        instructor = driver.find_element(By.CLASS_NAME, "mentor-name").text
                    except NoSuchElementException:
                        instructor = None
                
                # 사이트 태그 추가
                courses[title].add('프로그래머스')

                row_template = dict.fromkeys(header)
                row_template['site'] = '프로그래머스'
                row_template['title'] = title
                row_template['instructor'] = instructor 
                row_template['description'] = ''
                row_template['url'] = url
                row_template['price'] = price
                row_template['tags'] = ','.join(courses[title])
                row_template['rating'] = rating
                row_template['thumbnail_url'] = thumbnail_url
                row_template['is_package'] = False
                row_template['is_free'] = price == 0
                row_template['enrollment_count'] = enrollment_count

                # 파일에 쓰기
                cssWriter.writerow(list(row_template.values()))
                driver.back()
            
            next_btn = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/div/button[3]')
            
            # 다음 페이지 없으면 끝
            if not next_btn.is_enabled():
                break
            next_btn.click()
            time.sleep(1)

        f.close()

    print('------프로그래머스 - 저장이 완료되었습니다.------')

# 인프런
def inflearn_crawl():
    Delay=2.5

    global driver
    global xpath

    course_data = []
    course_urls = []
    course_name = []
    course_rate = []
    course_tag = []
    course_thumbnail = []
    course_ins = []
    course_rev_cnt = []
    course_vat_price = []
    course_price = []
    course_is_free = []

    for page in range(1, 5): 
        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
            driver.get("https://www.inflearn.com/courses/it-programming?order=seq&page="+str(page))

            for element in driver.find_elements(By.CLASS_NAME, "course-data"):
                attrs = []
                for attr in element.get_property('attributes') :
                    attrs.append(attr['value'])
                course_data.append(attrs[1])
            # url
            for element in driver.find_elements(By.CLASS_NAME, "course_card_back"):
                aTag = element.find_element(By.CLASS_NAME, "e_course_click")
                url = aTag.get_attribute('href')
                course_urls.append(url)

            # thumbnail
            elements = driver.find_elements(By.CLASS_NAME, "card-image")
            for element in elements:
                try:
                    thumbnail = element.find_element(By.CLASS_NAME, "swiper-lazy").get_attribute('src')
                    course_thumbnail.append(thumbnail)
                except:
                    course_thumbnail.append('https://file.mk.co.kr/meet/neds/2022/05/image_readtop_2022_476589_16538895495059468.jpg')            

    # 수집
    for i, course in enumerate(course_data):         
        course_name.append(course[course_data[i].find('"course_title\":"')+16:course_data[i].find('","course_level":')])
        course_rate.append(course[course_data[i].find('"star_rate":')+12:course_data[i].find(',"review_count":')])
        cate = course[course_data[i].find('"second_category":"')+19:course_data[i].find('","skill_tag":')]
        lang = course[course_data[i].find('"skill_tag":"')+13:course_data[i].find('","seq0_instructor_id":')]
        level = course[course_data[i].find('"course_level":"')+16:course_data[i].find('","first_category":')]
        course_tag.append(','.join([cate, lang, level, '인프런']).replace(" · ", ",").lower())
        course_ins.append(course[course_data[i].find('"seq0_instructor_name":"')+24:course_data[i].find('","student_count":')])
        course_rev_cnt.append(course[course_data[i].find('"review_count":')+15:course_data[i].find(',"is_new_course":')])
        course_vat_price.append(course[course_data[i].find('"reg_vat_price":')+16:course_data[i].find(',"selling_price":')])
        price = course[course_data[i].find('"reg_price":')+12:course_data[i].find(',"reg_vat_price":')]
        course_price.append(course[course_data[i].find('"reg_price":')+12:course_data[i].find(',"reg_vat_price":')])
        course_is_free.append(True if price == 0 else False)

        
    # 데이터프레임
    # ['title', 'instructor', 'description', 'url', 'price', 'tags', 'category','rating', 'thumbnail_url', 'is_package', 'is_free', 'enrollment_count']
    raw_data = {'site': '인프런', 
                'title': course_name,
                'instructor': course_ins, 
                'description':'',
                'url': course_urls,
                'price': course_price, 
                'tags': course_tag, 
                'rating': course_rate,
                'thumbnail_url': course_thumbnail,
                'is_package': False,
                'is_free': course_is_free,
                'enrollment_count':0,
                }
    df=DataFrame(raw_data)
    df.to_csv('./result/' + f'{now}_inflearn.csv',index=False, encoding="utf-8-sig")#csv로 저장

    print('------인프런 - 저장이 완료되었습니다.------') 

def save_dataframe(df):

    def get_newtag(tag):
        if tag in tag_mapping:
            return tag_mapping[tag]
        else:
            return tag

    now = datetime.now().date()
    for _, row in df.iterrows():
        site = row['site']
        title = row['title']
        instructor = row['instructor']
        description = row['description']
        url = row['url']
        try:
            price = Decimal(row['price'])
        except InvalidOperation:
            price = Decimal('0.00')
        tags = row['tags']
        rating = row['rating']
        try:
            rating = round(Decimal(row['rating']), 3)
        except InvalidOperation:
            rating = Decimal('0.000')
        thumbnail_url = row['thumbnail_url']
        is_package = row['is_package']
        is_free = row['is_free']
        enrollment_count_str = row['enrollment_count']
        if enrollment_count_str == "" or enrollment_count_str == "0.0":
            enrollment_count = 0
        else:
            enrollment_count = int(float(enrollment_count_str))

        # Course 모델에 데이터 저장
        course = Course.objects.create(
            title=title,
            instructor=instructor,
            description=description,
            site=site,
            url=url,
            price=price,
            rating=rating,
            thumbnail_url=thumbnail_url,
            is_package=is_package,
            is_free=is_free,
            enrollment_count=enrollment_count,
        )
        for tag_name in tags.split(','):
            tag, _ = Tag.objects.get_or_create(name=get_newtag(tag_name.strip()))
            course.tags.add(tag)


def main():
    # 크롤링하여 result폴더에 결과파일 저장
    # goorm_crawl()
    # programmers_crawl()
    inflearn_crawl()

    # result 폴더에 있는 파일 읽으면서 데이터 저장
    path = './result/*.csv'
    data = []
    files = glob.glob(path)

    for file in files:
        # 각 파일의 헤더 행을 지정하여 파일을 읽어옵니다.
        df = pd.read_csv(file)  # 헤더가 없는 경우
        df['tags'] = df['tags'].fillna('')
        data.append(df)
        save_dataframe(df)
    
    result = pd.concat(data)

    # 통합파일 저장
    result.to_csv('./result/' + f'{now}_devcombine.csv',index=False, mode='w',encoding="utf-8-sig")


import os
# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록한다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만든다.
django.setup()

from courses.models import Course, Tag


if __name__ == '__main__':
    main()
    