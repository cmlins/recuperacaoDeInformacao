import requests
import re
from urllib.parse import urlparse
import os.path
import time

class PyCrawler(object):
    def __init__(self, starting_url, save_path, urls_completeName):
        self.starting_url = starting_url
        self.urls_completeName = urls_completeName
        self.visited = set()
        self.save_path = save_path

    #gets the html of the current link
    def get_html(self, url):
        try:
            time.sleep(10)
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
        #saraiva '''<a\s+(?:[^>]*?\s+)?href="([^"]*[\d]+/p+)'''
        #travessa '''<a\s+(?:[^>]*?\s+)?href="([^"]*/artigo/+[^"]*)'''
        #traca '''<a\s+(?:[^>]*?\s+)?href="([^"]*/livro/+[^"]*)'''
        #ciadoslivros '''<a\s+(?:[^>]*?\s+)?href="([^"]*/produto/+[\w-]*[\d]+[^/"]*)'''
        #livrariacultura '''<a\s+(?:[^>]*?\s+)?href="([^"]*p/livros/+[\w/]+[\w-]+[\d]+[^/;"]*)'''
        #americanas e submarino '''<a\s+(?:[^>]*?\s+)?href="([^"]*produto/+[\d/]+livro+[^"]*)'''
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*dp+[^;<>&]*)''', html)
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
        with open(completeName1, "w+", encoding="utf-8") as file1:
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
##    https://www.amazon.com.br/
##    https://www.saraiva.com.br/
##    https://www.travessa.com.br/
##    https://www.traca.com.br/
##    https://www.ciadoslivros.com.br/
##    https://www.extra.com.br/ ??????????????
##    https://www.livrariacultura.com.br/
##    https://www.disal.com.br/
##    https://www.americanas.com.br/  ???????????????
##    https://www.submarino.com.br/  ??????????????
    sp = 'C:/Users/Gabs/Documents/UFPE-CC/RI/amazon'
    urls_filename = "urls_amazon.txt"
    urls_completeName = os.path.join(sp, urls_filename)
    site = "https://www.amazon.com.br/"
    crawler = PyCrawler(site, sp, urls_completeName)
    crawler.start()
