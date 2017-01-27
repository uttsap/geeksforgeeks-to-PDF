import httplib2
import pdfcrowd
import urllib2
import re
import sys
import dotenv
from bs4 import BeautifulSoup, SoupStrainer
from random import choice
from string import ascii_uppercase

to_crawl=[]
to_convert=[]
crawled=[]
dotenv.load()

def get_page(page):
    source=urllib2.urlopen(page)
    return source.read()

def save_as_pdf(s):
    try:
        m = re.search('http://www.geeksforgeeks.org/(.+?)/', s)
        if m:
            filename = m.group(1)
        else:
            filename = ''.join(choice(ascii_uppercase) for i in range(12))
        client = pdfcrowd.Client(dotenv.get('USER_NAME'), dotenv.get('API_KEY'))
        output_file = open('BST_'+filename+'.pdf', 'wb')
        html=get_page(s)
        client.convertHtml(html, output_file)
        output_file.close()
    except pdfcrowd.Error, why:
        print 'Failed: ', why

def keyword_exist(link):
    return any(x in link for x in ['bst', 'binary-search']) and \
           link not in crawled and \
           link.find('http://www.geeksforgeeks.org')==0

def crawler(hyperlink):
    global to_crawl
    global crawled
    http = httplib2.Http()
    status, response = http.request(hyperlink)
    for href in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
        if href.has_attr('href'):
            link=href['href']
            if keyword_exist(link):
                to_crawl.append(link)

def filter_useless_links():
    for pages in crawled:
        if any(x in pages for x in ['#', 'tag', 'category', 'forum']):
            continue
        to_convert.append(pages)

def main():
    global to_crawl
    global crawled
    count = 0
    
    print "Beginning Crawling process. This might take a while."
    url= 'http://www.geeksforgeeks.org/category/binary-search-tree/'
    to_crawl.append(url)

    while len(to_crawl):
        print '.',
        link=to_crawl.pop()
        if keyword_exist(link):
            crawled.append(link)
            crawler(link)

    print "\nCrawling Finished! Beginning conversion to PDF, Hang Tight!"    
    filter_useless_links()
    task = len(to_convert)
    for pages in to_convert:
        save_as_pdf(pages)
        count = count + 1
        sys.stdout.write("\r[%i/%i] PDF created!" % (count, task))
        sys.stdout.flush()

    print "\nTask Completed!"
    print "Total PDFs created = " + str(count)

if __name__ == "__main__": main()