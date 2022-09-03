'''
Created on 12 Aug 2022
Use this page to scrape the probability data from fplreview using selenium. 
It should mimic the functionality on ReadCSV. Once complete ReadCSV can be deprecated
@author: stefanosilva
'''
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def loadFPLReview():
    PATH = '/Users/stefanosilva/Documents/GitHub/FPL-Python/Python Workspace/FPL Analysis/chromedriver'
    driver = webdriver.Chrome(PATH)
    driver.get('https://fplreview.com/raw-free-model-data/')
    return driver

def closeBrowser(driver):
    try:
        driver.quit()
    except:
        print("driver already closed")
        
        
    
 
'''    
Returns a list contain all data for each gw that is available
returns a mult-d list. Each list will contain the cleansheet/assist/goal data for a gameweek. E.g.
[[gw1CSData],...,[gw5CSData]]
gw1CSData = [['Man City', 'BOU', 'H', '56%'],...,["Nott'm Forest", 'WHU', 'H', '20%']]
need to append gw to each gwXCSData
''' 
def scrapeAllData(driver, dataType):

    try:
        WebDriverWait(driver,30).until(
            EC.presence_of_element_located((By.ID,'myGW'))
            )
        
        selectProabilityTypeDropDown(driver, dataType)
                
        WebDriverWait(driver,5).until(
            EC.element_to_be_clickable((By.XPATH, "//select[@id='myGW']/option"))
            )
        gws = driver.find_elements(By.XPATH, "//select[@id='myGW']/option")
        
        gwsdata = [] #contains data for each gw
        
        # iterate through each gw
        for gw in gws:
            rows = [] #contains data for each row in CS GW table
            WebDriverWait(driver,5).until(EC.element_to_be_clickable(gw))
            g = gw.text
            gw.click()
            allRows = driver.find_elements(By.XPATH,"//tr[@class='normsp']")
            l = len(allRows)
            # iterate through each row in table
            for i in range(1,l+1):
                row = [] #contains individual column data to be stored in cs
                i = str(i)
                probData = driver.find_elements(By.XPATH, "//tr[@class='normsp']["+i+"]/td")
                # iterate though each column in row
                for data in probData:
                    row.append(data.get_attribute('textContent'))
                row.insert(0,g)
                rows.append(row)
                
            gwsdata.append(rows)
        # print(gwsdata)
        

    except:
        print('test2')
        driver.quit()
        
    
    return gwsdata
        
def selectProabilityTypeDropDown(driver, probType):
    
    if probType.lower() == 'cs':
        xpath = "//select[@class='myType']/option[1]"
        
    elif probType.lower() == 'scorer':
        xpath = "//select[@class='myType']/option[2]"
    elif probType.lower() == 'assist':
        xpath = "//select[@class='myType']/option[3]"
    else:
        print("couldnt find the drop down - quitting driver")
        
        
    try:
        elements = WebDriverWait(driver,5).until(
            EC.element_to_be_clickable((By.XPATH,xpath))
            )
        elements.click()
        
    except:
        print("Unable to locate element")
    
      
'''
returns a mult-d list. Each list will contain the cleansheet data for a gameweek. E.g.
[[gw1CSData],...,[gw2CSData]]
gw1CSData = [['Man City', 'BOU', 'H', '56%'],...,["Nott'm Forest", 'WHU', 'H', '20%']]
need to append gw to each gwXCSData
'''

# ' GW3'
def getAllProbabilityData():
    driver = loadFPLReview()
    
    csData = scrapeAllData(driver, 'cs')
    goalData = scrapeAllData(driver, 'scorer')
    assistData = scrapeAllData(driver, 'assist')
    
    closeBrowser(driver)
    
    allData = [csData,goalData,assistData]
    
    return allData



# a = getAllProbabilityData()
# print(a)