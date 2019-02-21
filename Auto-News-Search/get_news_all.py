from urllib import request
from lxml import etree
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import csv
import random
import time
import logging
import PySimpleGUI as sg
from fake_useragent import UserAgent   

in_name = 'News_source.csv'
out_name = 'News.csv'

with open(in_name,'r') as infile, open(out_name,'a', encoding='utf-8') as outfile:
	for line in infile:
		cells = line.split(',')
		url = "https://www.seekingalpha.com"+cells[2]
		print(url)
		
		#"https://seekingalpha.com/article/4228513-wall-street-breakfast-moved-markets-week"

		my_headers=[
		"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
		]
		
		headers = {}
		#headers['User-Agent'] = UserAgent().random
		headers['User-Agent'] = random.choice(my_headers)
		print(headers)
		req = request.Request(url, headers = headers)
		req = request.urlopen(req).read().decode("utf8")
		sel=etree.HTML(req)
		for i in range(1,6):
			try:
				time.sleep(0.5)
				size = len(sel.xpath(r"//div/p[@class='wsb_pb']["+str(i)+"]/text()"))
				Mon_news = sel.xpath(r"//div/p[@class='wsb_pb']["+str(i)+"]/strong/a/text()")[0]
				for j in range(size):
					Mon_news = Mon_news+sel.xpath(r"//div/p[@class='wsb_pb']["+str(i)+"]/text()")[j]
			except Exception as e:
				logging.error(" Type1 error at "+str(datetime.now())+" on Day "+str(i))
				size = len(sel.xpath(r"//div[@class='wsb_mb']/div/text()"))
				Mon_news = ""
				for j in range(size-1):
					Mon_news = Mon_news+sel.xpath(r"//div[@class='wsb_mb']/div/text()")[j+1]
					
			Sat_dt = datetime.strptime(cells[0], '%m/%d/%Y')
			Mon_dt = Sat_dt-timedelta(days=6-i)
			Mon_str = Mon_dt.strftime('%m/%d/%Y')
			to_wrt = Mon_str + "|" + Mon_news+"\n"
			outfile.write(to_wrt)		
			
sg.Popup('Please check file:',out_name)
			