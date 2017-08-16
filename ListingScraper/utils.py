from __future__ import print_function

class Utils:
	@staticmethod
	def price_text_to_int(price_text):
		if price_text:
			return int(price_text.replace('$','').replace(',','').strip())
		return 0