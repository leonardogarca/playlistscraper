from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from sys import argv

url = ""

try:
    url = argv[1]
except IndexError:
    url = input("type your link: ")

#Setting up driver and fully loading the webpage
opts = Options()
opts.add_argument('--headless')
driver = webdriver.Chrome('chromedriver', options=opts)
driver.maximize_window()
driver.get(url)
while True:
    scroll_height = 2000
    driver.implicitly_wait(3)
    html_before = driver.page_source
    document_height_before = driver.execute_script("return document.documentElement.scrollHeight")
    driver.execute_script(f"window.scrollTo(0, {document_height_before + scroll_height});")
    document_height_after = driver.execute_script("return document.documentElement.scrollHeight")
    if html_before == driver.page_source:
        break

#Playlist title for output csv
playlist_title = driver.title

#Get every element that points to a video
div_elements = driver.find_elements(By.TAG_NAME, "ytd-playlist-video-renderer")
videos = []
for div in div_elements:
    video = div.find_element(By.TAG_NAME, 'h3')
    title = video.find_element(By.TAG_NAME, 'a')
    videos.append([title.get_attribute('title'), title.get_attribute('href')])

#Output to csv
f = open((playlist_title + '.csv'), 'w', encoding='utf-8')
f.write("title, link\n")
for video in videos:
    f.write("\"" + video[0] + "\"," + video[1] + "\n")
driver.close()
