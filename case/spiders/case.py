import scrapy


class CaseSpider(scrapy.Spider):
    name = 'case'
    allowed_domains = ['https://stackoverflow.com/questions/9076650/find-nearest-number-in-unordered-array/9076924#9076924']
    start_urls = ['https://stackoverflow.com/questions/9076650/find-nearest-number-in-unordered-array/9076924#9076924']

    def parse(self, response):
        rnCounter = 0
        votes = response.css(".js-vote-count.flex--item.d-flex.fd-column.ai-center.fc-black-500.fs-title::text").extract()
        words = response.css(".s-prose.js-post-body *::text").extract()
        comment = ""
        fullDoc = []

        for item in zip(words):
            #create a dictionary to store the scraped info
            print("here: ",item[0])
            if(item[0] == "\r\n"):
                #\r\n signifies the start of a new comment, and thus it will be a way of parsing  all but the last comment
                print("FORTNITE")
                print("heres comment: ",comment)
                print("MITSKIMITSKIMITSKI")
                fullDoc.append(comment)
                rnCounter += 1
                scraped_info = {
                    'comment' : comment
                }
                comment = ""
                yield scraped_info
            else:
                comment += item[0]
        
        #since \r\n doesn't exist for the last comment, need to do it one more time
        scraped_info = {
            'comment' : comment
        }
        comment = ""
        yield scraped_info
        print(fullDoc)
