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

values = ["a","b","c"]

layout = [[sg.Text('Start quarter(\'mm_dd_yyyy\',eg:01_31_2018):')],      
          [sg.Input()],
		  [sg.Text('End quarter(eg,\'mm_dd_yyyy\'):')],
		  [sg.Input()],
		  [sg.Text('One keyword(eg:bond,China...):')],
		  [sg.Input()], 		  
          [sg.RButton('Read'), sg.Exit()]]      

window = sg.Window('Persistent GUI Window').Layout(layout)      

while True:      
    event, start_end = window.Read()      
    if event is None or event == 'Exit':      
        break  
    else:
        print(start_end)
        values[0] = start_end[0]
        values[1] = start_end[1]
        values[2] = start_end[2]
window.Close() 

start_dt = datetime.strptime(values[0], '%m_%d_%Y')+timedelta(days=7)
end_dt = datetime.strptime(values[1], '%m_%d_%Y')
keyword = values[2]

####################################################################################################################
logging.basicConfig(filename='get_news_error.log',level=logging.INFO)

in_name = 'News_source.csv'
out_name = 'News-'+values[0]+'-'+values[1]+'-'+keyword+'.csv'

sg.Popup('Please check file:',out_name) 

with open(in_name,'r') as infile, open(out_name,'a', encoding='utf-8') as outfile:
	for line in infile:
		cells = line.split(',')
		Sat_dt = datetime.strptime(cells[0], '%m/%d/%Y')
		if start_dt <= Sat_dt <= end_dt:
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
				
				if keyword in Mon_news:
					Sat_dt = datetime.strptime(cells[0], '%m/%d/%Y')
					Mon_dt = Sat_dt-timedelta(days=6-i)
					Mon_str = Mon_dt.strftime('%m/%d/%Y')
					to_wrt = Mon_str + "|" + Mon_news+"\n"
					outfile.write(to_wrt)		
			
sg.Popup('Please check file:',out_name)
			