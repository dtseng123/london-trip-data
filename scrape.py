import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
pages_to_scrape = 3
url = "https://www.tripadvisor.com/Restaurants-g186338-London_England.html"
# https://www.tripadvisor.com/Restaurants-g186338-London_England.html
path_to_file = "./london_restaurants.csv"
# >>> import scrapy_gui
# >>> scrapy_gui.open_browser()
# import the webdriver
driver = webdriver.Safari()
driver.get(url)

# open the file to save the review
csvFile = open(path_to_file, 'a', encoding="utf-8")
csvWriter = csv.writer(csvFile)


# change the value inside the range to save the number of reviews we're going to grab
for i in range(0, pages_to_scrape):

    # give the DOM time to load
    time.sleep(3) 
    # Click the "expand review" link to reveal the entire review.
    driver.find_element(by=By.XPATH, value=".//div[contains(@data-test-target, 'expand-review')]").click()


    # Now we'll ask Selenium to look for elements in the page and save them to a variable. First lets define a  container that will hold all the reviews on the page. In a moment we'll parse these and save them:
    container = driver.find_element(by=By.XPATH, value="//div[@data-reviewid]")
    driver.implicitly_wait(4)

    # Next we'll grab the date of the review:
    dates = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div[9]/div/div[1]/div[1]/div/div/div[3]/div[3]/div[2]/div[3]/div[2]/span[1]')

   # Now we'll look at the reviews in the container and parse them out

    for j in range(len(container)): # A loop defined by the number of reviews

        # Grab the rating
        rating = container[j].find_element(by=By.XPATH, value=".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class").split("_")[3]

        # Grab the title
        title = container[j].find_element(by=By.XPATH, value=".//div[contains(@data-test-target, 'review-title')]").text

        #Grab the review
        review = container[j].find_element(by-By.XPATH, value=".//q[@class='IRsGHoPm']").text.replace("\n", "  ")

        #Grab the data
        date = " ".join(dates[j].text.split(" ")[-2:])
        
        #Save that data in the csv and then continue to process the next review
        csvWriter.writerow([date, rating, title, review]) 
        
    # When all the reviews in the container have been processed, change the page and repeat            
    driver.find_element(by=By.XPATH,value='.//a[@class="ui_button nav next primary "]').click()

# When all pages have been processed, quit the driver
driver.quit()
