import requests
import time
import json

def scrape_rooms(url: str, sleep=10, verbose=False) -> tuple:
    if verbose:
        print('[DEBUG] Sleeping for 10 seconds...')
    time.sleep(sleep)
    response = json.loads(requests.get(url).text)
    curr_page = response.get('page')
    total_pages = response.get('rows')[0]['pages']
    return response.get('rows'), curr_page, total_pages

def scrape_events(url: str, sleep=10, verbose=False):
    if verbose:
        print('[DEBUG] Sleeping for 10 seconds...')
    time.sleep(sleep)
    response = json.loads(requests.get(url).text)
    return response.get('root').get('events')