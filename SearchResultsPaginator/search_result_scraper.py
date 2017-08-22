from __future__ import print_function

import logging

import requests
from utils import Utils
from dynamo_client import DynamoClient
from parser import Parser

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamo_client = DynamoClient()

def paginate_through_search_page(event, context):
    records = event['Records']
    logger.info('Received Dynamo Batch of %d events. Initiating Scraping' % len(records))

    for record in records:

        # Processing only 'INSERT events'
        if 'INSERT' not in record['eventName']:
            logger.info('Found %s dynamo event. Skipping it' % record['eventName'])
            continue

        search_page_url = record['dynamodb']['Keys']['neighborhood_url']['S']
        logger.info('Extracting Listing Urls from Search Page: %s' % search_page_url)

        response = requests.get(search_page_url)
        if response.status_code == requests.codes.ok:
            search_page = response.text

            # Extracting Listings from Home Page
            urls = Parser.extract_listing_urls(search_page)

            if len(urls) == 0:
                logger.info('Found no listings for this area.')
                return

            # Adding Urls to Dynamo
            dynamo_client.write_batch(urls)

            # Extracting the index of the last page
            max_search_pages = Parser.extract_search_pages_count(search_page)

            if not max_search_pages:
                logger.info('Search has only one page worth of results.')
                return

            logger.info('Total Number of Pages Found: %s' % max_search_pages)
            for page_idx in range(1, int(max_search_pages)):
                next_page = page_idx + 1

                # Assembling URL of the next page
                next_page_url = Utils.get_next_page_url(search_page_url, next_page)
                logger.info('Parsing page: %d (%s)' % (next_page, next_page_url))

                # Get Request for next page
                response = requests.get(next_page_url)

                # Sanity Check
                if response.status_code != requests.codes.ok:
                    logger.error('Error while getting page %s [STATUS CODE: %d]' % (next_page_url, response.status_code))
                    continue

                # Extracting Listings from current page
                urls = Parser.extract_listing_urls(response.text)

                # Adding Urls to Dynamo
                dynamo_client.write_batch(urls)