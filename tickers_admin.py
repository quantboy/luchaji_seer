# tickers_admin
#
# to debug- python -m pdb tickers_admin.py

import sqlite3
import time
from yahoo_finance import Share


def getData(tkr):
    conn = sqlite3.connect('luchaji_seer.db')
    cur = conn.cursor()
    cur.execute("select symbol, date, price, volume from data where symbol=? order by symbol, date", [tkr] )
    rows = cur.fetchall()
    return rows



def getTickers():
    conn = sqlite3.connect('luchaji_seer.db')
    cur = conn.cursor()
    cur.execute('select symbol from tickers order by symbol')
    rows = cur.fetchall()
    return rows


def insertTicker(tkr, desc):
    conn = sqlite3.connect('luchaji_seer.db')
    cur = conn.cursor()
    cur.execute("insert into tickers(symbol, description) values( ?, ?)", (tkr, desc))
    conn.commit()


def deleteTicker(tkr):
    conn = sqlite3.connect('luchaji_seer.db')
    cur = conn.cursor()
    cur.execute("delete from tickers where symbol = ?", (tkr))
    cur.execute("delete from data where symbol = ?", (tkr))
    cur.execute("delete from stats where symbol = ?", (tkr))
    conn.commit()


def showTickers():
    symbols = getTickers()
    for s in symbols:
        print str(s[0]),
    print


def showData():
    tkr = raw_input('Ticker of data to show ').strip()
    rows = getData(tkr)
    for r in rows:
        print "%5s %s %10.3f %12.0f" % (r[0], r[1], r[2], r[3])


def showMenu():
    print "[1] Show tickers"
    print "[2] Add ticker"
    print "[3] Remove ticker"
    print "[4] Update ticker stats"
    print "[5] Show data"
    print "[0] Exit"


def addTicker():
    tkr = raw_input('Ticker to add ').strip()
    desc = raw_input('Description to add ').strip()
    insertTicker(tkr, desc)


def removeTicker():
    tkr = raw_input('Ticker to remove ').strip()
    deleteTicker(tkr)


def getLastCobDateForTicker(tkr):
    conn = sqlite3.connect('luchaji_seer.db')
    cur = conn.cursor()
    cur.execute("select max(date) from data where symbol = ?", [tkr])
    rows = cur.fetchall()
    return rows[0][0]


def insertData(tkr,data,lastCob):
    conn = sqlite3.connect('luchaji_seer.db')
    cur = conn.cursor()

    script = ""
    for dataRow in data:
        date = str(dataRow['Date'])
        if date > lastCob:
            adjPrice = str(dataRow['Adj_Close'])
            vol = str(dataRow['Volume'])
            command = "insert into data(symbol, date, price, volume) values ('%s','%s',%.3f,%12.0f);\n" % ( tkr, date, float(adjPrice), float(vol))
            script = script + command
            print command
    if len(script)>1:
        cur.executescript(script)
        conn.commit()


def updateAllTickerStats():
    tickers = getTickers()
    for tkr in tickers:
        updateStats(str(tkr[0]))


def updateStats(tkr):
    lastCob = '2010-01-01'
    lastCobFromDb = str(getLastCobDateForTicker(tkr))
    if (lastCobFromDb != "(None,)"):
        lastCob = lastCobFromDb

    print "Getting historical data for %s since %s" % (tkr, lastCob)
    tkrObj = Share(tkr)
    tkrData = tkrObj.get_historical(lastCob, time.strftime("%Y-%m-%d") )
    print len(tkrData)
    insertData(tkr,tkrData,lastCob)


def letUserTakeAction():
    shouldExit = False
    showMenu()
    choice = raw_input('Select ')
    if choice == '1':
        showTickers()
    elif choice == '2':
        addTicker()
    elif choice == '3':
        removeTicker()
    elif choice == '4':
        updateAllTickerStats()
    elif choice == '5':
        showData()
    elif choice == '0':
        shouldExit = True
    return shouldExit


while 1:
    if letUserTakeAction() == True:
        break


