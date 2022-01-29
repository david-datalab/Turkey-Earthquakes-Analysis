#Turkey Earthquakes Analysis
#Copyright (C) <2021-2022>  <Muhannad Daoud>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
#Email: daoudmhnd@gmail.com

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
    date DATE,
    time TIME,
    latitiude TEXT,
    longitude TEXT,
    depth TEXT,
    magnitude INTEGER,
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
    #this line is to check to compare the results
    cur.execute('SELECT id FROM EarthQuake ORDER BY id DESC LIMIT 1')
    IdRecent = cur.fetchone()


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

    #to check the results
    try:
        cur.execute('SELECT * FROM EarthQuake ORDER BY id DESC LIMIT 1')
        result = cur.fetchone()
        IdNew = result[0]
        if IdNew > IdRecent[0]:
            print(result)

    except Exception as E5:
        print('E5: Data checking error')
        print(E5)

    conn.commit()
    T.sleep(15)
