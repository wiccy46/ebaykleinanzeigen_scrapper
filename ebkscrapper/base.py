# Base class of the package. 
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from .utils import get_request, convert_date, make_clickable
from warnings import warn
import copy

class EBKScrapper(object):
    
    def __init___(self):
        """Main class of the Ebaykleinanzeigen scrapper. Keep track of item price, 
        see available listings, custom search, keep extendable data record for data mining. 
        
        
        Examples
        --------
        >>> scrapper = EBKScrapper()
        >>> scrapper.payload = {}
        
        """
        # API: https://api.ebay-kleinanzeigen.de/docs/pages/home
        self.base_url = "http://kleinanzeigen.ebay.de/anzeigen/s-suchanfrage.html"
        self.base_payload = {"sortingField": "SORTING_DATE", 
                        "adType": "", "posterType": "", 
                        "pageNum": "1", "action": "find"}
        
        # if not payload:
        #     warn("payload is not set. search is not available, but you can still view past data if any.")
            
        # else:
        #     self.payload = copy(self.base_payload)
        #     self.payload.update(payload)
      

    
    # also have a multiple query version         
    def one_query(query="", where="", maxentries=1000, 
            radius=0, minprice=0, maxprice=1000, categoryid=0):
        """One query and return all search data """
        
        base_payload = copy(self.base_payload)
        base_payload.update({
            'keywords': query, 
            'locationStr': where, 
            'minPrice': str(minprice), 
            'maxPrice': str(maxprice), 
            'categoryId': str(categoryid),
            'radius': str(radius)})

        soup = get_request(base_url, base_payload)
        # Get category info, usually it has multi-level. But we only care the find category:
        # TODO: a better way to do it is to refer category id from the api. 
        category_box = soup.find('div', {'class': 'browsebox-section-body'})
        category = []
        for li in category_box.findAll('li'):
            category.append(li)
        category = category[-1].find('a').text

        results = []
        if soup.text.find('Es wurden leider keine Anzeigen') == -1:
            main_content = soup.find('div', {"id": "srchrslt-content"})
            listing = main_content.find('ul', {"id": "srchrslt-adtable"})
            listing_result = []
            for li in listing.findAll('li'):
                listing_result.append(li)
            data = []
            for lr in listing_result:
                try:
                    title = lr.h2.a.text 
                    href = ebk_url + lr.find('div', {'class': 'aditem-main'}).a['href']   
                    date = lr.find('div', {'class': 'aditem-addon'}).text.replace(' ', '').replace('\n', '')
                    date = convert_date(date)
                    details = lr.find('div', {"class": "aditem-details"})
                    # Convert german locale number string to float. 
                    price = details.strong.text.split(" ")[0]  # Remove the currency sign
                    currency = details.strong.text.split(" ")[-1]
                    price = float(price.replace('.', '')) if '.' in price else float(price)
                    postcode = details.text.replace(' ', '').split('\n')[3]
                    city = details.text.replace(' ', '').split('\n')[4]
                    distance_km = float(details.text.replace(' ', '').split('\n')[5].replace('km', ''))

                    data.append([query, title, category, date, price, postcode, city, distance_km, currency, href])
                except:
                    pass
        df = pd.DataFrame(data, columns=['Query', 'Title', 'Type', 'Date', 'Price', 'Postcode',
                                    'City', 'Distance', 'Currency', 'URL'])
        return df
    
    
                    
    
    
    
    


        