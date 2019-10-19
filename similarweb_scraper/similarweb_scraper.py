from proxycrawl.proxycrawl_api import ProxyCrawlAPI
from bs4 import BeautifulSoup as bs
import json
import re
import pandas as pd 
from datetime import datetime
import time
from string import Template
from iso3166 import countries

class similarweb_to_pandas():
    """
    it is used for changing the data into pandas format
    """        
    def to_df_mode(self, mode, scraped_data ,latest_date, raw_data , website):
        """
        determine which data you want to extract
        mode = data  to transform
        scpraed_data = date for data extraction
        latest_date = latest date from similarweb
        website = name of the website
        """
        ### empty data
        data = None
        
        ### fucntion to go
        if mode == 'country_share':
            data = self.counrty_share(scraped_data , latest_date , raw_data,website)
            return data
        
        elif mode == 'traffic_share':
            data = self.traffic_share(scraped_data , latest_date , raw_data,website)
            return data
        
        elif mode == 'engagement':
            data = self.engagement(scraped_data , latest_date , raw_data,website)
            return data
        
        elif mode == 'monthly_traffic_data':
            data = self.monthly_traffic_data(scraped_data , latest_date , raw_data,website)
            return data
        
        else:
            print('input mode is not found , plx check')
            return None
        
    
    def country_share(self,scraped_date , latest_date , json_d , webname):
        """
        get the top countres_share
        """
        ### empty data 
        data = None
        
        ### trasnform the data
        data = pd.DataFrame(data = {
            'countries':[countries.get(str(_[0]).replace('.0','')).name for _ in json_d['overview']['TopCountryShares']],
            'share':[_[1] for _ in json_d['overview']['TopCountryShares']],
            'website' : webname,
            'scrpaed_date' : scraped_date,
        'similarweb_updated_date' : latest_date})
        
        ### return
        return data
    
    def traffic_share(self,scraped_date , latest_date , json_d , webname):
        """
        get the traffic share
        """
        ### empty data 
        data = None
        
        ### transfomr the data
        data = pd.DataFrame(data = {
            'traffic_source':[_ for _ in json_d['overview']['TrafficSources']],
            'ratio':[json_d['overview']['TrafficSources'][_] for _ in json_d['overview']['TrafficSources']],
            'website' : webname,
            'scrpaed_date' : scraped_date,
        'similarweb_updated_date' : latest_date})
        
        ### return 
        return data
    
    def monthly_traffic_data(self,scraped_date , latest_date , json_d , webname):
        """
        get the traffic data 
        """
        ### empty data 
        data = None
        
        ### transfomr the data
        data = pd.DataFrame(data = {
            'estimate_traffic':[json_d['overview']['EngagementsSimilarweb']['WeeklyTrafficNumbers'][_] for _ in json_d['overview']['EngagementsSimilarweb']['WeeklyTrafficNumbers']],                    
            'website' : webname,
            'scrpaed_date' : scraped_date,
        'month_for_traffic' :  [_ for _ in json_d['overview']['EngagementsSimilarweb']['WeeklyTrafficNumbers']]})
        
        
        ### return 
        return data

   
    def engagement(self,scraped_date , latest_date , json_d , webname):
        """
        get the engagement data
        """
        ### empty data
        data = None
        
        ### transform the data
        data = pd.DataFrame(data ={
                    'website': webname,
                   'scrpaed_date': scraped_date,
                    'date for metrics' :latest_date,
                   'type':[_ for _ in json_d['overview']['EngagementsSimilarweb']][:3],
                   'value': [json_d['overview']['EngagementsSimilarweb'][_] for _ in json_d['overview']['EngagementsSimilarweb']][:3]})
        
        ### return
        return data
    
class scraper():
    """
    it is used for scraping similar web page through the service of proxycrawl(https://proxycrawl.com)
    First 1000 requests is free and so far it has been able to bypass the distil prtection so far
    
    """
    def __init__(self,similar_web_prefix = 'https://www.similarweb.com/website/'):
        """
        similar_web_prefix : similar web prefix(default = 'https://www.similarweb.com/website/')
        """
        self.crawler = None
        self.json_storage = None
        self.web_name = None
        self.web_template = Template(similar_web_prefix+'$webname')
        self.scraped_date = str(datetime.today())[:10]
        self.similar_web_latest_date = None
        self.og_soup = None
        
    def login(self , api_key , connect_test_url = 'http://www.hk.yahoo.com/'):
        """
        login the proxycrawl
        api_key = the normral api token from proxycrawl.com
        connect_test_url = website for checking connection to proxycrawl default = http://www.hk.yahoo.com/'
        """
        ### connection status
        connection_test = None
        
        ### create the api connection first
        api_caller = ProxyCrawlAPI({ 'token': api_key })
        
        ### check the conenction
        connection_test =  api_caller.get('http://www.hk.yahoo.com/')
        assert connection_test['status_code'] != 403 , 'login test with hk yahoo fail , your api key may be invalid plx check'
        
        ### return the connector
        self.crawler = api_caller
        
    def webpage_scrape(self ,website_suffix,attempt = 3):
        """
        it scrape the webpage inforamtion into json format
        website_suffix = target website suffix e.g :hk.yahoo.com
        attempt = time for re-retry it failed. default = 3
        """
        ### check whether it is logined and web suffic format
        assert self.crawler != None , 'plx login first'
        assert type(website_suffix) == str , 'website_suffix has to be str'
        
        ### get api handler and create tg url
        api_handler = self.crawler
        tg_url = self.web_template.substitute(webname = website_suffix)
        soup = None
        
        ### start scraping
        for trial in range(attempt):
            response = api_handler.get(tg_url)
            if response['status_code'] == 200:
                break
        
        ### testing whether it sucessfully scrape the page
        assert response['status_code'] == 200 , 'fail to scrape the page, plx check whether the web suffix is correct or similarweb block the acess'
        
        ### scape the page as json and save the soup 
        self.og_soup = response['body']
        try:
            soup = self.bs_to_json(response['body'])
        except:
            print('failed in tranfomring html code into json stage , the target webiste may not have sufficient data or access to similar web being block plx check the html code through similar_scraper.og_soup')
        
        ### save the json data and record the web name
        self.json_storage = soup
        self.web_name = website_suffix
        self.scraped_date = str(datetime.today())[:10]
        self.similar_web_latest_date = str(soup['overview']['Date'])[:10]

        ### return
        return None
        
    def bs_to_json(self ,soup_raw):
        """
        save the data as json
        """
        ### temp word
        temp_wrod = None
        preload_json = None
        souper = bs(soup_raw)
    
        ### find target tg
        for _ in souper.find_all('script'):
            if 'Sw.preloadedData' in _.text:
                preload_json = _

        ### find the tg json
        for _ in preload_json.text.splitlines():
            if 'Sw.preload' in _:
                temp_wrod = _

        ### jsonize
        data = temp_wrod.split('=', 1)[1].strip(' ;') 
        data = json.loads(data) 

        ### return json
        return data
    
    def metrics_to_df(self,metrics_type):
        """
        extract the target data and return with pd dataframe
        metrics_type = metrics to extract ( 1.country_share ,2.traffic_share , 3.engagement,4.monthly_traffic_data)
        
        todo : add more metrics to extract
        """
        ### empty df
        df = None
        
        ### check whether data is collected
        assert self.json_storage is not None , 'no data has been scraped yet'
        
        ### extract declare
        similarweb_extractor = similarweb_to_pandas()
        
        ### required_data
        date_scraped = self.scraped_date 
        similarweb_date =  self.similar_web_latest_date
        json_data = self.json_storage
        webpage = self.web_name
        mode_type = metrics_type
        
        ### extract start
        df = similarweb_extractor.to_df_mode(mode_type,date_scraped,similarweb_date,json_data,webpage)
        
        ### return data
        if type(df) == None:
            return None
        else:
            return df
        
      
        
