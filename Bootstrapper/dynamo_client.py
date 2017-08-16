from __future__ import print_function

import logging
import boto3
import time
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DynamoClient:
	def __init__(self):
		self.region_name = os.environ['region_name']
		self.table_name = os.environ['table_name']
		self.dynamo_client = boto3.resource('dynamodb', region_name=self.region_name)
		self.current_table = self.dynamo_client.Table(self.table_name)
	
	def write_batch(self, items):
		with self.current_table.batch_writer() as batch:
			for item in items:
				batch.put_item(
						Item={'listing_url': item, 'processing_date': int(time.time()) + 120} # 2 minutes in the future
					)