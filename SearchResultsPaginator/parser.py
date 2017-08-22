from __future__ import print_function
from bs4 import BeautifulSoup

class Parser:
	@staticmethod
	def extract_listing_urls(search_page):
		urls = set()
		parser = BeautifulSoup(search_page, 'html.parser')
		for listing_node in parser.findAll('span', class_='listing-address'):
			for listing_url in listing_node.findAll("a", href=True):
				url = 'https://www.rew.ca' + listing_url['href']
				if url not in urls:
					urls.add(url)
		
		return list(urls)
	
	@staticmethod
	def extract_search_pages_count(search_page):
		parser = BeautifulSoup(search_page, 'html.parser')
		last_page_found = ''
		for paginator_node in parser.findAll('li', class_='paginator-page'):
			for paginator_txt in paginator_node.findAll('a', href=True):
				last_page_found = paginator_txt.text
		
		return last_page_found