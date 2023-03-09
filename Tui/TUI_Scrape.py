from selenium import webdriver
import datetime
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager 
import json
import csv


# open the file in the write mode
f = open('C:\\Users\\hanno\\Desktop\\tui2.csv', 'w')

# create the csv writer
writer = csv.writer(f)
header = ['Price',"FlightNumber", 'Date of Departure','Date of Arrival','Available seats', 'Arrival Airport code', 'Arrival Airport name', "Departure Airport code", "Departure Airport name","Flight Duration","Scraping date"]
writer.writerow(header)
# close the file
f.close()

#Prepare for-loop with data
OriginArray=["BRU","CRL"]
DestinationArray=["CFU","HER","RHO","BDS","NAP","PMO","FAO","ALC","IBZ","AGP","PMI","TFS"]
startDate = datetime.datetime(2023,4,1)
Days = []
for i in range(0,31):
    Days.append(startDate)
    startDate = startDate + datetime.timedelta(days = 7) 
arrayPages = []

for DayLoop in Days:
    for DestinationLoop in DestinationArray:
        k = open('C:\\Users\\hanno\\Desktop\\tui2.csv', 'a')
        writer2 = csv.writer(k)
        DateOut=DayLoop.strftime("%Y-%m-%d")
        Destination=DestinationLoop

        PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

        url = "http://www.tuifly.be/flight/nl/"


        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_argument('--ignore-certificate-errors')
        driver_service = Service(executable_path=PATH)
        driver = webdriver.Chrome(service=driver_service,options=options)
        driver.maximize_window()
        driver.implicitly_wait(25)
        driver.get(url)

        driver.find_element(By.CSS_SELECTOR, "#cmCloseBanner").click()


        element = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#page div.container footer > script"))
        ) 

        url = f"http://www.tuifly.be/flight/nl/search?flyingFrom%5B%5D=CRL&flyingTo%5B%5D={Destination}&depDate={DateOut}&adults=1&children=0&childAge=&choiceSearch=true&searchType=pricegrid&nearByAirports=true&currency=EUR&isOneWay=true"

        driver.get(url)

        data = driver.execute_script("return JSON.stringify(searchResultsJson)")
        json_object = json.loads(data)
        flightviewdata = json_object["flightViewData"]
        if(len(flightviewdata) != 0):
            for item in flightviewdata:
                flightData = [item["totalPrice"],f'{item["flightsectors"][0]["carrierCode"]} {item["flightsectors"][0]["flightNumber"]}',f'{item["journeySummary"]["departDate"]}T{item["journeySummary"]["depTime"]}',f'{item["journeySummary"]["arrivalDate"]}T{item["journeySummary"]["arrivalTime"]}',item["journeySummary"]["availableSeats"],item["journeySummary"]["arrivalAirportCode"],item["journeySummary"]["arrivalAirportName"],item["journeySummary"]["departAirportCode"],item["journeySummary"]["departAirportName"],item["journeySummary"]["totalJnrDuration"],datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')]
                print(flightData) 
                if (item["journeySummary"]["departAirportCode"] == "BRU" or item["journeySummary"]["departAirportCode"] == "CRL"):
                    writer2.writerow(flightData)
                    print(f"wrote {flightData} to CSV")

        driver.close()
        k.close()


