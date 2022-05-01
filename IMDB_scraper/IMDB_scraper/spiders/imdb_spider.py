# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy
from scrapy.http import Request

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt0108778/']

    
    def parse(self,response):
        '''
        A parsing method that navigates to its Cast and Crew page.
        '''
        # Join current url with "fullcredits"
        full_credits = response.urljoin("fullcredits")
        yield scrapy.Request(full_credits, callback = self.parse_full_credits)


    def parse_full_credits(self,response):
        '''
        A parsing method that navigates to each actor's page
        '''
        # a list to get all urls to each actor's IMDB page
        actor_page_list = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        # navigate to each actor's IMDB page
        for next_page in actor_page_list:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback = self.parse_actor_page)

    # Function to yield actor_name and movie_or_TV_name in dictionaries 
    def parse_actor_page(self, response):
        '''
        A parsing method to get all movies and TV shows that an actor
        is listed in and put in dictionary.
        '''
        #get actor name
        actor_name = response.css("h1.header").css("span.itemprop::text").get()

        # use set to avoid multiple entries
        movie_or_TV_list = set([a.get() for a in response.css("div.filmo-row b").css("a::text")])
        
        #yield dictionary
        for a in movie_or_TV_list:
            movie_or_TV_name = a
            yield {"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name}