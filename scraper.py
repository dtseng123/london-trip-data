import requests 
from bs4 import BeautifulSoup
import csv 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import argparse
import base64
# clear
pathToStoreInfo = "london_restaurants.csv"
STARTURL = "https://www.tripadvisor.com/Restaurants-g186338-oa30-London_England.html"
# python3 scraper.py -m -i --url "https://www.tripadvisor.com/Restaurants-g186338-oa4920-London_England.html\#EATERY_LIST_CONTENTS"
# https://www.tripadvisor.com/Restaurants-g186338-oa12437-London_England.html\#EATERY_LIST_CONTENTS
def scrapeRestaurantsUrls(tripURLs):
    urls =[]
    for url in tripURLs:
        page = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
        soup = BeautifulSoup(page.text, 'html.parser')
        results = soup.find('div', class_='YtrWs') # data-test-target="restaurants-list"
        stores = results.find_all('div', class_='YHnoF Gi o')  #data-test="3_list_item" 
 
        # print("stores ",stores)
        for store in stores:
            unModifiedUrl = str(store.find('a', href=True)['href'])
            urls.append('https://www.tripadvisor.com'+unModifiedUrl)      
    # print('URLS',urls)      
    return urls

def scrapeRestaurantInfo(url):
    details = []
    storeName=""
    page = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
    soup = BeautifulSoup(page.text, 'html.parser')

    if soup.find('h1', class_='HjBfq') is not None:
        storeName = soup.find('h1', class_='HjBfq').text
        print(storeName)

    # allInfo = soup.find_all('div', class_= 'vQlTa H3')
    allInfo = soup.find_all("span", class_="DsyBj cNFrA")
    
    website =''
    storeAddress= ''
    phoneNum =''
    website=''
    cuisines=''
    meals = ''
    features = ''

    for info in allInfo:
        if info.find('a', href=True, class_="AYHFM") is not None:
        
            unModifiedUrl = str(info.find('a', href=True, class_="AYHFM")['href'])
            # ADDRESS
            if unModifiedUrl == "#MAPVIEW":
                storeAddress = info.find('a', href=True, class_="AYHFM").text.strip()
                details.append(storeAddress)
            
        if info.find('a', class_="YnKZo Ci Wc _S C AYHFM") is not None:
            codedLink = str(info.find('a',  class_="YnKZo Ci Wc _S C AYHFM")['data-encoded-url'])
            decoded = base64.b64decode(codedLink)
            website = decoded.decode()
            link = website.split('//')[1]
            website = "http://" + link.split("_")[0]  
            details.append(website)

        if info.find('span', class_="AYHFM"):
            phoneNum = info.find('a', class_='BMQDV _F G- wSSLS SwZTJ').text.strip()
            details.append(phoneNum)   

    mealDetails = soup.find_all('div', class_="SrqKb")
 
    if 0  < len(mealDetails):
        cuisines =  mealDetails[0].text.strip()
 
    if 1  < len(mealDetails):
        meals = mealDetails[1].text.strip()
    
    if 2  < len(mealDetails):
        features = mealDetails[2].text.strip()
 

    print(details)
  
    with open(pathToStoreInfo, mode='a', encoding="utf-8") as trip:
        data_writer = csv.writer(trip, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        data_writer.writerow([storeName, storeAddress, phoneNum, website, cuisines, meals, features])


def scrape(urls):
    global STARTURL 
    count = 0
    currentManyUrls = len(urls)
    driver = webdriver.Chrome('chromedriver')
    for url in urls:
        #if you want to scrape restaurants info
        if info == True:
            scrapeRestaurantInfo(url)
            count = count + 1
            print('count', count)
            if count == currentManyUrls:  
                   
                driver.get(STARTURL)
                page = requests.get(STARTURL, headers={'User-Agent': "Mozilla/5.0"})
                soup = BeautifulSoup(page.text, 'html.parser')
 
                unModifiedUrl = str(soup.find('a', class_ = 'nav next rndBtn ui_button primary taLnk', href=True)['href'])
                STARTURL = 'https://www.tripadvisor.com' + unModifiedUrl
               
                print("NEXT URL", STARTURL)

                urls = scrapeRestaurantsUrls([STARTURL])
                driver.quit()
                scrape(urls)

parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True, help ='need starting url')
parser.add_argument('-i', '--info', action='store_true', help="Collects restaurant's info")
parser.add_argument('-m', '--many', action='store_true', help="Collects whole area info")
args = parser.parse_args()

startingUrl = args.url 

if args.info:
    info = True
else:
    info = False
if args.many:
    
    urls = scrapeRestaurantsUrls([startingUrl])
    scrape(urls)
    
else:
    urls = [startingUrl]
