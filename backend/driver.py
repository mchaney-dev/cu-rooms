from scrape import scrape_rooms
from parse import parse_rooms
import os

queries = ['102984', '103001', '103002']

# change cwd to the directory of this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

for query in queries:
    # get initial page counts
    text, curr_page, total_pages = scrape_rooms(f'https://25live.collegenet.com/25live/data/clemson/run/list/listdata.json?compsubject=location&page=1&page_size=25&obj_cache_accl=0&query_id={query}&caller=pro-ListService.getData')
    # scrape each page
    for i in range(1, total_pages + 1):
        text, curr_page, total_pages = scrape_rooms(f'https://25live.collegenet.com/25live/data/clemson/run/list/listdata.json?compsubject=location&page={i}&page_size=25&obj_cache_accl=0&query_id={query}&caller=pro-ListService.getData')
        entries = parse_rooms(text)
        # create file if it does not exist
        if not os.path.exists(f'./rooms_{query}.txt'):
            open(f'./rooms_{query}.txt', 'w').close()
        # append to file
        with open(f'./rooms_{query}.txt', 'a') as f:
            for entry in entries:
                f.write(f'{entry}\n')
        f.close()