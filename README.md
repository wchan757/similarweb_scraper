# similarweb_scraper

similarweb_scraperis is a python library for scraping similarweb with pywinauto.It also provides some functionality for transforming scraped data into pd dataframe.
   
## Installation and Usage
```bash
### install
1.pip install similarweb-scraper
2.download the similarweb_html_extract.py
3.you need to have a Chrome Browser

### Setup
1 You have to create two folder first 
-short_cutpath  
-data_storage 

2.Change the path of the varialbes(short_cutpath , data_storage) to your local path in the similarweb_html_extract.py

3.Go to the target website in similarweb , create the shortcut and move all the lnk file into the folder of short_cutpath
https://www.laptopmag.com/articles/how-to-create-desktop-shortcuts-for-web-pages-using-chrome

4.Execute similarweb_html_extract.py and it will launch the shortcut and download the html file into the folder of data_storage

5.After you download all the html file, you can scrape the file through similarweb-scraper


### Example for reading the data from html file and extract the traffic of the website
def url_extraction(webname , aboaddress):
   
    """
    go to the website through the api
    """
    ### empty data
    webpage = None
   
    ### open file
    with open(f'{address_ob}{webname}.html', 'r') as filer:
        webpage = filer.read() 
       
    return bs(webpage)

def to_json(need_data):
    """
    change the data as json
    """
    ### temp word
    temp_wrod = None
    preload_json = None
   
    ### find target tg
    for _ in need_data.find_all('script'):
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


def similarweb_get(web , folder):
    web_scrape = scraper()
    soup = url_extraction(web , folder)
    web_json = to_json(soup)
    web_scrape.json_storage = web_json
    
    ### get target
    df = web_scrape.metrics_to_df('monthly_traffic_data')
    
    ### retrun
    return df

if __name__ == '__main__':
    web_name = 'your_html_file_name'
    html_folder_path = 'your_html_file_folder_path'
    simweb_scraper = similarweb_get(web_name , html_folder_path)   

```
## metrics_type name :
Apart from'monthly_traffic_data', you can try other metrics as well
'country_share',
'traffic_share',
 engagement',
 More function will be available soon

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
