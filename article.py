#Modelo feito para o site F1000 no GoogleChrome

import requests
from bs4 import BeautifulSoup

userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
class Article:
    def __init__(self, url, userAgent):
        self.site = self.create_request(userAgent, url)
        self.content = ""
        
    def create_request(self, userAgent, url):
        headers = {"User-Agents": userAgent}
        req = requests.get(url, headers=headers)
        return BeautifulSoup(req.text, "html.parser")
    
    def get_article_content(self):
        return BeautifulSoup(str(self.site.find_all("div", id="article1-body",class_ = "generated-article-body")), "lxml").text
    
    def get_article_name(self):
        #return self.site.find_all("div", class_ ="article-title-and-info", id="anchor-title")
        return  BeautifulSoup(str(self.site.find_all("h1", class_="js-article-title")), "lxml").text

teste = Article("https://f1000research.com/articles/12-1007", userAgent)