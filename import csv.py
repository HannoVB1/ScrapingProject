import csv


f = open('C:\\Users\\hanno\\Desktop\\tui.csv', 'w')

# create the csv writer
writer = csv.writer(f)

# write a row to the csv file
writer.writerow(["TEST"])

# close the file
f.close()