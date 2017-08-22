from __future__ import print_function
from bs4 import BeautifulSoup

class Parser:
	@staticmethod
	def extract_neighborhood_urls(search_page, province):
		urls = set()
		parser = BeautifulSoup(search_page, 'html.parser')
		for neighborhood_node in parser.findAll('a', class_='gridblock-link', href=True):
			neighborhood_url = 'https://www.rew.ca' + neighborhood_node['href']
			# Duplicate and Province checks
			if neighborhood_url not in urls and province in neighborhood_url:
				urls.add(neighborhood_url)
		
		return list(urls)