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
import ssl
import re
import time
import sqlite3
import sys

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#database creation
conn = sqlite3.connect('Database.sqlite')
cur = conn.cursor()
cur.executescript('''
CREATE TABLE IF NOT EXISTS earthQuake (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    date   TEXT,
    time    TEXT UNIQUE,
    latitiude   TEXT,
    longitude  TEXT,
    depth   TEXT,
    magnitude   TEXT,
    region  TEXT
)
''')

print('started')

while True:
    # Check to see if we are already in progress...
    cur.execute('SELECT id,time FROM earthQuake WHERE latitiude is NULL and longitude is NULL ORDER BY RANDOM() LIMIT 1')
    row = cur.fetchone()
    if row is not None :
        print("Restarting existing crawl.  Remove old database to start a fresh crawl.")
    else:
        lst=list()
        url = ('http://www.koeri.boun.edu.tr/scripts/lst9.asp')
        try:
            html = requests.get(url).text
        except:
            print("!!! NETWORK ERROR !!!")

        soup = BeautifulSoup(html, "html.parser")
        #retrive raw data
        tags = soup('pre')
        # Look at the parts of a tag
        for tag in tags:
            fh = tag

            for line in fh:#to extract valuse and put them in a list
                data = line
                ln = re.findall("(\S.*)", data)

                for s in ln: #to loop through the strings found in ln
                    if s not in lst:#UPDATE: the headache was here XD #to add the string value in a single list
                        #print(s)
                        lst.append(s)

        lastEQ = lst[6].split()
        mag = lastEQ[5] + " " + lastEQ[6] + " " + lastEQ[7]
        reg = " ".join(lastEQ[8:-1])
        date = lastEQ[0]
        tim = lastEQ[1]
        latitiude = lastEQ[2]
        longitude = lastEQ[3]
        #print(longitude)
        depth = lastEQ[4]
        magnitude = mag
        region = reg
        lstResults = [date,tim,latitiude,longitude,depth,magnitude,region]
        #print(lstResults)
        try:
            #read last value from data base and compare it to last reading value
            cur.execute('SELECT longitude FROM earthQuake ORDER BY id DESC')
            lon = cur.fetchone()
            print(lon)
            slon = str(lon[0])
            try:
                cur.execute('SELECT latitiude FROM earthQuake ORDER BY id DESC')
                lat = cur.fetchone()
                slat = str(lat[0])
            except Exception as e:
                print(e)

            if slon != longitude and slat != latitiude:
                #fh = open('records.csv',"a+")
                formated = "{},{},{},{},{},{},{}\n".format(lstResults[0], lstResults[1], lstResults[2], lstResults[3], lstResults[4], lstResults[5], lstResults[6])
                #print(formated)
                #fh.write(formated)
                #fh.close()
                cur.execute('''INSERT OR IGNORE INTO earthQuake (date, time, latitiude, longitude, depth, magnitude, region)
                VALUES (?,?,?,?,?,?,?)''', (date,tim,latitiude,longitude,depth,magnitude,region))
        except Exception as e:
            z = e
            print(z)

        conn.commit()
        time.sleep(3)
