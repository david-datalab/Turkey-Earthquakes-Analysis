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
conn = sqlite3.connect('EQ.sqlite')
cur = conn.cursor()
cur.executescript('''
CREATE TABLE IF NOT EXISTS earthQuake (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    date   TEXT,
    time    TEXT,
    latitiude   TEXT,
    longtitude  TEXT,
    depth   TEXT,
    magnitude   TEXT,
    region  TEXT
)
''')
def watchEQ():
    counter = 1
    print("Monitoring started ....\n")
    while True:
        lst=list()
        print("--- !!! ",counter," !!! ---")
        url = ('http://www.koeri.boun.edu.tr/scripts/lst9.asp')
        try:
            html = urllib.request.urlopen(url, context=ctx).read()
        except:
            print("!!! NETWORK ERROR !!!")
            watchEQ()
        soup = BeautifulSoup(html, 'html.parser')
        #retrive raw data
        tags = soup('pre')
        #a function to split and organize data and store the values in a list then to a dictionary to finally go to a data base

        for tag in tags:
            # Look at the parts of a tag
            fh = tag

            for line in fh:#to extract valuse and put them in a list
                data = line
                ln = re.findall("(\S.*)", data)

                for s in ln: #to loop through the strings found in ln
                    if s not in lst:#UPDATE: the headache was here XD #to add the string value in a single list
                        lst.append(s)

        lastEQ = lst[6].split()
        mag = lastEQ[5] + " " + lastEQ[6] + " " + lastEQ[7]
        reg = " ".join(lastEQ[8:-1])

        results = {"date" : lastEQ[0],
        "time" : lastEQ[1],
        "latitiude" : lastEQ[2],
        "longtitude" : lastEQ[3],
        "depth" : lastEQ[4],
        "magnitude" : mag,
        "region" : reg}
        cur.execute('''INSERT OR IGNORE INTO earthQuake (date, time, latitiude, longtitude, depth, magnitude, region)
        VALUES (?,?,?,?,?,?,?)''', (results["date"],results["time"],results["latitiude"],results["longtitude"],results["depth"],results["magnitude"],results["region"]))
        conn.commit()
        time.sleep(3)
        counter = counter + 1
        print("Date :", results["date"])
        print("Time :", results["time"])
        print("Latitude :", results["latitiude"])
        print("Longtitude :", results["longtitude"])
        print("Depth\Km :", results["depth"])
        print("Magnitude :", results["magnitude"])
        print("Region :", results["region"])
        print("\n")
watchEQ()
