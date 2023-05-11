# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver
from selenium.webdriver.common.by import By
# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time



# 크롬드라이버 경로

driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver")

# 검색할 값 입력
context = '대구 반려동물미용'
#크롬 드라이버에 url 주소 넣고 실행
driver.get('https://map.naver.com/v5/search/'+context+'?c=15,0,0,0,dh')

while True:
    # 페이지가 완전히 로딩되도록 3초동안 기다림
    time.sleep(3)
    # 웹 드라이버도 기다림
    driver.implicitly_wait(3)

    #  검색하고나서 가게정보창이 바로 안뜨는 경우 고려해서 무조건 맨위에 가게 링크 클릭하게 설정
    driver.switch_to.frame('searchIframe')
    driver.implicitly_wait(3)

    # ----------  list를 끝까지 scroll --------------

    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.click()
    for i in range(100):
            time.sleep(0.1)
            body.send_keys(Keys.PAGE_DOWN)
    # ------------------------------------------------


    # 메뉴표에 있는 텍스트 모두 들고옴(개발자 도구에서 그때그때 xpath 복사해서 들고오는게 좋다
    temp = driver.find_element(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul')
    driver.implicitly_wait(20)  # selenium에서 가끔씩 태그 시간내에 못찾는 경우 때문에 일부러 길게 설정해놓음

    # list들을 모두 가져옴
    lists = temp.find_elements(By.CLASS_NAME, 'qbGlu')

    # list에 있는 객체들 수 만큼 반복 ****

    for index in range(len(lists)):
        button = lists[index].find_elements(By.TAG_NAME, 'a')
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


        # ----  (1) title을 얻어오는 -----
        title = driver.find_element(By.CLASS_NAME, 'Fc1rA')
        print(title.text)
        # --------------------------


        # ---- (2) place를 얻어오는 ----
        place = driver.find_element(By.CLASS_NAME, 'LDgIH')
        print(place.text)
        # --------------------------


        # ---- (3) 요일 정보를 읽어오는 ----
        try:    # 요일 정보가 있을 경우
            temp = driver.find_element(By.XPATH, "//div[contains(@class, 'O8qbU')][contains(@class, 'pSavy')]") # 클래스 2개 이상
            # 더보기 란 클릭
            try:    # 더보기란이 있는 경우
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
            except:
                days = temp.find_element(By.CLASS_NAME, 'U7pYf')
                day = '매일'
                oc_time = days.text
                print(day, oc_time)
                schedule[day] = oc_time

        except: # 요일 정보가 아예 없는 경우
            day = '요일정보'
            oc_time = '없음'
            print(day, oc_time)
            schedule[day] = oc_time


        print(schedule)
        #-------------------


        # ---- (4) 전화번호를 가져오는 ----
        try:
            temp = driver.find_element(By.XPATH, "//div[contains(@class, 'O8qbU')][contains(@class, 'nbXkr')]") # 클래스 2개 이상
            phone = temp.find_element(By.CLASS_NAME, 'xlx7Q')
            phone = phone.text
        except:
            phone = '전화번호 없음'

        print(phone)
        # -------------------

        # ---- (5) 리뷰 정보들을 가져오는 ----
        try :   # 리뷰 담는 객체가 있다면 ok
            temp = driver.find_element(By.CLASS_NAME, 'dAsGb')
            reviews = temp.find_elements(By.TAG_NAME, 'em')

            rate = -1.0

            if len(reviews) == 1: # 방문자 리뷰만 있는 경우
                visitor_review = reviews[0].text
                blog_review = '0'
            elif len(reviews) == 2: # 방문자 리뷰, 블로그 리뷰 2개 있는 경우
                # 별점, 방문자 리뷰 2개일수도 있음
                try:    # int형 = 방문자수
                    int(reviews[0].text)    # int화가 안되면
                    visitor_review = reviews[0].text
                    blog_review = reviews[1].text
                except: # float형 = 별점
                    rate = float(reviews[0].text)
                    visitor_review = reviews[1].text
                    blog_review = '0'
            elif len(reviews) == 3: # 별점 , 방문자 리뷰, 블로그 리뷰 3개 있는 경우
                rate = float(reviews[0].text)
                visitor_review = reviews[1].text
                blog_review = reviews[2].text


        except :   # 리뷰가 하나도 없다면
            rate = -1.0
            visitor_review = '0'
            blog_review = '0'

        if rate < 0 :
            star_rate = '별점이 없습니다.'
        elif rate > 0 :
            star_rate = str(rate)

        print(f'별점 : {star_rate}, 방문자 리뷰 : {visitor_review}, 블로그 리뷰 : {blog_review}')
        # -------------------

        # ---- (6) 가게의 상세 페이지를 가져오는 ----
        homepage = ''

        try:    # 주소에 하나의 주소라도 존재할 경우
            temp = driver.find_element(By.XPATH, "//div[contains(@class, 'O8qbU')][contains(@class, 'yIPfO')]")  # 클래스 2개 이상
            hompage_element = temp.find_elements(By.TAG_NAME, 'a')
            homepage = hompage_element[0].text

        except:
            homepage = '블로그 / 인스타그램 준비중입니다.'
        # ----------------------

        print(f'홈페이지 주소는 : {homepage}')


        # (final step) * 다음 게시물 클릭을 위해, 원래 프레임으로 돌아가기
        driver.switch_to.default_content()
        driver.switch_to.frame('searchIframe')

    # 모든 것들을 [50개] 크롤링했다면, 다음 페이지로 이동해야함!
    temp = driver.find_element(By.CLASS_NAME, 'zRM9F')

    try:  # 만약 왼쪽 끝이거나, 오른쪽 끝이라면
        invalid_button = temp.find_element(By.CLASS_NAME, 'Y89AQ ')  # -> 이 값이 찾아져야함
        valid_buttons = temp.find_elements(By.CLASS_NAME, 'eUTV2 ')
        if invalid_button.text == '이전페이지':  # 이전페이지 값이 없다면
            my_button = valid_buttons[1]
        elif invalid_button.text == '다음페이지':  # 크롤링이 끝났다는 것임
            print('crawling 끝..')
            break
    except:  # 왼쪽 끝도 아니고, 오른쪽 끝도 아닐 경우
        valid_buttons = temp.find_elements(By.CLASS_NAME, 'eUTV2')
        my_button = valid_buttons[1]

    # 다음 페이지 클릭
    my_button.send_keys(Keys.ENTER)
    driver.switch_to.default_content()


