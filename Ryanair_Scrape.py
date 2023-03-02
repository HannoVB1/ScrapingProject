import requests
from bs4 import BeautifulSoup
import json
import datetime

OriginArray=["BRU","CRL"]
DestinationArray=["CFU","HER","RHO","BDS","NAP","PMO","FAO","ALC","IBZ","AGP","PMI","TFS"]
startDate = datetime.datetime(2023,4,1)
Days = []
for i in range(0,31):
    Days.append(startDate)
    startDate = startDate + datetime.timedelta(days = 6) 

arrayPages = []

for DayLoop in Days:
    for OriginLoop in OriginArray:
        for DestinationLoop in DestinationArray:
            DateOut=DayLoop.strftime("%Y-%m-%d")
            Destination=DestinationLoop
            Origin=OriginLoop

            URL = f"https://www.ryanair.com/api/booking/v4/nl-nl/availability?dateOut={DateOut}&Destination={Destination}&Origin={Origin}&FlexDaysOut=6&ToUs=AGREED"

            page = requests.get(URL)

            print(page.content)            
            arrayPages.append(page.content)



    