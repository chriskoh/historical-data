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
	var = input('Enter Ticker: ')

	# scrape data and write to a file
	data = scrape('https://www.google.com/finance/getprices?q=' + str(var.upper()) + '&x=NASD&i=60&p=30d&f=d,c,h,l,o,v')
	f = open('datatest', 'w')
	f.write(data)
	f.close()

	# remove lines 1-7 and the last line, then override file
	lines = open('datatest').readlines()
	newfile = open('datatest','w').writelines(lines[7:-1])

	# open new file and use data
	data = open('datatest').readlines()

	# create dictionary for data storage
	intraday = {}
	count = 0
	for line in data:
		split = line.split(',')
		if str(split[0]).startswith('a'): # replace unix time stamp for new day with 0, to represent minute 0 rather than new day
			split[0] = str(0)
		intraday[split[0] + 'high'] = 0 
		intraday[split[0] + 'low'] = 0
		intraday[split[0] + 'open'] = 0
		intraday[split[0] + 'close'] = 0


	# populate dictionary
	for line in data:
		split = line.split(',')
		if str(split[0]).startswith('a'):
			split[0] = str(0)
		intraday[split[0] + 'high'] += float(split[2]) 
		intraday[split[0] + 'low'] += float(split[3])
		intraday[split[0] + 'open'] += float(split[4])
		intraday[split[0] + 'close'] += float(split[1])

	# divide data by 15 (max number of days pulled by google finance intraday)
	for x in range(390):
		intraday[str(x) + 'high'] /= int(15)
		intraday[str(x) + 'low'] /= int(15)
		intraday[str(x) + 'open'] /= int(15)
		intraday[str(x) + 'close'] /= int(15)

	# calculation variables
	today = datetime.datetime.today()
	marketopen = datetime.datetime(today.year, today.month, today.day, 6, 30)
	low = 1000
	lowest = 0
	high = 0
	highest = 0

	# calculate data based on close price for each min
	for x in range(390):
		if intraday[str(x) + 'close'] < low: # average lowest close min in the last 15 days
			low = intraday[str(x) + 'close']
			lowest = x
		if intraday[str(x) + 'close'] > high: # average highest close min in the last 15 days
			high = intraday[str(x) + 'close']
			highest = x

	# calculate time
	lowdelta = datetime.timedelta(minutes = int(lowest))
	highdelta = datetime.timedelta(minutes = int(highest))
	marketlow = marketopen + lowdelta
	markethigh = marketopen + highdelta

	
	print(str(var.upper()) + ' last 15 days (Average intraday) - Highest: $' + str(high) + '(' + str(markethigh) + ')' + ' | Lowest: $' + str(low) + '(' + str(marketlow) + ')')

















if __name__ == '__main__':
	main()
