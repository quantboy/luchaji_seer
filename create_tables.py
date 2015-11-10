# create tables
#   tickers
#   data
#   stats

import sqlite3
conn = sqlite3.connect('luchaji_seer.db')

c = conn.cursor()

# Create tables
c.execute('create table if not exists tickers(symbol text, description text)')
c.execute('create unique index if not exists tickers_idx on tickers(symbol)')

c.execute('create table if not exists data(symbol text, date text, price real, volume real)')
c.execute('create unique index if not exists data_idx on data(symbol, date)')

c.execute('create table if not exists stats(symbol text, date text, ma50 real, ma200 real, ema200 real)')
c.execute('create unique index if not exists stats_idx on stats(symbol, date)')

conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()


