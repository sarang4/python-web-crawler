"""You will require BeautifulSoup, logging, urllib, urlparse packges 
     If they are not present make sure you have installed it and then only run this script
"""


import sys
import logging
from urllib import urlopen
from urlparse import urlparse
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

def enable_console_logging(log):
    """Logging function to enable logging to the console"""

    log.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    log.addHandler(ch)

def crawl_url(no_links_to_crawl = None, start_url = 'http://python.org/'):
    """   Aim: This function will actually perform crawling of links
	Input: Both inputs no_links_to_crawl and start_url are optional
       Output: Links that has been crawled and repository of links that found after crawling
    """
    
    links_crawled = [] 
    links_to_crawl = []

    try:
	links_to_crawl.append(start_url)
	while 1:

	    #pcondition to stop the program after specified no of links crawled if no of links to be crawled has been provided
	    if no_links_to_crawl and len(links_crawled) == no_links_to_crawl:
		break
	    
	    try:
		crawling_url = links_to_crawl.pop(0)
		log.info("Going to Crawl : %s" %crawling_url)
	    except KeyError:
		log.exception("Exception occured while poping next url to crawl.")
		raise IndexError

	    try:
		page_content = urlopen(crawling_url)
		parsed_url = urlparse(crawling_url)
	    except:
		continue
	    
	    #Link that just crawled has been added to repository of crawled links.
	    links_crawled.append(crawling_url)
	    
	    #Beautifying the content.
	    beautiful_content = BeautifulSoup(page_content.read())

	    for a_tag in beautiful_content.find_all('a'):
		link = a_tag.get('href')
		if link:
		    if link.startswith('/'):
			link = 'http://' + parsed_url[1] + link
		    elif link.startswith('#'):
			link = 'http://' + parsed_url[1] + parsed_url[2] + link
		    elif not link.startswith('http'):
			link = 'http://' + parsed_url[1] + '/' + link
		    
		    #If link is not already crawled, put in repository of links to be crawled.
		    if link not in links_crawled:
			links_to_crawl.append(link)
    
    except KeyboardInterrupt:
	log.exception("Programmed has been stopped manually.")
    except:
	log.exception("Exception occured")
    finally:
	log.info("Links that has been crawled are %s" %links_crawled)
	log.info("Repositary of links is %s" %(links_crawled + links_to_crawl))

if __name__ == '__main__':
    
    enable_console_logging(log)

    #Formation imput that is cming from command line arguments
    no_links_to_crawl = int(sys.argv[1]) if len(sys.argv) >= 2 else None
    start_url = sys.argv[2] if len(sys.argv) == 3 else 'http://python.org/'
   
    #Calling web crawling main function
    crawl_url(no_links_to_crawl, start_url)
	
