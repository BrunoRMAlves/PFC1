#Modelo feito para o site F1000 no GoogleChrome

import requests
from article import Article
from collections import defaultdict
from bs4 import BeautifulSoup

userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
class WebScrapperF1000:
    def __init__(self, url, userAgent):
        self.url = url
        self.req = self.create_request(userAgent)
        print("Construiu a request")
        self.site = BeautifulSoup(self.req.text, "html.parser")
        print("Fez a request")
        self.articles_divs = self.get_articles_divs()
        print("Pegou todas as divs")
        self.articles_status = self.get_articles_review_status()
        print("Pegou todos os status dos artigos")
        self.drop_unreviewed_articles()
        print("Dropou os artigos não revisados")
        self.articles_names = self.get_articles_names()
        print("Pegou todos os nomes")
        self.articles_links = self.get_articles_url()
        print("Pegou todos os links")
        self.articles_dict = self.get_articles_dict()
        print("Pegou o dict de artigos")
        self.save_article_text()

    def create_request(self, userAgent):
        headers = {"User-Agents": userAgent}
        return requests.get(self.url, headers=headers)

    def get_articles_divs(self):
        return self.site.find_all(self.custom_selector)
        
    def custom_selector(self, tag):
	    return tag.name == "div" and tag.has_attr("class") and tag.has_attr("data-index") and tag.has_attr("data-article-id") and tag.has_attr("data-article-doi")

    def get_articles_names(self):
        names = []
        for article in self.articles_divs:
            str_article = str(article)
            splitted = str_article.split('"')
            names.append(splitted[7])
        return names        

    def get_articles_url(self):
        urls = []
        for article in self.articles_divs:
            str_article = str(article)
            splitted = str_article.split('"')
            urls.append(splitted[12][1:48])
        return urls

    def get_articles_review_status(self):
        status = []
        for article in self.articles_divs:
            str_article = str(article)
            if(str_article.count("peer-review-status") == 1):
                status.append("AWAITING PEER REVIEW")
            else:
                status.append("CONTAINS PEER REVIEW")
        return status
        
    def drop_unreviewed_articles(self):
        indexes = []
        for i in range(len(self.articles_status)):
            if(self.articles_status[i] == "AWAITING PEER REVIEW"):
                indexes.append(i)
        for index in indexes[::-1]:
            self.articles_status.pop(index)
            self.articles_divs.pop(index)
        print(len(self.articles_divs), "artigos estão disponíveis com suas respectivas revisões")
            
    def get_articles_dict(self):
        articles = defaultdict(str)
        for i in range(len(self.articles_links)):
            articles.update({str(self.articles_names[i]) : Article(self.articles_links[i], userAgent)}) 
            print(Article(self.articles_links[i], userAgent).get_article_name())
        return articles
    
    def save_article_text(self):
        for key in self.articles_dict.keys():  
            name = str("./artigos/"+ (BeautifulSoup(str(key), "lxml").text).replace(":","").replace("/","_").replace("-","_").replace(".","").replace(",","").replace("(","[").replace(")","]"))
            if len(name)>120:
                with open((name[0:120] + ".txt"), 'w') as f:
                    f.write(str(self.articles_dict.get(key).get_article_content()))
            else:
                with open((name + ".txt"), 'w', encoding="utf-8") as f:
                    f.write(str(self.articles_dict.get(key).get_article_content()))
                
        
        

    #def request_to_article_url(self):

    #def get_version_url(self):

    #def set_article_version(self):
        # article = request_to_article_url()

    #def get_article_content(self):

    #def get_article_first_review(self):
    
    #def save_review(self, review_name, review_content):
    #    with open(review_name, 'w') as f:
    #       f.write(review_content)

print("Iniciou o programa")
teste = WebScrapperF1000("https://f1000research.com/browse/articles", userAgent)
teste.get_articles_dict()