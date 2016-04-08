import requests

def get_page(url):
    page = requests.get(url)
    return page.content

# adding keyword into index
def add_to_index(index, keyword, url):
    for entry in index:
        if entry[0] == keyword:
            if url not in entry[1]:
                entry[1].append(url)
            return
    index.append([keyword, [url]])

# find keyword on the index
def lookup(index, keyword):
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
    return []

# adding all the keyword from a webpage to index
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

# split content into what split_items character contains
def split_string(source,split_items):
    output = []
    start_index = 0
    stop_index = 0
    for char in source:
        if char in split_items:
            content = source[start_index:stop_index]
            if len(content) > 0:
                output.append(content)
            start_index = stop_index + 1
        stop_index = stop_index + 1
    if len(source[start_index:]) > 0:
        output.append(source[start_index:])
    return output
#------------------------------------------------------------------- indexing.py
# search next url on a page content

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

# join two list and save it on the first list
def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

# get all links on a page content
def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = []
    while tocrawl:
        webpage = tocrawl.pop()
        if webpage not in crawled:
            page_content = get_page(webpage)
            add_page_to_index(index, webpage, page_content)
            union(tocrawl, get_all_links(page_content))
            crawled.append(webpage)
    return index

