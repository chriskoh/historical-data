#!/usr/bin/env python3

import datetime
import os
import requests
from bs4 import BeautifulSoup, NavigableString

def scrape(website):
        set_url = website
        cal_resp = requests.get(set_url)
        cal_data = cal_resp.text
        data = BeautifulSoup(cal_data, 'lxml')

        return data

def temp(ticker, market):

        # scrape data and write to a temp file
        data = scrape('https://www.google.com/finance/getprices?q=' + str(ticker.upper()) + '&x=' + str(market.upper()) + '&i=60&p=30d&f=d,c,h,l,o,v')
        data = str(data)
        f = open('/intradata/temp', 'w')
        f.write(data)
        f.close()

def findmarket(ticker):
	
	data = scrape('https://www.google.com/finance?q=' + ticker)
	title = str(data.title)
	if 'NASDAQ' in title:
		return 'NASD'
		print('nasdaq')
	else:
		return 'NYSE'
		print('nyse')

def parsefile(lines):

#get a dict containing #days, day name, #mins and min data for temp file (use to compare to saved file to append new data)      
	tempfile = {}
	days = []
	mins = 0
	for x in range(len(lines)):
		split = lines[x].split(',')
		if str(split[0]).startswith('a'):
			currentday = split[0]
			days.append(currentday)
			tempfile[currentday + 'days'] = split[0]
			tempfile[currentday + 'mins'] = mins
			tempfile[currentday + 'data'] = ''
			tempfile[currentday + 'data'] += str(lines[x])
		else:
			if len(days) != 0 and x + 1 != len(lines):
				tempfile[str(currentday) + 'mins'] += 1
				tempfile[str(currentday) + 'data'] += str(lines[x])

	return tempfile, days


def minmax(dictionary, dataset):

	lowval = dictionary[str(0) + dataset]
	lowmin = 0
	lowamount = 0
	highval = dictionary[str(0) + dataset]
	highmin = 0
	highamount = 0

	for x in range(390):
		if dictionary[str(x) + dataset] < lowval:
			lowval = dictionary[str(x) + dataset]
			lowmin = x
			lowamount = dictionary[str(x) + 'close']
		if dictionary[str(x) + dataset] > highval:
			highval = dictionary[str(x) + dataset]
			highmin = x
			highamount = dictionary[str(x) + 'close']

	# calculate times (based on market open (6:30 GMT+8)
	today = datetime.datetime.today()
	marketopen = datetime.datetime(today.year, today.month, today.day, 6, 30)
	lowdelta = datetime.timedelta(minutes = int(lowmin))
	highdelta = datetime.timedelta(minutes = int(highmin))
	marketlow = marketopen + lowdelta
	markethigh = marketopen + highdelta


	return lowval, marketlow, lowamount, highval, markethigh, highamount

	






