#! /usr/bin/env python

"""plot market prices"""

import os,sys
from optparse import OptionParser
import datetime as dt
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as mp
import modules as mod

from IPython import embed
#embed() # this call anywhere in your program will start IPython

np.set_printoptions(precision=3, threshold=50, linewidth=80)

def chooseYear(dates,prices,year):
	newdates,newprices=[],[]
	for i in xrange(len(dates)):
		if dates[i].year==year:
			newdates.append(dates[i])
			newprices.append(prices[i])
	return newdates,newprices

def main():
	print 'here starts main program'

parser = OptionParser()
(options, args) = parser.parse_args()

if len(args)<1:
	raise NameError("Usage: %s /some/path")
else: fname=args[0]

lines = [line.strip() for line in open(fname)]

dates,prices=[],[]
for line in lines:
	date = line.split('\t')[0]
	date = date[:6]+'20'+date[6:]
	date = dt.datetime.strptime(date,'%d.%m.%Y')
	price=''
	for item in line.split('\t')[1]:
		if item=='.': continue
		elif item ==',': price+='.'	
		else:	price+=item
	dates.append(date)
	prices.append(float(price))
dates = np.array(dates)	
prices = np.array(prices)	

mp.figure(1)
ax1=mp.subplot(111)
ax1.plot(dates,prices,ls='-',c='r')
ax1.set_title(fname[6:-4])
ax1.set_ylabel('price')
ax1.set_xlabel('time')

mp.figure(2)
ax2=mp.subplot(111)
i,year=0,2013
colors = mod.colorlist()
while year>=2008:
	newdates,newprices = chooseYear(dates,prices,year)
	days=[]
	for item in newdates:
		days.append(item.strftime('%j'))
	ax2.plot(days,newprices,ls='-',c=colors[i],label=str(year))
	i+=1
	year-=1
ax2.legend(loc='lower right')
ax2.set_title(fname[6:-4])
ax2.set_ylabel('price')
ax2.set_xlabel('days of year')
#~ mp.savefig('alpha.pdf')
mp.show()
	
	
	
	
