import requests
import re
from urllib.parse import urlparse
import os.path

class PyCrawler(object):
    def __init__(self, starting_url, save_path, urls_completeName):
        self.starting_url = starting_url
        self.urls_completeName = urls_completeName
        self.visited = set()
        self.save_path = save_path

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
        #amazon '''<a\s+(?:[^>]*?\s+)?href="([^"]*dp+[^;<>&]*)'''
        #saraiva '''<a\s+(?:[^>]*?\s+)?href="([^"]*/p+)'''
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*/p+)''', html)
        for i, link in enumerate(links):
            if not urlparse(link).netloc:
                link_with_base = base + link
                links[i] = link_with_base
        return set(filter(lambda x: 'mailto' not in x, links))

    #creates file from extracted html
    def create_html_file(self, url, counter):
        html_code = self.get_html(url)
        filename1 = str(counter) + ".txt"
        completeName1 = os.path.join(self.save_path, filename1)
        file1 = open(completeName1,"w+")
        file1.write(html_code)
        file1.close()
        return None

    def crawl(self, url):
        for link in self.get_links(url):
            if len(self.visited) < 10:
                if link in self.visited:
                    continue
                print(link)
                self.visited.add(link)             
                file = open(self.urls_completeName,"a+")
                file.write(link + "\r\n")
                file.close()
                c = len(self.visited)
                info = self.create_html_file(link, c)
                self.crawl(link)

    def start(self):
        file = open(urls_completeName,"w+")
        file.close()
        self.crawl(self.starting_url)

if __name__ == "__main__":
    sp = 'C:/Users/Gabs/Documents/UFPE-CC/RI/saraiva'
    urls_filename = "urls_saraiva.txt"
    urls_completeName = os.path.join(sp, urls_filename)
    site = "https://www.saraiva.com.br/"
    crawler = PyCrawler(site, sp, urls_completeName)
    crawler.start()
