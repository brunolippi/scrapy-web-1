import scrapy
import logging

class SunglassesSpider(scrapy.Spider):
    name = 'Sunglasses'
    start_urls = ['https://www.sunglasshut.com/us/mens-sunglasses']
    def count_my_calls(func, *args, **kwargs):
        """
        # This call_counter function is your new fuction.  When you use a decorator
        # you're creating a new fuction that wraps the old one up with some new
        # feature... in this case a counter
        """
        def call_counter(*args, **kwargs):
            """
            # When you call your original function after decorating it this is where
            # your code will end up.  So, here it looks like we're adding 1 to an
            # uninitilized memeber of call_counter, but we haven't actually executed
            # this code yet.
            """
            call_counter.count += 1
            """
            # This is a debug print statement to show off your count
            """
            print(call_counter.count)
            """
            # This is where you are callinging the function that was passed to
            # count_my_calls.  This will call the function with the arguments.
            """
            return func(*args, **kwargs)
        """
        # This is where you initilize the member variable in the call_counter
        # function.  This code is executed when the decorator in envoked below with
        # the @call_counter statement
        """
        call_counter.count = 0
        """
        # you are here returning the function you've just created, but you don't
        # have to do anything else with it, it'll be covered by the decorator
        # syntax
        """
        return call_counter

    @count_my_calls
    def parse(self, response):
        page = self.parse.count
        logging.info({ 'message': '*********************** PARSE PAGE ***********************', page: page})
        for products in response.css('article.sgh-tile'):
            listOfNames = products.css('span.sgh-tile__model-name')
            try:
                yield {
                    'brand': products.css('span.sgh-tile__brand::text').get(),
                    'name': listOfNames.css('.pt-2::text').get().replace('\u00ae', '').replace('\u2122', ''),
                    'price': products.css('span.sgh-tile__price::text').get().replace('$', '')
                }
            except: 
                yield {
                    'brand': products.css('span.sgh-tile__brand::text').get(),
                    'name': listOfNames.css('.pt-2::text').get().replace('\u00ae', '').replace('\u2122', ''),
                }
        next_page = str(self.start_urls[0]) + '?currentPage=' + str(page + 1)
        call_next_page = response.follow(next_page, callback=self.parse)
        if call_next_page is not None:
            logging.info({ 'message': '!!!*********************** CALLING PAGE ***********************!!!', page: page, next_page: next_page })
            yield response.follow(next_page, callback=self.parse)
