from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import requests
from urllib.parse import urlsplit
from urllib.parse import unquote

# 검색어와 저장할 디렉토리 설정
search_term = "site:https://www.leagueoflegends.com/ko-kr/"
save_dir = "downloaded_images"

# 디렉토리 생성
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Selenium WebDriver 설정
driver = webdriver.Chrome()  # 크롬 드라이버 경로가 환경 변수에 설정되어 있어야 합니다
driver.get(f"https://www.google.com/search?tbm=isch&q={search_term}")

# 페이지가 로드될 시간을 기다림
time.sleep(2)

# 스크롤 다운을 통해 더 많은 이미지를 로드
elem = driver.find_element_by_tag_name("body")
for i in range(5):  # 스크롤 다운 횟수
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

# 이미지 요소 선택
thumbnails = driver.find_elements_by_css_selector("img.rg_i")

# 이미지 URL 수집 및 다운로드
for idx, thumbnail in enumerate(thumbnails):
    try:
        thumbnail.click()
        time.sleep(1)
        img_url = driver.find_element_by_css_selector("img.n3VNCb").get_attribute("src")
        
        if img_url.startswith("http"):
            img_data = requests.get(img_url).content
            img_name = os.path.join(save_dir, f"image_{idx+1}.jpg")
            with open(img_name, 'wb') as handler:
                handler.write(img_data)
            print(f"Downloaded {img_name}")
    except Exception as e:
        print(f"Failed to download image {idx+1}: {e}")

driver.quit()
