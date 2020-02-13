import requests
from bs4 import BeautifulSoup
# import inspect
# import functools
from datetime import datetime, timedelta

def convert_date(date):
    """Ebaykleinanzeigen have heute for today and Gestern for yesterday.
    Convert them to actual date. 
    """
    date = date.lower()
    if "heute" in date:
        date = datetime.strptime(datetime.today().strftime('%d.%m.%Y'), '%d.%m.%Y')
    elif "gestern" in date:
        yesterday = datetime.today() - timedelta(1)
        date = datetime.strptime(yesterday.strftime('%d.%m.%Y '), '%d.%m.%Y')
    elif date:
        date = datetime.strptime(date, '%d.%m.%Y')
    return date




# def checkParams(**types):
# 	def decorate(f):
# 		farg, _, _, def_params = inspect.getargspec(f)
# 		if def_params is None: def_params = []
# 		farg = farg[:len(farg) - len(def_params)]
 
# 		param_info = [(par, ptype, par in farg) for par, ptype in types.items()]
 
# 		@functools.wraps(f)
# 		def wrapper(*args, **kargs):
# 			getparam = bottle.request.GET.get
# 			for par, ptype, required in param_info:
# 				value = getparam(par)
# 				if not value: # None or empty str 
# 					if required:
# 						error = "%s() requires the parameter %s" % (wrapper.__name__, par)
# 						raise TypeError(error)
# 					continue
# 				try:
# 					kargs[par] = ptype(value)
# 				except:
# 					error = "Cannot convert parameter %s to %s" % (par, ptype.__name__)
# 					raise ValueError(error)
 
# 			return f(*args, **kargs)
 
# 		return wrapper
# 	return decorate


def get_request(url, payload):
	"""Request URL and return BeautifulSoup object"""
	requests_get = requests.get(url, params=payload)
	requests_get.encoding = 'utf-8'

	# TODO this may not be necessary . 
	if "kleinanzeigen.ebay.de" in url:
		return BeautifulSoup(requests_get.text.replace("&#8203",""), features="lxml")

	return BeautifulSoup(requests_get.text)


def make_clickable(val):
    """Make url column in the DataFrame clickable."""
    # target _blank to open new window
    return '<a target="_blank" href="{}">{}</a>'.format(val, val)