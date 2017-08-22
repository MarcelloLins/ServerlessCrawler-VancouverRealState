from __future__ import print_function

import logging

import requests
from utils import Utils
from dynamo_client import DynamoClient
from parser import Parser
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamo_client = DynamoClient()

def bootstrap_cities_page(event, context):
    home_page_url = os.environ['home_page']
    target_province = "-" + os.environ['target_province'].lower().strip()

    logging.info('Starting Bootstrapper. Executing request for neighborhood pages')
    response = requests.get(home_page_url)

    if response.status_code == requests.codes.ok:
        search_page = response.text
        
        # Extracting neighborhood urls from initial page
        neighborhood_urls = Parser.extract_neighborhood_urls(search_page, target_province)

        if not neighborhood_urls:
            logging.fatal('Found no neighborhood urls on initial page. Scraper is most likely broken. Aborting')
            return

        logging.info('Found %d neighborhood urls on initial page' % len(neighborhood_urls))

        # Iterating over Urls
        processed_neighborhoods = 1
        total_neighborhoods = len(neighborhood_urls)
        processed_sub_neighborhoods = 0
        for neighborhood_url in neighborhood_urls:
            logging.info('Processing Neighborhood %d out of %d - %s' % (processed_neighborhoods, total_neighborhoods, neighborhood_url))
            processed_neighborhoods = processed_neighborhoods + 1

            response = requests.get(neighborhood_url)
            if response.status_code != requests.codes.ok:
                logging.warn('Get Request for Page returned NOT OK [%s]' % response.status_code)
                continue

            search_page = response.text
            sub_neighborhood_urls = Parser.extract_neighborhood_urls(search_page, target_province)
            processed_sub_neighborhoods = processed_sub_neighborhoods + len(sub_neighborhood_urls)

            if not sub_neighborhood_urls:
                logging.fatal('Found no sub-neighborhood urls for this neighborhood')
                continue

            logging.info('Found %d sub-neighborhoods' % len(sub_neighborhood_urls))

            # Adding Urls to Dynamo
            dynamo_client.write_batch(sub_neighborhood_urls)
        logging.info('Finished Processing Pages. A Total of %d sub-neighborhoods were saved for processing' % processed_sub_neighborhoods)