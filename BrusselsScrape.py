from seleniumwire import webdriver
from selenium_stealth import stealth
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import json
import time

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

#CSS Selectors and XPaths
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
searchselectxpath = "/html[1]/body[1]/div[3]/article[1]/div[1]/section[1]/div[3]/div[3]/div[1]/section[1]/fieldset[9]/footer[1]/button[1]/span[1]"
departdatexpath = "/html[1]/body[1]/div[6]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[3]/div[1]/table[1]/tbody[1]/tr[1]/td[6]"

#Path to Chromedriver and options
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


driver.get(url)
driver.find_element(By.CSS_SELECTOR, coockieselector).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, owselector))).click()
driver.find_element(By.XPATH, owxpath).click()
#driver.find_element(By.CSS_SELECTOR, owselector).click()
#driver.find_element(By.XPATH, owxpath).click()
driver.find_element(By.XPATH, destxpath).send_keys(destinations[0])
time.sleep(1)
driver.find_element(By.XPATH, dateselector).click()
#WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, departdatexpath))).click()
time.sleep(3)
driver.find_element(By.XPATH, "/html[1]/body[1]/div[7]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[3]/div[1]/table[1]/tbody[1]/tr[1]/td[6]").click()
driver.find_element(By.CSS_SELECTOR, searchselector).click()
time.sleep(5)
print(driver.find_elements(By.CLASS_NAME, "bound-stop-text ng-star-inserted"))


#driver.quit()