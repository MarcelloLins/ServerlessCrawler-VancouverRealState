from __future__ import print_function

import re
from utils import Utils
from bs4 import BeautifulSoup
from utils import Utils

class Parser:

	@staticmethod
	def extract_address(html_map):
		key_node = html_map.find('span', itemprop='streetAddress')
		return key_node.get_text() if key_node else None

	@staticmethod
	def extract_locality(html_map):
		key_node = html_map.find('span', itemprop='addressLocality')
		return key_node.get_text() if key_node else None

	@staticmethod
	def extract_region(html_map):
		key_node = html_map.find('span', itemprop='addressRegion')
		return key_node.get_text() if key_node else None

	@staticmethod
	def extract_postal_code(html_map):
		key_node = html_map.find('span', itemprop='postalCode')
		return key_node.get_text() if key_node else None

	@staticmethod
	def extract_price(html_map):
		key_node = html_map.find('div', class_='propertyheader-price pull-left')
		return key_node.get_text().replace('$', '').replace(',','') if key_node else None

	@staticmethod
	def extract_summary(html_map):
		elements = ['bedroof', 'bathtub','size','info']
		summary_bar = []
		for element in elements:
			class_name = ('rewicon-%s hidden-xs hidden-sm' % element)
			node = html_map.find('i', class_=class_name).find_next_sibling('span').find('strong')
			summary_bar.append(node.get_text())

		return summary_bar

	@staticmethod
	def extract_description(html_map):
		desc = html_map.find('div', itemprop='description')
		if desc is not None:
			return desc.get_text()
		return None

	@staticmethod
	def extract_features(html_map):
		features = dict()
		try:
			feature_nodes = html_map.find('table', class_='contenttable contenttable-fit').findAll('tr')
		except Exception:
			return features

		for feature_node in feature_nodes:
			feature_name = feature_node.find('th').get_text()
			feature_value = feature_node.find('td').get_text()

			if feature_name not in features:
				features[feature_name] = feature_value if feature_value else None

		return features

	@staticmethod
	def extract_property_overview(html_map):
		overview = dict()
		try:
			overview_table = html_map.find('table', class_='contenttable')
			if overview_table:
				for overview_node in overview_table.findAll('tr'):
					node_name = overview_node.find('th').get_text().replace(' ', '_').lower().strip()
					node_value = overview_node.find('td').get_text().strip()

					# Special case for "Taxes of Year"
					if 'taxes' in node_name:
						node_name = 'yearly_taxes'

					if 'sub-area' in node_name:
						node_name = 'sub_area'

					if node_name not in overview:
						overview[node_name] = node_value if node_value else None
		except Exception as e:
			print('Error Parsing Overview : %s' % str(e))
		return overview

	@staticmethod
	def normalize_overview_data(overview_data):
		# Property age: (x years old)
		if 'property_age' in overview_data:
			dict_value = overview_data['property_age']

			# Checking Edge case of "-X yrs" and "0 yrs"
			if '(-' in dict_value:
				overview_data['property_age'] = -1
			elif '(0' in dict_value:
				overview_data['property_age'] = 0
			else:
				regex_pattern = '\((\d+).+\)'
				matches = re.search(regex_pattern, dict_value)
				if matches and matches.group():
					dict_value = int(matches.group(1))
					overview_data['property_age'] = dict_value

		# Property Taxes this year
		if 'yearly_taxes' in overview_data:
			dict_value = overview_data['yearly_taxes']
			overview_data['yearly_taxes'] = Utils.price_text_to_int(dict_value)

		# Strata Maintenance Fees
		if 'strata_maintenance_fees' in overview_data:
			dict_value = overview_data['strata_maintenance_fees']
			overview_data['strata_maintenance_fees'] = Utils.price_text_to_int(dict_value)

	@staticmethod
	def extract_listing_data(search_page):
		html_map = BeautifulSoup(search_page, 'html.parser')

		# Parsing Attributes
		address = Parser.extract_address(html_map)
		locality = Parser.extract_locality(html_map)
		region = Parser.extract_region(html_map)
		postal_code = Parser.extract_postal_code(html_map)
		price = Parser.extract_price(html_map)
		summary = Parser.extract_summary(html_map)
		description = Parser.extract_description(html_map)
		features = Parser.extract_features(html_map)
		overview = Parser.extract_property_overview(html_map)

		if overview:
				Parser.normalize_overview_data(overview)

		return {'address': address, 'locality': locality, 'region': region, 'postal_code': postal_code,
				'price': int(price), 'bedrooms': summary[0], 'bathrooms': summary[1], 'sqft': int(summary[2]),
				'kind': summary[3], 'description': description, 'features': features.get('Features', None),
				'amenities': features.get('Amenities', None), 'fireplaces': int(features.get('No.Fireplaces', 0)),
				'age': overview.get('property_age', -1), 'yearly_taxes': overview.get('yearly_taxes', -1),
				'strata_maintenance_fees': overview.get('strata_maintenance_fees', 0), 'area': overview.get('area', None),
				'sub_area': overview.get('sub_area', None), 'title': overview.get('title', None),
				'listing_id': overview.get('listing_id', None), 'primary_agent': overview.get('primary_agent', None),
				'primary_broker': overview.get('primary_broker', None), 'secondary_agent': overview.get('secondary_agent', None),
				'secondary_broker': overview.get('secondary_broker', None)}