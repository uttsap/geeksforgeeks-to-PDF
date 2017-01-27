import httplib2
import pdfcrowd
import urllib2
import re
import sys
from bs4 import BeautifulSoup, SoupStrainer
from random import choice
from string import ascii_uppercase

to_crawl=[]
crawled=[]

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
        client = pdfcrowd.Client("raghavjajodia", "e956749933e5c1c6bf15954aa970ed90")
        output_file = open('BST_'+filename+'.pdf', 'wb')
        html=get_page(s)
        client.convertHtml(html, output_file)
        output_file.close()
    except pdfcrowd.Error, why:
        print 'Failed: ', why

def crawler(hyperlink):
    global to_crawl
    global crawled
    http = httplib2.Http()
    status, response = http.request(hyperlink)
    for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            li=link['href']
            if li.find('http://www.geeksforgeeks.org')==0 and (li.find('bst')>0 or li.find('binary-search')>0) and li not in crawled and li.find('forums')<0:
                to_crawl.append(li)

def main():
    global to_crawl
    global crawled
    count = 0
    
    print "Beginning Crawling process. This might take a while."
    url= 'http://www.geeksforgeeks.org/category/binary-search-tree/'
    crawled.append(url)
    crawler(url)

    while len(to_crawl):
        print '.',
        link=to_crawl.pop()
        if link.find('http://www.geeksforgeeks.org')==0 and (link.find('bst')>0 or link.find('binary-search')>0) and link not in crawled:
            crawled.append(link)
            crawler(link)

    print "\nCrawling Finished! Beginning conversion to PDF, Hang Tight!"
    task = len(crawled)
    for pages in crawled:
        if any(x in pages for x in ['#', 'tag', 'category', 'forum']):
            continue
        elif pages.find('bst') >= 0 or pages.find('binary-search') >= 0:
            #save_as_pdf(pages)
            count = count + 1
            sys.stdout.write("\r[%i/%i] PDF created!" % (count, task))
            sys.stdout.flush()

    print "\nTask Completed!"
    print "Total PDFs created = " + str(count)

if __name__ == "__main__": main()