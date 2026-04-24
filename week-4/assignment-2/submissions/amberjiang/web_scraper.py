'''
web_scraper.py - web scraping

1. Checks IMDb's robots.txt
2. Scrapes movie pages for ratings and review counts
3. Implements rate limiting (minimum 2 seconds between requests)
4. Uses appropriate User-Agent header
5. Handles missing data gracefully
6. Saves scraped data to JSON files
7. Logs all scraping activity

Key Functions:
def check_robots_txt() -> bool
def scrape_movie_page(imdb_id: str) -> Dict
def scrape_multiple_movies(imdb_ids: List[str]) -> List[Dict]
'''

import requests
import os
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup
import time
import json
from typing import Dict, List
import logging


class IMDbScraper:
    def __init__(self, delay: float = 2.0):
        self.delay = delay
        self.session = requests.Session() # create a Session object to persist TCP connection, cookies, config across requests
        self.last_request_time = 0
        self.main_request_interval = max(delay, 2.0) # ensure minimum 2 seconds between requests 
        self.session.headers.update({
            'User-Agent': 'UCLA STAT418 Student - amberjiang@g.ucla.edu'
        })
        self.can_scrape = False

        os.makedirs('logs', exist_ok=True)
        os.makedirs('data', exist_ok=True)

        logging.basicConfig(
            filename='logs/web_scraper.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    def _rate_limit(self):
        """Ensure rate limits are not exceeded"""
        elapsed = time.time() - self.last_request_time # time between current and last request time 
        if elapsed < self.main_request_interval: # if the elapsed time is less than the main request interval 
            time.sleep(self.main_request_interval - elapsed) # sleep for the rest of the time until the main request interval time
        self.last_request_time = time.time() # set the last request time to now
    
    def check_robots_txt(self) -> bool:
        """Check robots_txt to see whether IMDb allows scraping movie title pages""" 
        try:
            rp = RobotFileParser()
            robots_url = 'https://www.imdb.com/robots.txt'
            test_url = f'https://www.imdb.com/title/'

            rp.set_url(robots_url)
            rp.read()

            can_fetch = rp.can_fetch(self.session.headers['User-Agent'], test_url)
            logging.info(f'IMDb robots.txt check result: {can_fetch}')

            return can_fetch

        except Exception as e:
            logging.error(f'Error checking robots.txt: {e}')
            return False

    def scrape_movie_page(self, imdb_id: str) -> Dict:
        """Scrape IMDb movie page"""
        
        #Check robots.txt
        if not self.can_scrape:
            if not self.check_robots_txt():
                logging.warning(f'Skipping {imdb_id} because robots.txt disallows scraping')
                return {'imdb_id': imdb_id, 'error': 'robots.txt disallows scraping'}
            else:
                self.can_scrape = True

        self._rate_limit()

        url = f'https://www.imdb.com/title/{imdb_id}/'

        try:
            response = self.session.get(url, timeout=10) 
            # timeout in case the server is not responding in a timely manner; without, code may hang for awhile
            # connect timeout = 10 -> number of seconds Requests will wait for client to establish a connection to remote machine
            # read timeout = 10 -> number of seconds the client will wait for the server to send a response

            response.raise_for_status() # checks HTTP status code of a response and raises HTTPError if the status is 4xx or 5xx

            soup = BeautifulSoup(response.content,'html.parser') # use BeautifulSoup instance to parse HTML content

            rating_data = soup.find('script', type='application/ld+json')
            rating_json = json.loads(rating_data.string) if rating_data else {}
            metascore_data = soup.find('script', id='__NEXT_DATA__')
            metascore_json = json.loads(metascore_data.string) if metascore_data else {}

            #Extract data
            data = {
                'imdb_id': imdb_id,
                'rating': rating_json.get('aggregateRating',{}).get('ratingValue',None),
                'num_reviews': rating_json.get('aggregateRating', {}).get('ratingCount', None),
                'metascore': metascore_json.get('props',{}).get('pageProps',{}).get('aboveTheFoldData', {}).get('metacritic', {}).get('metascore', {}).get('score', None)
            }

            logging.info(f'Successfully scraped {imdb_id}')
            return data

        except Exception as e:
            logging.error(f'Error scraping {imdb_id}: {e}')
            return {'imdb_id':imdb_id, 'error':str(e)}

    def scrape_multiple_movies(self, imdb_ids: List[str]) -> List[Dict]:
        """Scrape multiple IMDb movie pages"""

        scraped_movies = []
        for imdb_id in imdb_ids:
            try:
                movie_data = self.scrape_movie_page(imdb_id=imdb_id)
                scraped_movies.append(movie_data)
            except Exception as e:
                logging.error(f'Error scraping {imdb_id}: {e}')
                scraped_movies.append({'imdb_id':imdb_id, 'error':str(e)})
        
        #Save scraped data to JSON file
        filepath = os.path.join('data', 'imdb_scraped_data.json')
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(scraped_movies, f, indent=4)
            logging.info(f'Saved scraped data to {filepath}')
        except Exception as e:
            logging.error(f'Error saving data to JSON: {e}')

        return scraped_movies
