import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re
import time
import sqlite3

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#database creation
conn = sqlite3.connect('E1Q.sqlite')
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
counter = 0
while True:
    # Check to see if we are already in progress...
    cur.execute('SELECT id,time FROM earthQuake WHERE latitiude is NULL and longitude is NULL ORDER BY RANDOM() LIMIT 1')
    row = cur.fetchone()
    if row is not None :
        print("Restarting existing crawl.  Remove old database to start a fresh crawl.")
    else:

        print("Monitoring started ....\n")
        lst=list()
        print("!!! ",counter," !!!")
        url = ('http://www.koeri.boun.edu.tr/scripts/lst9.asp')
        try:
            html = urllib.request.urlopen(url, context=ctx).read()
        except:
            print("!!! NETWORK ERROR !!!")
        soup = BeautifulSoup(html, 'html.parser')
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
                        lst.append(s)
        print("=== LAST READING ===")
        lastEQ = lst[6].split()
        mag = lastEQ[5] + " " + lastEQ[6] + " " + lastEQ[7]
        reg = " ".join(lastEQ[8:-1])

        date = lastEQ[0]
        tim = lastEQ[1]
        latitiude = lastEQ[2]
        longitude = lastEQ[3]
        depth = lastEQ[4]
        magnitude = mag
        region = reg

        lstResults = [date,tim,latitiude,longitude,depth,magnitude,region]
        #print(lstResults)

        try:
            #read last value from data base and compare it to last reading value
            cur.execute('SELECT longitude FROM earthQuake ORDER BY id DESC')
            lon = cur.fetchone()
            slon = str(lon[0])

            cur.execute('SELECT latitiude FROM earthQuake ORDER BY id DESC')
            lat = cur.fetchone()
            slat = str(lat[0])

            if slon == longitude:
                print("NO NEW EARTHQUAKE DETECTED")
            elif slat == latitiude:
                print("NO NEW EARTHQUAKE DETECTED")
            else:
                print(" /!\ /!\ /!\ NEW EARTHQUAKE DETECTED /!\ /!\ /!\ ")
                print(lstResults)
        except:
            print("ERROR READING FROM DATABASE")

        try:
            cur.execute('''INSERT OR IGNORE INTO earthQuake (date, time, latitiude, longitude, depth, magnitude, region)
            VALUES (?,?,?,?,?,?,?)''', (date,tim,latitiude,longitude,depth,magnitude,region))
        except:
            print("!!! DATABASE WRITING ERROR !!!")

        conn.commit()
        time.sleep(30)
        counter = counter + 1
        lst = None
        lastEQ = None
        lstResults = None

    pass
