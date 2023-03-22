from seleniumwire import webdriver
from selenium_stealth import stealth
from datetime import datetime
from datetime import timedelta
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import csv
import time

#Start date for scraping
currentdate = datetime(2023,4,1)

#Open the file in the write mode
f = open('/Users/jonasbert/Documents/GitHub/ScrapingProject/brussels.csv', 'w')

#Create the csv writer
writer = csv.writer(f)
header = ['Price',"FlightNumber", 'Date of Departure','Date of Arrival','Available seats', 'Arrival Airport code', 'Arrival Airport name', "Departure Airport code", "Departure Airport name","Flight Duration","Scraping date"]
writer.writerow(header)

#Close the file
f.close()

#Destinations defined by ITAO codes
Corfu = "CFU"
Kreta = "HER"
Rhodos = "RHO"
Brindisi = "BDS"
Napels = "NAP"
Palermo = "PMO"
Faro = "FAO"
Alicante = "ALC"
Ibiza = "IBZ"
Malaga = "AGP"
Palma = "PMI"
Tenerife = "TFS"

destinations = [Corfu, Kreta, Rhodos, Brindisi, Napels, Palermo, Faro, Alicante, Ibiza, Malaga, Palma, Tenerife]

#Static CSS Selectors and XPaths
url = 'https://www.brusselsairlines.com/be/en/homepage'
coockieselector = "#cm-acceptNone"
owselector = ".selectable .selectable-dropdown.selectable-dropdown-secondary .dropdown-content"
searchselector = ".btn-primary"
dateselector = "/html[1]/body[1]/div[2]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/section[1]/div[2]/div[1]/div[1]/div[1]/form[1]/div[2]/div[2]/div[1]/div[1]/div[1]/input[1] "
owxpath = "/html/body/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div/section/div[2]/div[1]/div/div/form/div[1]/div/div/div[2]/ul/li[2]/div"
destxpath = "/html/body/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div/section/div[2]/div[1]/div/div/form/div[2]/div[1]/div/div[3]/div/div[1]/div[1]/div[1]/input"
confirmxpath = "/html/body/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div/section/div[2]/div[1]/div/div/form/div[2]/div[1]/div/div[3]/div/div[2]"
flightxpath = "/html/body/div[2]/div/cont-ffpp/cont-splashable-content/div/cont-avails/pres-avails/div[2]/cont-avail[1]/pres-avail/div/div/pres-avail-class-info[1]"
flightdetailsxpath = "/html/body/div[2]/div/cont-ffpp/cont-splashable-content/div/cont-avails/pres-avails/div[2]/cont-avail[1]/pres-avail/div/pres-avail-info"
errorxpath = "/html/body/div[3]/article/div/section/leg-messages/cont-messages-common/pres-message-common"
searchselectxpath = "/html[1]/body[1]/div[7]/div[1]/div[1]/div[2]/div[3]/div[2]/button[1]"
monthselectxpath = "//span[normalize-space()='March']"
aprilxpath = "//div[@role='option'][normalize-space()='April']"
tableselector = "body > div.modal.react-modal.modal-calendar.modal-size-calendar.react-modal-opened > div > div > div.modal-body > div.calendar.d-md-flex.justify-content-center > div > div > div > div.DayPicker_focusRegion.DayPicker_focusRegion_1 > div.DayPicker_transitionContainer.DayPicker_transitionContainer_1.DayPicker_transitionContainer__horizontal.DayPicker_transitionContainer__horizontal_2 > div > div:nth-child(2) > div > table"
confirmdatexpath = "//button[@aria-label='Continue']"
accordionselector = "body > app > refx-app-layout > div > div.main-content.justify-content-center > refx-upsell > refx-basic-in-flow-layout > div > div.content-wrapper > div:nth-child(3) > div > div > div > refx-upsell-premium-cont > refx-upsell-premium-pres > mat-accordion"

#Path to Chromedriver and setting up Selenium
PATH = "/Users/jonasbert/Downloads/chromedriver/chromedriver"

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
#options.add_argument("--headless")
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
driver_service = Service(executable_path=PATH)
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(service=driver_service, options=options)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
driver.implicitly_wait(25)
wait = WebDriverWait(driver, 25)

#Actual scraping script
for destination in destinations:
        print("Scraping flights for destination: " + destination + "...")

        while currentdate < datetime(2023,10,1):

                #Change dynamic XPaths and Selectors
                monthxpath = "//div[@role='option'][normalize-space()='" + currentdate.strftime('%B') + "']"

                driver.get(url)
                driver.find_element(By.CSS_SELECTOR, coockieselector).click()
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, owselector))).click()
                driver.find_element(By.XPATH, owxpath).click()
                driver.find_element(By.XPATH, destxpath).send_keys(destinations[0])
                time.sleep(1)
                driver.find_element(By.XPATH, dateselector).click()
                driver.find_element(By.XPATH, monthselectxpath).click()
                driver.find_element(By.XPATH, monthxpath).click()

                #Iterate over all cells in calendar table and select cell which corresponds to current date
                table = driver.find_element(By.CSS_SELECTOR, tableselector)
                for row in table.find_elements(By.TAG_NAME,"tr"):
                        for cell in row.find_elements(By.TAG_NAME,"td"):  
                                if len(cell.text.splitlines()) > 0 and int(cell.text.splitlines()[0]) == currentdate.day:
                                        cell.click()
                                        break

                driver.find_element(By.XPATH, confirmdatexpath).click()
                driver.find_element(By.CSS_SELECTOR, searchselector).click()

                #Iterate over available flights
                ingo = []
                accordion = driver.find_element(By.CSS_SELECTOR, accordionselector)
                for flight in accordion.find_elements(By.TAG_NAME,"refx-upsell-premium-row-pres"):
                        operatedBy = []
                        for airline in flight.find_elements(By.CLASS_NAME, "operating-airline-name"):
                                operatedBy.append(airline.text)
                        #Select flights at least operated once by Brussels Airlines
                        if "Brussels Airlines" in operatedBy:
                                departtime = flight.find_elements(By.CLASS_NAME, 'refx-display-1 bound-departure-datetime')
                                print(departtime)
                                departdatetime = currentdate + timedelta(hours=int(departtime[:2]),minutes=int(departtime[3:2]))
                                print(departdatetime)
                                for button in flight.find_elements(By.TAG_NAME, "button"):
                                        button.click()
                                for carousel in accordion.find_elements(By.TAG_NAME,"refx-carousel"):
                                        for fare in carousel.find_elements(By.TAG_NAME,"mat-card"):
                                                #Select only Economy Classic fare
                                                if fare.text.splitlines()[1] == "Economy Classic":
                                                        print(fare.text.splitlines())
                                                        print(flight.find_elements(By.CLASS_NAME, 'refx-display-1 bound-departure-datetime'))
                                                        departtime = flight.find_elements(By.CLASS_NAME, 'refx-display-1 bound-departure-datetime')[0]
                                                        departdatetime = currentdate + timedelta(hours=int(departtime[:2]),minutes=int(departtime[3:2]))
                                                        arrivaltime = flight.find_elements(By.CLASS_NAME, 'refx-display-1 bound-arrival-datetime')[0].text
                                                        arrivaldatetime = currentdate + timedelta(hours=int(arrivaltime[:2]),minutes=int(arrivaltime[3:2]))
                                                        daysafter = flight.find_elements(By.CLASS_NAME, 'refx-caption bound-arrival-day-indicator ng-star-inserted')
                                                        if daysafter != []:
                                                                arrivaldatetime + timedelta(days=int(daysafter[0][1]))
                                                        
                                                        fareList = []
                                                        fareList.append(fare.text.splitlines()[0])
                                                        fareList.append(departdatetime)
                                                        fareList.append(arrivaldatetime)
                                                        if fare.text.splitlines()[2] == "Rebooking":
                                                                fareList.append(-1)
                                                        else:
                                                                fareList.append(int(fare.text.splitlines()[2][0]))
                                                        fareList.append
                                                        with open('/Users/jonasbert/Documents/GitHub/ScrapingProject/brussels.csv', 'a') as f_object:
                                                                writer_object = csv.writer(f_object)
                                                                writer_object.writerow(fareList)
                                                                f_object.close()     

                time.sleep(3600)

                #Adding 1 day to current date
                currentdate + timedelta(days=1)
                driver.close()
        




