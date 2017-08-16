from __future__ import print_function

from datetime import datetime
import logging
import requests
import os

from parser import Parser
import pymysql

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def process_dynamo_stream(event, context):
    records = event['Records']
    logger.info('Received Dynamo Batch of %d events. Initiating Scraping' % len(records))

    # Creating MySQL Connection
    connection = pymysql.connect(host=os.environ['host'],
                                 user=os.environ['user'],
                                 password=os.environ['password'],
                                 db=os.environ['db'],
                                 charset=os.environ['charset'],
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            for record in records:

                # Processing only 'INSERT events'
                if 'INSERT' not in record['eventName']:
                    logger.info('Found %s dynamo event. Skipping it' % record['eventName'])
                    continue

                current_url = record['dynamodb']['Keys']['listing_url']['S']
                logger.info('Scraping Url: %s' % current_url)

                response = requests.get(current_url)
                if response.status_code != requests.codes.ok:
                    logger.error('Request for page failed with code %s' % str(response.status_code))
                    continue

                # Parsing HTML
                listing_page_html = response.text
                listing_dict = Parser.extract_listing_data(listing_page_html)

                # Adding missing data to the dictionary
                listing_dict['capture_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                listing_dict['url'] = current_url

                logger.info('Finished Processing Listing. Inserting into MYSQL')
                placeholders = ', '.join(['%s'] * len(listing_dict))
                columns = ', '.join(listing_dict.keys())
                insert_statement = 'INSERT INTO real_state.rew_ca (%s) VALUES(%s)' % (columns, placeholders)
                cursor.execute(insert_statement, listing_dict.values())
                connection.commit()
    except Exception as ex:
        logging.exception('Error Processing Listing')
    finally:
        connection.close()