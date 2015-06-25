#!/user/bin/python
# encoding: utf-8
__author__="Bo Zhou"
__email__="bzhou2@ualberta.ca"

import sys
import bs4
import urllib2
from workflow import Workflow, ICON_WEB, web
import requests
#import json
#from multiprocessing import pool


# find tid number from html
def FindTid(htmlContext):
    url_info = htmlContext.contents[0].get('href')
    realId_list=list(url_info.split('-')[1])
    tid=''
    for i in realId_list:
        if i==".":
            break
        else:
            tid=tid+i
    return tid

# find title from html
def FindTitle(htmlContext):  
    title = htmlContext.contents[0].string
    return title

def run(wf):
    
    #crawl this web info (edmontonchina buy & sell)
    crawl_url = 'http://www.edmontonchina.ca/archiver/?fid-36.html'
    response = requests.get(crawl_url)
    soup = bs4.BeautifulSoup(response.text)
    contexts = soup.find_all('li')
    
    # Format all search result
    all_posts = []
    for context in contexts:
        tid = str(FindTid(context))
        tid = tid.encode("ascii")
        #print tid
        open_url = 'http://www.edmontonchina.ca/forum.php?mod=viewthread&tid='+tid+'&extra=page%3D1'
        #print open_url
        open_title = FindTitle(context)
        all_posts.append({'link':open_url, 'title':open_title})
    
    # ignore top ads
    for i in range(10):
        all_posts.pop(0)
    
    for info in all_posts:  
        wf.add_item(info['title'],arg=info['link'],icon='rune.png',valid = True)
    wf.send_feedback()
        
if __name__=="__main__":
    wf = Workflow()
    run(wf)
    #sys.exit(wf.run())

#url format:   
#open_url = 'http://www.edmontonchina.ca/forum.php?mod=viewthread&tid='+tid+'\&extra=page%3D1'
