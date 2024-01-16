from selenium import webdriver #This code is implemented to handle one professor. Others to be implemented soon
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import numpy as np
import re
import pandas as pd
import gender_guesser.detector as gender
d = gender.Detector()
#Get the adblocker 
ad_block_path = r"\Users\aikob\Downloads\GIGHMMPIOBKLFEPJOCNAMGKKBIGLIDOM_5_16_0_0.crx"
chrome_options = Options()
chrome_options.add_extension(ad_block_path)
#get the allprofessors link
driver = webdriver.Chrome(options=chrome_options)
all_prof = "https://www.ratemyprofessors.com/search/professors/1072?q=*"
driver.get(all_prof)
#click on the show more button x amount of times 
num_profs_blerb = driver.find_element(by ="xpath", value="//h1[@data-testid='pagination-header-main-results']").text
pat = r'\d+'
num_profs = int(re.findall(pat, num_profs_blerb)[0])
#Define review counter 
def counter_maker(n): 
    if n%8==0: 
        counter = n//8 - 1
    else:
        counter = n//8
    return counter
tracker = counter_maker(num_profs)
if num_profs>8: 
    for i in np.arange(0,tracker):
        load_more = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Show More']")))
        load_more.click()
#define collect review function 
def collect_review(review):
    ratings = review.find_elements(by = "xpath", value = './/div[starts-with(@class, "CardNumRating__CardNumRatingNumber")]')
    quality, difficulty = ratings[0].text, ratings[1].text
    comments = review.find_element(by="xpath", value='.//div[starts-with(@class, "Comments__StyledComments")]').text
    time_stamp = review.find_element(by="xpath", value='.//div[starts-with(@class, "TimeStamp")]').text
    return [name,id,gen,department,quality,difficulty, comments,time_stamp]
#define load more professor reviews 
def load_more_counter(n):
    extra = n-20
    if extra%10==0:
        count = extra//10
    elif extra%10>0: 
        count = extra//10+1
    return count
#gather a professor cards 
cards = driver.find_elements(by="xpath", value='//a[contains(@class, "TeacherCard__StyledTeacherCard")]')
#no rating check 
get_rating = driver.find_elements(by= "xpath", value = '//div[contains(@class,"CardNumRating__CardNumRatingCount")]')
rating_text = [int(float(i.text.split(" ")[0])) for i in get_rating]
#get professor urls 
urls = list(map(lambda card : card.get_attribute('href'), cards))
#make output datframe 
columns = ["Professor Name","Professor ID","Professor Gender","Department","Quality","Difficulty","Comments", "Time Stamp"]
output_df = pd.DataFrame(columns=columns)
#big loop: (testing on american studies department)
exception_count  = 0
for i in range(len(urls)):
    if rating_text[i] == 0:
        continue
    else:
        try:
            driver.get(urls[i])
            #click open all reviews 
            num_ratings = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='#ratingsList']")))
            num_ratings = num_ratings.text
            just_num = int(num_ratings.split(" ")[0])
            counter = load_more_counter(just_num)
            if just_num>20:
                for i in np.arange(0,counter):
                    load_more = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Load More Ratings']")))
                    load_more.click()
            #get general info
            pat = r'\d+'
            id = re.findall(pat, urls[i])[0]
            name = driver.find_element(by= "xpath",value ="//div[@class='NameTitle__Name-dowf0z-0 cfjPUG']").text
            department = driver.find_element(by= "xpath",value ='//a[@class="TeacherDepartment__StyledDepartmentLink-fl79e8-0 iMmVHb"]').text
            gen = d.get_gender(name.split(" ")[0])
            #get review data
            all_reviews = driver.find_elements(by = "xpath", value='.//div[starts-with(@class, "Rating__RatingBody")]')
            mapped = map(collect_review,all_reviews)
            map_df = pd.DataFrame(mapped,columns=columns)
            output_df = pd.concat([output_df, map_df], sort=False)
        except TimeoutException:
            print("Encountered TimeOut Exception, moving onto next professor")
            exception_count = exception_count + 1
            continue
#Accuracy checks 
actual_profs = len(output_df["Professor Name"].unique())
zeroes = sum(1 for item in rating_text if item == 0)  
true_profs = len(urls) - (zeroes+exception_count)
csv_file_path = r"C:\Users\aikob\OneDrive\Documents\RMP Project\all_prof.csv" 
output_df.to_csv(csv_file_path, index=False)


#12/24 problems - randomly skipping ppl and getting stuck on timeout errors 
#random coding 
five_stars = output_df[output_df["Quality"]=="5.0"]["Professor Name"].unique()
