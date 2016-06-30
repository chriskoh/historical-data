#!/usr/bin/env python3

import sys
import requests
import os
import datetime
from bs4 import BeautifulSoup, NavigableString

def scrape(website):
	set_url = website
	cal_resp = requests.get(set_url)
	cal_data = cal_resp.text
	data = BeautifulSoup(cal_data, 'lxml')

	return str(data)

def main():
	os.system('clear')

	# Get ticker from user
	ticker = input('Enter Ticker: ')
	market = input('Choose Market (NYSE || NASD): ')

	# scrape data and write to a file
	data = scrape('https://www.google.com/finance/getprices?q=' + str(ticker.upper()) + '&x=' + str(market.upper()) + '&i=60&p=30d&f=d,c,h,l,o,v')
	f = open('./data/' + ticker, 'w')
	f.write(data)
	f.close()

	# remove lines 1-7 and the last line, then override file
	lines = open('./data/' + ticker).readlines()
	newfile = open('./data/' + ticker,'w').writelines(lines[7:-1])

	# open new file and use data
	data = open('./data/' + ticker).readlines()

	# create dictionary for data storage && store data / calculate pct change per min per day
	intraday = {}
	average = {}
	day = 0
	for line in data:
		split = line.split(',')
		if str(split[0]).startswith('a'): # replace unix time stamp for new day with 0, to represent minute 0 rather than new day
			split[0] = str(0)

		intraday[str(day) + split[0] + 'high'] = float(split[2]) # split[0] = min, [1] = close, [2] = high, [3] = low, [4] = open, [5] = volume
		intraday[str(day) + split[0] + 'low'] = float(split[3])
		intraday[str(day) + split[0] + 'open'] = float(split[4])
		intraday[str(day) + split[0] + 'close'] = float(split[1])
		intraday[str(day) + split[0] + 'vol'] = int(split[5])
		intraday[str(day) + split[0] + 'pctchange'] = ((float(split[1]) / float(split[4])) - int(1)) * int(100)

		average[split[0] + 'avgpctchange'] = 0
		average[split[0] + 'close'] = 0

		if int(split[0]) == int(390):
			day += 1

	# add pctchanges for each min
	for x in range(day):
		for x2 in range(390):
			average[str(x2) + 'avgpctchange'] += float(intraday[str(x) + str(x2) + 'pctchange'])	
			average[str(x2) + 'close'] += float(intraday[str(x) + str(x2) + 'close'])

	# calculate average pctchange
	for x in range(390):
		average[str(x) + 'avgpctchange'] /= int(day)
		average[str(x) + 'close'] /= int(day)

	# find min and max
	lowval = average[str(0) + 'avgpctchange']
	lowmin = 0
	lowamount = 0
	highval = average[str(0) + 'avgpctchange']
	highmin = 0
	highamount = 0
	for x in range(390):
		if average[str(x) + 'avgpctchange'] < lowval:
			lowval = average[str(x) + 'avgpctchange']
			lowmin = x
			lowamount = average[str(x) + 'close']
		if average[str(x) + 'avgpctchange'] > highval:
			highval = average[str(x) + 'avgpctchange']
			highmin = x
			highamount = average[str(x) + 'close']

	# calculate time
	today = datetime.datetime.today()
	marketopen = datetime.datetime(today.year, today.month, today.day, 6, 30)
	lowdelta = datetime.timedelta(minutes = int(lowmin))
	highdelta = datetime.timedelta(minutes = int(highmin))
	marketlow = marketopen + lowdelta
	markethigh = marketopen + highdelta

	
	print('%s: Average +/- percent change per min (Last 15 days) - Highest: $%.2f @ +%.4f%% (%s) | Lowest: $%.2f @ %.4f%% (%s) ' % (str(ticker.upper()), highamount, highval, str(markethigh.strftime("%I:%M%p")), lowamount, lowval, str(marketlow.strftime("%I:%M%p"))))











if __name__ == '__main__':
	main()
