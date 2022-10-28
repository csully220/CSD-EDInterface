import json
import os
from datetime import datetime 


    

path = 'C:/Users/Colin/Saved Games/Frontier Developments/Elite Dangerous/'
fn = r'Status.json'
fp = path + fn
f = open(fp, 'r')
tsLP = os.stat(fp).st_mtime
line = f.readline().strip()
f.close()
d = json.loads(line)


def GetLatestJournal(path):
    journals = []
    files = os.listdir(path)
    for f in files:
        fs = f.split('.')
        if(fs[0] == 'Journal'):
            journals.append(f)
    lj = ''
    jdtLP = 0.0
    for j in journals:
        jdt = os.stat(fp).st_mtime
        if(jdt >= jdtLP):
            lj = j
    return lj
    



while(True):
    ts = os.stat(fp).st_mtime
    if(ts != tsLP):
        f = open(fp, 'r')
        line = f.readline().strip()
        f.close()
        if(line):
            d = json.loads(line)
            print(d['Flags'])
            print(d['Pips'])
        tsLP = ts
