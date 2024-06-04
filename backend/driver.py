from scrape import scrape_rooms, scrape_events
from parse import parse_rooms, parse_events
import os
import pickle
import pandas as pd

def store_rooms(verbose=False) -> None:
    results = []
    queries = ['102984', '103001', '103002']

    # change cwd to the directory of this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    for query in queries:
        # get initial page counts
        text, curr_page, total_pages = scrape_rooms(f'https://25live.collegenet.com/25live/data/clemson/run/list/listdata.json?compsubject=location&page=1&page_size=25&obj_cache_accl=0&query_id={query}&caller=pro-ListService.getData', verbose)
        if verbose:
            print(f'[DEBUG] Query {query} has {total_pages} pages.')
        # scrape each page
        for i in range(1, total_pages + 1):
            text, curr_page, total_pages = scrape_rooms(f'https://25live.collegenet.com/25live/data/clemson/run/list/listdata.json?compsubject=location&page={i}&page_size=25&obj_cache_accl=0&query_id={query}&caller=pro-ListService.getData', verbose)
            if verbose:
                print(f'[DEBUG] {i}/{total_pages}')
            rooms = parse_rooms(text)
            results.extend(rooms)
            if verbose:
                print(f'[DEBUG] Parsed {len(rooms)} rooms.')

    # remove duplicates
    results = pd.DataFrame(results).drop_duplicates(subset=['item_id']).to_dict('records')

    if os.path.exists('./rooms.pkl'):
        if verbose:
            print('[DEBUG] Removing existing rooms.pkl...')
        os.remove('./rooms.pkl')
    with open('./rooms.pkl', 'wb') as f:
        if verbose:
            print(f'[DEBUG] Dumping rooms at {os.path.dirname(os.path.abspath(__file__))}\\rooms.pkl')
        pickle.dump(results, f)

def retrieve_rooms(verbose=False) -> list:
    # change cwd to the directory of this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with open('./rooms.pkl', 'rb') as f:
        if verbose:
            print(f'[DEBUG] Loading rooms from {os.path.dirname(os.path.abspath(__file__))}\\rooms.pkl')
        rooms = pickle.load(f)
    return rooms