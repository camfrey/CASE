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
        voteList = []

        #iterates through all the lines for all the comments
        #since there will be more than one line per comment, this for loop will be O(n) where n >= number of comments
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
                comment = ""
            else:
                comment += item[0]
        
        #since \r\n doesn't exist for the last comment, need to do it one more time
        fullDoc.append(comment)

        #for loop for votes and probably other stuff later
        #THIS FOR LOOP IS OF A DIFFERENT SIZE THAN THE FOR LOOP FOR THE WORDS
        for item in zip(votes):
            voteList.append(item[0])

        #going to do the scraped info yield here
        i = 0
        for item in fullDoc:
            scraped_info = {
                'comment' : fullDoc[i],
                'vote' : voteList[i]
            }
            yield scraped_info
            i += 1
