import requests
from bs4 import BeautifulSoup
import re
import sqlite3
import time as T

print('Started')

try:
    #Database creation
    conn = sqlite3.connect('Database.sqlite')
    #Database Handler
    cur = conn.cursor()
    #Database table
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS EarthQuake (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    date TEXT,
    time TEXT UNIQUE,
    latitiude TEXT,
    longitude TEXT,
    depth TEXT,
    magnitude TEXT,
    region TEXT
    )
    ''')

except Exception as E1:
    print('E1: Database creation error')
    print(E1)

#the program will loop for ever to keep refreshing the data source every 15 seconds

while True:
    try:
        #preparing the data source
        url = ('http://www.koeri.boun.edu.tr/scripts/lst9.asp')
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        tags = soup('pre')
        lst = list()

    except Exception as E2:
        print('E2: Connection Error')
        print(E2)

    try:
        #looping through the strings inside the pre tag and add the results to a list
        for tag in tags:
            fh = tag

            for line in fh:
                data = line
                ln = re.findall("(\S.*)", data)

                for s in ln:
                    if s not in lst:#UPDATE: to add the string value in a single list
                        lst.append(s)

    except Exception as E3:
        print('E3: Error while scraping data from source')
        print(E3)

    #cleaning the retrived data and prepare the requried lines for analysis
    lastEQ = lst[6].split()
    date = lastEQ[0]
    time = lastEQ[1]
    latitiude = lastEQ[2]
    longitude = lastEQ[3]
    depth = lastEQ[4]
    magnitude = lastEQ[6]
    region = " ".join(lastEQ[8:-1])
    lstResults = [date,time,latitiude,longitude,depth,magnitude,region]
    #now we have a list of the data needed for the analysis
    #we will add the data to sqlite data base to proceed with the analysis
    #to fill the records in the database
    try:
        #first we start to write the data to the database
        cur.execute('''INSERT OR IGNORE INTO EarthQuake (date, time, latitiude, longitude, depth, magnitude, region)
        VALUES (?,?,?,?,?,?,?)''',(date, time, latitiude, longitude, depth, magnitude, region))
    
    except Exception as E4:
        print('E4: Database writing error')
        print(E4)

    try:
        #to check the results
        #first we divide the data as strings 
        formated = "{},{},{},{},{},{},{}\n".format(lstResults[0], lstResults[1], lstResults[2], lstResults[3], lstResults[4] ,lstResults[5], lstResults[6])
    
        #we look for the longitude and compare it with recorded results
        cur.execute('SELECT longitude FROM EarthQuake ORDER BY id DESC')
        lon = cur.fetchone()
        slon = str(lon[0])

        #we look for the latitude and compare it with recorded results
        cur.execute('SELECT latitiude FROM EarthQuake ORDER BY id DESC')
        lat = cur.fetchone()
        slat = str(lat[0])
        #we compare the values and print the last record to avoid printing new lines for each execution

        if slon != longitude and slat != latitiude:
            print(formated)

    except Exception as E5:
        print('E5: Data checking error')
        print(E5)

    conn.commit()
    T.sleep(15)
