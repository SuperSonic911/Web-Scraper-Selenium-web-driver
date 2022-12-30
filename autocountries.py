from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import json


f = open("countriesDict.txt", "w") #create clean text to save dict 
f.write("{\n")
f.close() 
#add all countries to an array
with open("countries.txt") as f:
    countries_array = []
    while True:
        line = f.readline()
        if not line:
            break
        countries_array.append(line.strip())

driver = webdriver.Chrome("chromedriver.exe")   #included in the same foler
driver.get("https://globalsolaratlas.info/map") #opens window with line


try:
    searchbar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-0")))
except:
    driver.quit()

countriesDict = {}


for country in countries_array:
    searchbar = driver.find_element(By.ID, "mat-input-0")  #look for search bar
    searchbar.clear() #ensure search bar is empty 
    searchbar.send_keys(country)   #type country name into the search bar
    time.sleep(5)
    searchbar.send_keys(Keys.ARROW_DOWN)  #arrow down to select first country
    searchbar.send_keys(Keys.RETURN)     #press enter

    time.sleep(5)
    print("")
    isarray = False
    
    #we put it in this try except because if we don't find it, we skip it and keep going
    try:
        #per day or per year button
        button = driver.find_element(By.XPATH ,"/html/body/gsa-app/div/div/main/ng-component/section/gsa-map-sidebar/aside/div/gsa-map-sidebar-site/gsa-section[1]/section/div[3]/gsa-card/div/div/span")
        button.click()
        time.sleep(5)
        #click per day
        button = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div/button[1]')
        button.click()
        time.sleep(5)
    except NoSuchElementException:
        isarray = True
    
    if isarray == False:  #there is only one value for dni and temp 
        #dni element                         
        dni = driver.find_element(By.XPATH, '/html/body/gsa-app/div/div/main/ng-component/section/gsa-map-sidebar/aside/div/gsa-map-sidebar-site/gsa-section[1]/section/div[3]/gsa-card/div/gsa-site-data/mat-list/mat-list-item[2]/div/gsa-site-data-item/div/div[4]')
        dni = dni.text

        #temp element
        temp = driver.find_element(By.XPATH, "/html/body/gsa-app/div/div/main/ng-component/section/gsa-map-sidebar/aside/div/gsa-map-sidebar-site/gsa-section[1]/section/div[3]/gsa-card/div/gsa-site-data/mat-list/mat-list-item[7]/div/gsa-site-data-item/div/div[4]")
        temp = temp.text
    else:  #there are two values for temp and dni, which means we must treat it as an array
        dni = driver.find_elements(By.XPATH, "/html/body/gsa-app/div/div/main/ng-component/section/gsa-map-sidebar/aside/div/gsa-map-sidebar-area/gsa-section[1]/section/div[3]/gsa-card/div/gsa-area-data/mat-list/mat-list-item[2]/div/gsa-area-data-item/div/div[4]")
        dni = dni[0].text

        temp = driver.find_elements(By.XPATH, "/html/body/gsa-app/div/div/main/ng-component/section/gsa-map-sidebar/aside/div/gsa-map-sidebar-area/gsa-section[1]/section/div[3]/gsa-card/div/gsa-area-data/mat-list/mat-list-item[7]/div/gsa-area-data-item/div/div[4]")
        temp = temp[0].text

    countriesDict[country] = {"dni":dni, "temp":temp}
    print(countriesDict[country])

    f = open("countriesDict.txt", "a")
    f.write(f'"{country}":{countriesDict[country]}, \n')
    

f.write("}")
f.close()