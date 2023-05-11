# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver
from selenium.webdriver.common.by import By
# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time

def infinite_loop(driver):
    # 최초 페이지 스크롤 설정
    # 스크롤 시키지 않았을 때의 전체 높이
    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # 윈도우 창을 0에서 위에서 설정한 전체 높이로 이동
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1.0)
        # 스크롤 다운한 만큼의 높이를 신규 높이로 설정
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        # 직전 페이지 높이와 신규 페이지 높이 비교
        if new_page_height == last_page_height:
            time.sleep(1.0)
            # 신규 페이지 높이가 이전과 동일하면, while문 break
            if new_page_height == driver.execute_script("return document.documentElement.scrollHeight"):
                break
        else:
            last_page_height = new_page_height



# 크롬드라이버 경로

driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver")

# 검색할 값 입력
context = '대구 반려동물미용'
#크롬 드라이버에 url 주소 넣고 실행
driver.get('https://map.naver.com/v5/search/'+context+'?c=15,0,0,0,dh')

# 페이지가 완전히 로딩되도록 3초동안 기다림
time.sleep(3)
# 웹 드라이버도 기다림
driver.implicitly_wait(3)

#  검색하고나서 가게정보창이 바로 안뜨는 경우 고려해서 무조건 맨위에 가게 링크 클릭하게 설정
driver.switch_to.frame('searchIframe')
driver.implicitly_wait(3)

# 메뉴표에 있는 텍스트 모두 들고옴(개발자 도구에서 그때그때 xpath 복사해서 들고오는게 좋다
temp = driver.find_element(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul')
driver.implicitly_wait(20)  # selenium에서 가끔씩 태그 시간내에 못찾는 경우 때문에 일부러 길게 설정해놓음

button = temp.find_elements(By.TAG_NAME, 'a')
driver.implicitly_wait(20)

# 여기서 send_keys를 통해 해당 가게 선택
if '이미지수' in button[0].text or button[0].text == '':  # 가게 정보에 사진이 있는경우
    button[1].send_keys(Keys.ENTER)
else:  # 사진이 없는 경우
    button[0].send_keys(Keys.ENTER)

driver.implicitly_wait(3)
time.sleep(3)

# frame이 이상하게 넘어가는 경우 방지를 위해 원래 frame으로 변경한 후에 이동
driver.switch_to.default_content()

# 메뉴정보가 entryIframe에 있기 때문에 frame 변경함
driver.switch_to.frame('entryIframe')
driver.implicitly_wait(2)


# ---- title을 얻어오는 -----
title = driver.find_element(By.CLASS_NAME, 'Fc1rA')
print(title.text)
# --------------------------


# ---- place를 얻어오는 ----
place = driver.find_element(By.CLASS_NAME, 'LDgIH')
print(place.text)
# --------------------------


# ---- 요일 정보를 읽어오는 ----
temp = driver.find_element(By.XPATH, "//div[contains(@class, 'O8qbU')][contains(@class, 'pSavy')]") # 클래스 2개 이상
# 더보기 란 클릭
button = temp.find_element(By.TAG_NAME, 'a')
button.send_keys(Keys.ENTER)


day_list = temp.find_elements(By.CLASS_NAME, 'i8cJw')
time_list = temp.find_elements(By.CLASS_NAME, 'H3ua4')

# 요일별로 저장하기 위해 딕셔너리 생성
schedule = {}

# 가게별로 운영일이 다를 수 있기 때문에 설정
for i in range (len(day_list)):
    day = day_list[i].text
    oc_time = time_list[i].text
    print(day, oc_time)
    schedule[day] = oc_time

print(schedule)
#-------------------


# ---- 전화번호를 가져오는 ----
temp = driver.find_element(By.XPATH, "//div[contains(@class, 'O8qbU')][contains(@class, 'nbXkr')]") # 클래스 2개 이상
phone = temp.find_element(By.CLASS_NAME, 'xlx7Q')
print(phone.text)


