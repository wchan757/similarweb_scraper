# similarweb_scraper

similarweb_scraperis is a python library for scraping similarweb with proxycrawl api and it can bypass the distil projection so far. It also provides some functionality for transforming scraped data into pd dataframe.
   
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install similarweb-scraper

## Usage

from similarweb_scraper import scraper

### get the website html
web_scrape = scraper()
web_scrape.login(#api key from proxycrawl.com)
web_scrape.webpage_scrape(#websit e.g: hk.yahoo.com)

### get the html code
soup = web_scrape.og_soup
### get the html code as json format
web_json = web_scrape.json_storage

### get data into json format
df = web_scrape.metrics_to_df(#str(metrics_type))
##metrics_type name :
#'country_share',
#'traffic_share',
# engagement',
#'monthly_traffic_data'
# more function will be available soon
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
