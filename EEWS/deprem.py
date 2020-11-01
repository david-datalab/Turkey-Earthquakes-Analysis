import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re
import time
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def watchEQ():
    try:
        print("Monitoring started ....\n")
        while True:
            url = ('http://www.koeri.boun.edu.tr/scripts/lst9.asp')
            try:
                html = urllib.request.urlopen(url, context=ctx).read()
            except:
                print("!!! NETWORK ERROR !!!")

            soup = BeautifulSoup(html, 'html.parser')
            #retrive raw data
            tags = soup('pre')
            #a function to split and organize data and store the values in a list then to a dictionary to finally go to a data base
            lst=list()

            for tag in tags:
                # Look at the parts of a tag
                fh = tag
                #print(fh)
                for line in fh:#to extract valuse and put them in a list
                    #print(line)
                    data = line
                    #print(data)
                    ln = re.findall("(\S.*)", data)
                    #print(ln)
                    for s in ln: #to loop through the strings found in ln
                        if s not in lst:#UPDATE: the headache was here XD #to add the string value in a single list
                            lst.append(s)
            lastEQ = lst[6].split()
            #print(lastEQ)
            results = {"date" : lastEQ[0],
            "time" : lastEQ[1],
            "latit" : lastEQ[2],
            "long" : lastEQ[3],
            "depth" : lastEQ[4],
            "magnitude" : lastEQ[5:8],
            "region" : lastEQ[8:-1]}
            print("Date :", results["date"])
            print("Time :", results["time"])
            print("Latitude :", results["latit"])
            print("Longtitude :", results["long"])
            print("Depth\Km :", results["depth"])
            print("Magnitude :", results["magnitude"])
            print("Region :", results["region"])
            print("\n")
            time.sleep(60)
    except:
        print("!!! RESTARTING !!!")
        watchEQ()
watchEQ()
