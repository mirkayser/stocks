#! /usr/bin/env python

"""create rsl ranking"""

import urllib,urllib2
import os,sys
import re
import datetime as dt
from optparse import OptionParser
import numpy as np
import matplotlib.pyplot as mp
import modules as mod
from pyik.performance import *

from IPython import embed
#embed() # this call anywhere in your program will start IPython

@cached
def getData(url):
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }
	req = urllib2.Request(url, headers=headers)
	response = urllib2.urlopen(req)
	page = response.read()
	date = dt.date.today()
	return page,date

class Stock(object):
	
	def __init__(self,id,name,url):
		self.name = name
		self.id = id
		self.url = url
		self.date=dt.date.today()
		
	def AddRSL30(self,rsl):
		tmp=''
		for i in rsl:
			if i==',':tmp+='.'
			else: tmp+=i
		self.rsl30 = float(tmp)	

	def AddRSL250(self,rsl):
		tmp=''
		for i in rsl:
			if i==',':tmp+='.'
			else: tmp+=i
		self.rsl250 = float(tmp)			


def main():
	print 'here starts main program'

liste =[[0,'adidas','http://www.onvista.de/aktien/Adidas-Aktie-DE000A1EWWW0'],
		[1,'allianz','http://www.onvista.de/aktien/Allianz-Aktie-DE0008404005'],
		[2,'basf','http://www.onvista.de/aktien/BASF-Aktie-DE000BASF111'],
		[3,'bayer','http://www.onvista.de/aktien/Bayer-Aktie-DE000BAY0017'],
		[4,'beiersdorf','http://www.onvista.de/aktien/Beiersdorf-Aktie-DE0005200000'],
		[5,'bmw','http://www.onvista.de/aktien/BMW-Aktie-DE0005190003'],
		[6,'commerzbank','http://www.onvista.de/aktien/Commerzbank-Aktie-DE000CBK1001'],
		[7,'continental','http://www.onvista.de/aktien/Continental-Aktie-DE0005439004'],
		[8,'daimler','http://www.onvista.de/aktien/Daimler-Aktie-DE0007100000'],
		[9,'deutsche_bank','http://www.onvista.de/aktien/Deutsche-Bank-Aktie-DE0005140008'],
		[10,'deutsche_boerse','http://www.onvista.de/aktien/Deutsche-Boerse-Aktie-DE0005810055'],
		[11,'lufthansa','http://www.onvista.de/aktien/Lufthansa-Aktie-DE0008232125'],
		[12,'post','http://www.onvista.de/aktien/Deutsche-Post-Aktie-DE0005552004'],
		[13,'telekom','http://www.onvista.de/aktien/Deutsche-Telekom-Aktie-DE0005557508'],
		[14,'eon','http://www.onvista.de/aktien/EON-Aktie-DE000ENAG999'],
		[15,'fresenius','http://www.onvista.de/aktien/Fresenius-Aktie-DE0005785604'],
		[16,'fmc','http://www.onvista.de/aktien/Fresenius-Medical-Care-Aktie-DE0005785802'],
		[17,'heidelbergcement','http://www.onvista.de/aktien/HeidelbergCement-Aktie-DE0006047004'],
		[18,'henkel','http://www.onvista.de/aktien/Henkel-Aktie-DE0006048432'],
		[19,'infineon','http://www.onvista.de/aktien/Infineon-Aktie-DE0006231004'],
		[20,'k+s','http://www.onvista.de/aktien/K+S-Aktie-DE000KSAG888'],
		[21,'lanxess','http://www.onvista.de/aktien/Lanxess-Aktie-DE0005470405'],
		[22,'linde','http://www.onvista.de/aktien/Linde-Aktie-DE0006483001'],
		[23,'merck','http://www.onvista.de/aktien/Merck-Aktie-DE0006599905'],
		[24,'muenchener','http://www.onvista.de/aktien/Muenchener-Rueck-Aktie-DE0008430026'],
		[25,'rwe','http://www.onvista.de/aktien/RWE-Aktie-DE0007037129'],
		[26,'sap','http://www.onvista.de/aktien/SAP-Aktie-DE0007164600'],
		[27,'siemens','http://www.onvista.de/aktien/Siemens-Aktie-DE0007236101'],
		[28,'thyssen','http://www.onvista.de/aktien/ThyssenKrupp-Aktie-DE0007500001'],
		[29,'vw','http://www.onvista.de/aktien/VW-Aktie-DE0007664039']
		]



dax30=[]
ids,rsl30s,rsl250s = [],[],[]
for i,item in enumerate(liste):
	print 'getting data ',i+1,'/30'
	
	stock = Stock(item[0],item[1],item[2])
	page,date = getData(stock.url)

	a,b=re.split('RSL-Levy 30T</th><td class="ZAHL">',page)
	stock.AddRSL30(b[:4]) 
	a,b=re.split('RSL-Levy 250T</th><td class="ZAHL">',page)
	stock.AddRSL250(b[:4])
	
	ids.append(stock.id)
	rsl30s.append(stock.rsl30)
	rsl250s.append(stock.rsl250)
	 
	dax30.append(stock)
	
array = np.array(zip(ids,rsl30s,rsl250s),dtype=[("id",int),("rsl30",float),("rsl250",float)])

date = date.strftime('%d-%m-%Y')
fname = 'rsl-ranking_'+date+'.npy'
np.save(fname,array)

breakpoint=10

print '\nRSL 30T'
array['rsl30']=array['rsl30']*-1
array.sort(order='rsl30') 
array['rsl30']=array['rsl30']*-1
for i,item in enumerate(array):
    print i+1, dax30[item['id']].name, item['rsl30']#,item['rsl250']
    if i==breakpoint: break

print '\nRSL 250T'
array['rsl250']=array['rsl250']*-1
array.sort(order='rsl250')
array['rsl250']=array['rsl250']*-1
for i,item in enumerate(array):
    print i+1, dax30[item['id']].name, item['rsl250']#, item['rsl30']
    if i==breakpoint:break




