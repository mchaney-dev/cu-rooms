import requests
import time
import json

def scrape_rooms(url: str) -> tuple:
    # debug
    print('Sleeping for 10 seconds...')
    
    time.sleep(10) # Be nice to the server
    response = json.loads(requests.get(url).text)
    curr_page = response.get('page')
    total_pages = response.get('rows')[0]['pages']
    return response.get('rows'), curr_page, total_pages