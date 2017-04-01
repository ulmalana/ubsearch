# Masalah: get page https bermasalah di SSL, usahakan semua https diganti ke http
# Tambahkan http content type selain image
import urllib, requests
from bs4 import BeautifulSoup

def get_page(url):
	try:
		page = requests.get(url)
		return page
	except:
		return ""

def get_text_from_page(html):
	soup = BeautifulSoup(html, 'lxml')

	for script in soup(["script", "style"]):
	    script.extract()

	text = soup.get_text()


	lines = (line.strip() for line in text.splitlines())
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	text = '\n'.join(chunk for chunk in chunks if chunk)
	return text


def split_string(source, splitlist):
	output = []
	atsplit = True
	for char in source:
		if char in splitlist:
			atsplit = True
		else:
			if atsplit:
				output.append(char)
				atsplit = False
			else:
				output[-1] = output[-1] + char
	return output

def lookup(index, keyword):
	for entry in index:
		if entry[0] == keyword:
			return entry[1]
	return []

#ekstrak link
def get_next_target(page):
	start_link = page.find('<a href=')
	if start_link == -1:
		return None, 0
	start_quote = page.find('"', start_link)
	end_quote = page.find('"', start_quote+1)
	url = page[start_quote+1:end_quote]	
	return url, end_quote

#get_all_links bisa pake beautifulsoup, cek unit 9
def get_all_links(page):
	links = []	
	while True:
		url, endpos = get_next_target(page)
		if url:
			if url != "#" and "http://" in url or "https://" in url:
				if "filkom.ub.ac.id" in url:
					links.append(url)
			page = page[endpos:]
		else:
			break
	return links


def union(p,q):
	for e in q:
		if e not in p:
			p.append(e)


def add_to_index(index, keyword, url):
	for entry in index:
		if entry[0] == keyword:
			if not url in entry[1]: #menyimpan hanya 1 key dari page
				entry[1].append(url)
			return
	index.append([keyword, [url]])

def add_page_to_index(index, url, content):
	splitlist = [" ", ".", ",", "\n", "\t"]
	words = split_string(content, splitlist)
	for word in words:
		add_to_index(index, word, url)

def crawl_web(seed): #crawl_web(seed, max_page) untuk membatasi jumlah page
	tocrawl = [seed]
	crawled = []
	index = []
	while tocrawl:
		page = tocrawl.pop()
		if page not in crawled: #and len(crawled) < max_page
			web_content = get_page(page)
			if "text/html" in web_content.headers["content-type"] or "text/plain" in web_content.headers["content-type"]:
				print "CRAWLING "+page+"..."
				add_page_to_index(index, page, get_text_from_page(web_content.content))
				union(tocrawl, get_all_links(web_content.content))
				print "[CRAWLED] "+page+" | %s pages more." % str(len(tocrawl))
			crawled.append(page)
	return index
