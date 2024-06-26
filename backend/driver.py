from .scrape import scrape_rooms, scrape_events
from .parse import parse_rooms, parse_events
import os
import pickle
import pandas as pd
from typing import Optional
import datetime

class Driver:
    def __init__(self, sleep=10, verbose=False):
        if verbose:
            print('[DEBUG] Driver instance created.')
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.sleep = sleep
        self.verbose = verbose
        self.status = 'idle'
        if not os.path.exists('./rooms.pkl'):
            self._rooms = []
        else:
            self._rooms = self.__retrieve_rooms__(self.verbose)
        if not os.path.exists('./events.pkl'):
            self._events = []
        else:
            self._events = self.__retrieve_events__(self.verbose)

    def __del__(self):
        if self.verbose:
            print('[DEBUG] Driver instance deleted.')

    def __store_rooms__(self, sleep=10, verbose=False) -> None:
        results = []
        queries = ['102984', '103001', '103002']

        for query in queries:
            # get initial page counts
            text, curr_page, total_pages = scrape_rooms(f'https://25live.collegenet.com/25live/data/clemson/run/list/listdata.json?compsubject=location&page=1&page_size=25&obj_cache_accl=0&query_id={query}&caller=pro-ListService.getData', sleep, verbose)
            if verbose:
                print(f'[DEBUG] Query {query} has {total_pages} pages.')
            # scrape each page
            for i in range(1, total_pages + 1):
                text, curr_page, total_pages = scrape_rooms(f'https://25live.collegenet.com/25live/data/clemson/run/list/listdata.json?compsubject=location&page={i}&page_size=25&obj_cache_accl=0&query_id={query}&caller=pro-ListService.getData', sleep, verbose)
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

    def __retrieve_rooms__(self, verbose=False) -> list:
        with open('./rooms.pkl', 'rb') as f:
            if verbose:
                print(f'[DEBUG] Loading rooms from {os.path.dirname(os.path.abspath(__file__))}\\rooms.pkl')
            rooms = pickle.load(f)
        return rooms

    def __store_events__(self, start: Optional[datetime.datetime], end: Optional[datetime.datetime], sleep=10, verbose=False) -> None:
        results = []
        queries = ['102984', '103001', '103002']

        if start is None:
            if verbose:
                print('[DEBUG] No start date provided. Using today.')
            start = datetime.datetime.now()
        # get each date in the selected day's week
        sunday = start - datetime.timedelta(days=(start.weekday() + 1) % 7)
        dates = [sunday + i * datetime.timedelta(days=1) for i in range(7)]
        if end is None:
            if verbose:
                print('[DEBUG] No end date provided. Using the end of the week.')
            end = dates[-1]
        
        # format start and end dates
        start = start.strftime('%Y-%m-%d')
        end = end.strftime('%Y-%m-%d')
        if verbose:
            print(f'[DEBUG] Getting events from {start} to {end}...')

        for query in queries:
            text = scrape_events(f'https://25live.collegenet.com/25live/data/clemson/run/home/calendar/calendardata.json?mode=pro&obj_cache_accl=0&start_dt={start}&end_dt={end}&comptype=calendar&sort=evdates_event_name&compsubject=location&spaces_query_id={query}&caller=pro-CalendarService.getData', sleep, verbose)
            events = parse_events(text)
            results.extend(events)
            if verbose:
                print(f'[DEBUG] Parsed {len(events)} events.')

        # remove duplicates
        results = pd.DataFrame(results).drop_duplicates(subset=['event_id']).to_dict('records')

        if os.path.exists('./events.pkl'):
            if verbose:
                print('[DEBUG] Removing existing events.pkl...')
            os.remove('./events.pkl')
        with open('./events.pkl', 'wb') as f:
            if verbose:
                print(f'[DEBUG] Dumping events at {os.path.dirname(os.path.abspath(__file__))}\\events.pkl')
            pickle.dump(results, f)

    def __retrieve_events__(self, verbose=False) -> list:
        with open('./events.pkl', 'rb') as f:
            if verbose:
                print(f'[DEBUG] Loading events from {os.path.dirname(os.path.abspath(__file__))}\\events.pkl')
            events = pickle.load(f)
        return events

    def refresh_rooms(self):
        self.status = 'running'
        self.__store_rooms__(self.sleep, self.verbose)
        self._rooms = self.__retrieve_rooms__(self.verbose)
        self.status = 'idle'

    def refresh_events(self, start: Optional[datetime.datetime], end: Optional[datetime.datetime]):
        self.status = 'running'
        self.__store_events__(start, end, self.sleep, self.verbose)
        self._events = self.__retrieve_events__(self.verbose)
        self.status = 'idle'

    def get_rooms(self) -> list:
        return self._rooms
    
    def get_events(self) -> list:
        return self._events