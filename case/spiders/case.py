from logging import exception
import scrapy
import re

urlVal = 5

class CaseSpider(scrapy.Spider):
    name = 'case'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/questions/4']

    def parse(self, response):
        global urlVal

        #detect duplicate pages by checking urlVal number and what the actual URL number is
        print("RESPONSE\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("RESPONSEURL: ",response.url)
        parseUrl = response.url.split("/")
        print(len(parseUrl))
        if(len(parseUrl) > 6):
            print("DUPLICATE DETECTED")
            urlVal += 1
            if(urlVal >= 200):
                raise exceptions.CloseSpider('limit reached')
            next_page = "https://stackoverflow.com/questions/" + str(urlVal)
            print(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)
        if(response.url == "https://stackoverflow.com/questions/61/microsoft-office-2007-file-type-mime-types-and-identifying-characters/65"):
            print("here")
<<<<<<< HEAD
            raise exceptions.CloseSpider('bad url')
            
=======
            raise exception.CloseSpider('bad url')
>>>>>>> one_row

        titles = response.css(".question-hyperlink::text").extract()
        votes = response.css(".js-vote-count.flex--item.d-flex.fd-column.ai-center.fc-black-500.fs-title::text").extract()
        words = response.css(".s-prose.js-post-body *::text").extract()
        dates = response.css(".flex--item.ws-nowrap.mr16.mb8 *").extract()
        views = response.css(".flex--item.ws-nowrap.mb8 ").extract()
        bookmarks = response.css(".js-bookmark-count::text").extract()
        tags = response.css(".post-tag::text").extract()


        comment = ""
        fullDoc = []
        voteList = []
        allLanguages = {'javascript','python','java','c#','php','html',"c++","css","sql","r",'c',"swift","ruby","xml","vba","typescript","bash","scala","powershell","matlab","kotlin","perl","dart","go","haskell","rust"}
        languages = ""


        #gets title
        title = titles[0]
        #print("TITLE: ",title)
        #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


        #gets number of bookmarks on the post
        bookmarkCount = 0
        if bookmarks:
            bookmarkCount = int(bookmarks[0])
        #print("BOOKMARKS: ",bookmarkCount)


        #gets number of views on the post
        #print("AYOOOOOO",views[2][52:57])
        viewCount = views[2][52:57]
        viewCount = re.sub("[^0-9]", "", viewCount)
        viewCount = int(viewCount)
        #print(viewCount)


        #gets creation date and last modified date
        created = dates[1][39:58]
        modified = dates[3][62:82]

        # TODO: fix parsing
        #iterates through all the lines for all the comments
        #since there will be more than one line per comment, this for loop will be O(n) where n >= number of comments
        for item in zip(words):
            #create a dictionary to store the scraped info
            #print("here: ",item[0])
            if(item[0] == "\r\n"):
                #\r\n signifies the start of a new comment, and thus it will be a way of parsing  all but the last comment
                #print("FORTNITE")
                #print("heres comment: ",comment)
                #print("MITSKIMITSKIMITSKI")
                fullDoc.append(comment)
                comment = ""
            else:
                comment += item[0]
        
        #since \r\n doesn't exist for the last comment, need to do it one more time
        fullDoc.append(comment)

        allComments = ""

        for word in fullDoc:
            allComments += word

        #for loop for votes and probably other stuff later
        #THIS FOR LOOP IS OF A DIFFERENT SIZE THAN THE FOR LOOP FOR THE WORDS
        for item in zip(votes):
            voteList.append(int(item[0]))


        #this will go through the tags to find any possible langauges
        #will probably have to manually store every possible language
        #in a set and check if any tags match it because
        #the tags include things other than languages
        #the only class that I found to work to get the tags
        #will list the list of tags twice, so we must
        #only iterate through half the length of the list
        #print("SIZE OF TAGS: ",len(tags))
        tagLength = len(tags)
        i = 0
        for item in zip(tags):
            if(i >= tagLength / 2):
                break
            #print(item)
            stripped = re.sub(r'[^a-zA-Z0-9]', '', str(item))
            if(stripped in allLanguages):
                #print("APPENDED: ",stripped)
                languages += stripped + " "
            i += 1


        #going to do the scraped info yield here
        i = 0
#        for item in fullDoc:
        scraped_info = {
            'title' : title,
            'comment' : allComments,
            'vote' : voteList,
            'views' : viewCount,
            'bookmarks' : bookmarkCount,
            'created' : created,
            'modified' : modified,
            'languages' : languages
        }
        yield scraped_info
        i += 1

        print("ayo\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(response.url)
        urlVal += 1
        print(urlVal)
        if(urlVal < 200):
            next_page = "https://stackoverflow.com/questions/" + str(urlVal)
            print(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)

