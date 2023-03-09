import requests
from bs4 import BeautifulSoup
import json
import datetime
import csv

# open the file in the write mode
f = open('C:\\Users\\hanno\\Desktop\\\\ryanair.csv', 'w')

# create the csv writer
writer = csv.writer(f)
header = ['Price',"FlightNumber", 'Date of Departure','Date of Arrival','Available seats', 'Arrival Airport code', 'Arrival Airport name', "Departure Airport code", "Departure Airport name","Flight Duration","Scraping date"]
writer.writerow(header)
# close the file
f.close()

OriginArray=["BRU","CRL"]
DestinationArray=["CFU","HER","RHO","BDS","NAP","PMO","FAO","ALC","IBZ","AGP","PMI","TFS"]
startDate = datetime.datetime(2023,4,1)
Days = []
for i in range(0,31):
    Days.append(startDate)
    startDate = startDate + datetime.timedelta(days = 6) 

for DayLoop in Days:
    for OriginLoop in OriginArray:
        for DestinationLoop in DestinationArray:
            k = open('C:\\Users\\hanno\\Desktop\\ryanair.csv', 'a')
            writer2 = csv.writer(k)
            DateOut=DayLoop.strftime("%Y-%m-%d")
            Destination=DestinationLoop
            Origin=OriginLoop
            URL = f"https://www.ryanair.com/api/booking/v4/nl-nl/availability?dateOut={DateOut}&Destination={Destination}&Origin={Origin}&FlexDaysOut=6&ToUs=AGREED"
        
            page = requests.get(URL)
       
            json_object = json.loads(page.content)
            if(len(json_object) == 8):
                for trip in json_object["trips"]:
                    tripOrigin = trip["origin"]
                    tripOriginName = trip["originName"]
                    tripDestination = trip["destination"]
                    tripDestinationName = trip["destinationName"]
                    if len(trip["dates"]) != 0:
                        for date in trip["dates"]:
                            if len(date["flights"]) != 0:
                               for flight in date["flights"]:   
                                tripDateOut = flight["time"][0]
                                tripDateArrival = flight["time"][1]
                                tripDuration = flight["duration"]
                                tripAvailableSeats = flight["faresLeft"]
                                tripPrice = flight["regularFare"]["fares"][0]["amount"]
                                tripFlightNumber = flight["flightNumber"]
                                if tripAvailableSeats == -1:
                                    tripAvailableSeats = 0
                                dataArray = [tripPrice,tripFlightNumber,tripDateOut,tripDateArrival,tripAvailableSeats,tripDestination,tripDestinationName,tripOrigin,tripOriginName,tripDuration,datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')]
                                print(dataArray)
                                writer2.writerow(dataArray)
            k.close()



    