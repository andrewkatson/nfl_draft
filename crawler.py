
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import re
import requests

import common

class Crawler:

    def __init__(self, urls=[], limit=-1, word="", regex="", depth=1):
        self.visited_urls = []
        self.urls_to_visit = {1: urls}
        self.limit = limit
        self.word_to_look_for = word
        self.regex_to_match = regex
        self.final_urls = []

    def get_linked_urls(self, url, html):
        soup = common.get_soup(html)
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
                if self.word_to_look_for in path:
                    yield path

    def add_url_to_visit(self, url, list_at_depth):
        if url not in self.visited_urls:
            for _, urls in self.urls_to_visit.items():
                if url not in urls:
                    list_at_depth.append(url)

    def crawl(self, url, depth):
        html = common.download_url(url)
        new_urls_to_visit_at_depth = []
        for url in self.get_linked_urls(url, html):
            new_urls_to_visit_at_depth.append(url)
            
        if depth in self.urls_to_visit.keys():
            urls_at_depth = self.urls_to_visit[depth]
            for url in new_urls_to_visit_at_depth:
                self.add_url_to_visit(url, urls_at_depth)
            self.urls_to_visit[depth] = urls_at_depth
        else: 
            self.urls_to_visit[depth] = new_urls_to_visit_at_depth

    def run(self):
        count = 0
        depth = 1
        while self.urls_to_visit and self.limit > count:
            urls = self.urls_to_visit[depth]
            while urls and self.limit > count:
                url = urls.pop(0)
                try:
                    self.crawl(url, depth + 1)
                except Exception as e:
                    print(f'Failed to crawl: {url} {e}')
                finally:
                    self.visited_urls.append(url)
                count += 1
            depth += 1
        
        self.final_urls = []
        for url in self.visited_urls:
            if self.url_matches(url) and url not in self.final_urls: 
                self.final_urls.append(url)
                
        for _, urls in self.urls_to_visit.items():
            for url in urls: 
                if self.url_matches(url) and url not in self.final_urls: 
                    self.final_urls.append(url)
                
    def url_matches(self, url): 
        matcher = re.compile(self.regex_to_match)
        if matcher.search(url):
            return True
        
        return False
