import requests
import re
from urllib.parse import urlparse

class PyCrawler(object):
    def __init__(self, starting_url):
        self.starting_url = starting_url
        self.visited = set()

    #gets the html of the current link
    def get_html(self, url):
        try:
            html = requests.get(url)
        except Exception as e:
            print(e)
            return ""
        return html.content.decode('latin-1')

    #gets links from the current page
    def get_links(self, url):
        html = self.get_html(url)
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        #amazon '''<a\s+(?:[^>]*?\s+)?href="([^"]*dp+)'''
        #saraiva '''<a\s+(?:[^>]*?\s+)?href="([^"]*p+)'''
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*p+)''', html)
        for i, link in enumerate(links):
            if not urlparse(link).netloc:
                link_with_base = base + link
                links[i] = link_with_base
        return set(filter(lambda x: 'mailto' not in x, links))

    def create_html_file(self, url):
        html = self.get_html(url)
        print(type(html))
##        filename = url + ".html"
##        file = open(filename,"w+")
        return None

    def crawl(self, url):
        for link in self.get_links(url):
            if len(self.visited) < 10:
                if link in self.visited:
                    continue
                print(link)
                self.visited.add(link)
                count = len(self.visited)
                info = self.create_html_file(link)
                self.crawl(link)

    def start(self):
        self.crawl(self.starting_url)

if __name__ == "__main__":
    crawler = PyCrawler("https://www.saraiva.com.br/")
    crawler.start()
