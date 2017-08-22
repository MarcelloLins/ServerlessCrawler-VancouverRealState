from __future__ import print_function

class Utils:
	@staticmethod
	def get_next_page_url(base_url, next_page):
		return base_url + ('/page/%d' % next_page)