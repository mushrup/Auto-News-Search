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

in_name = 'News.csv'
out_name = 'News-'+values[0]+'-'+values[1]+'-'+keyword+'.csv'

with open(in_name,'r', encoding='utf-8') as infile, open(out_name,'a', encoding='utf-8') as outfile:
	for line in infile:
		cells = line.split('|')
		Sat_dt = datetime.strptime(cells[0], '%m/%d/%Y')
		if start_dt <= Sat_dt <= end_dt:
			Mon_news = cells[1]
			if keyword in Mon_news:
				to_wrt = cells[0] + "|" + Mon_news
				outfile.write(to_wrt)		
			
sg.Popup('Please check file:',out_name)
			