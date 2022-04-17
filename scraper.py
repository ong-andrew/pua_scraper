from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import os
import shutil
from webdriver_manager.chrome import ChromeDriverManager



options = Options()
# options.binary_location = "/usr/bin/google-chrome-stable"    #chrome binary location specified here
options.add_argument("--headless") #open Browser in maximized mode
options.add_argument("--no-sandbox") #bypass OS security model
options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path='/home/island/Documents/PyCharm/Selenium/chromedriver')
print(datetime.now().strftime("[%H:%M:%S] ") + "Starting Chrome")
driver.get("https://lom.agc.gov.my/subsid.php?type=pua")
print(datetime.now().strftime("[%H:%M:%S] ")+"Waiting for website to load")
sleep(20)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')
print(datetime.now().strftime("[%H:%M:%S] ")+"Soup created")
with open('test.html',"w") as html:
    html.write(str(soup))

table = soup.find(lambda tag: tag.name=='tbody')
rows = table.findAll(lambda tag: tag.name=='tr')

gazettes = []
links = []

for row in rows:
    x = row.findAll('td')
    gazettes.append(x[2].text)
    link = str(row.findAll('a')[-1]).split("\" target")[0].replace("<a href=\"../../../","https://lom.agc.gov.my/").replace(" ","%20")
    links.append(link)
print(datetime.now().strftime("[%H:%M:%S] ")+"Creating names of gazette and pdf links")

new_txt = ""
for gazette,link in zip(gazettes, links):
    new_txt += gazette + "\n"
    new_txt += link + "\n\n"
with open('new.txt',"w") as write:
    write.write(new_txt)
print(datetime.now().strftime("[%H:%M:%S] ")+"Writing to new.txt")

driver.quit()
os.system('pkill chrome')
