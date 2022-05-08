from logging import exception
import scrapy
import re
import time
from html.parser import HTMLParser  # Python 3

urlVal = 8
pageNum = 1
postPage = []
pageIndex = 51
pageFinal = pageNum + 100
reqCounter = 0


class CaseSpider(scrapy.Spider):
    name = 'case'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/questions?tab=votes&page=1']
    handle_httpstatus_list = [404, 429] #we handle 404's inside the parse function

    def parse(self, response):
        global reqCounter
        global urlVal
        global pageNum
        global postPage
        global pageIndex
        global pageFinal
        print("response status: ",response.status)


        if(response.status == 429):
            time.sleep(180)
            pageIndex += 1
            if(pageIndex > 49):
                pageIndex = -1
                next_page = "https://stackoverflow.com/questions?tab=votes&page=" + str(pageNum)
                pageNum += 1
                print("here's the new list of next pages: ",next_page)
                yield scrapy.Request(url=next_page, callback=self.parse,dont_filter = True)
                return
            #gets list of questions (only have to do this once per changing of questions listings page)
            if(pageIndex == -1):
                print("in here")
                pageIndex = 0
                posts = response.css(".s-post-summary--content-title .s-link").extract()
                print("number of posts on this page: ",len(posts))
                print("here are the questions: ")
                postPage = posts
                for item in postPage:
                    item = item.split("\"")
                    print(item[1])
                #goes to next forum post, after gathering all data
                next_page = "https://stackoverflow.com" + postPage[pageIndex].split("\"")[1]
                pageIndex += 1
                print("next page: ",next_page)

                yield scrapy.Request(url=next_page, callback=self.parse,dont_filter = True)
                return
            #goes to next forum post, after gathering all data
            print("here is the pageIndex: ",pageIndex)
            next_page = "https://stackoverflow.com" + postPage[pageIndex].split("\"")[1]
            pageIndex += 1
            print("next page: ",next_page)

            yield scrapy.Request(url=next_page, callback=self.parse,dont_filter = True)
            
        
            



        #automated stop for testing purposes
        if(pageNum > pageFinal):
            return

        #each page has 50 forum posts on it, checks if we looked at all posts
        #redirects to next page of post listings
        if(pageIndex > 49):
            pageIndex = -1
            next_page = "https://stackoverflow.com/questions?tab=votes&page=" + str(pageNum)
            pageNum += 1
            print("here's the new list of next pages: ",next_page)
            yield scrapy.Request(url=next_page, callback=self.parse,dont_filter = True)
            return

        
        #gets list of questions (only have to do this once per changing of questions listings page)
        if(pageIndex == -1):
            print("in here")
            pageIndex = 0
            posts = response.css(".s-post-summary--content-title .s-link").extract()
            print("number of posts on this page: ",len(posts))
            print("here are the questions: ")
            postPage = posts
            for item in postPage:
                item = item.split("\"")
                print(item[1])
            #goes to next forum post, after gathering all data
            next_page = "https://stackoverflow.com" + postPage[pageIndex].split("\"")[1]
            pageIndex += 1
            print("next page: ",next_page)

            yield scrapy.Request(url=next_page, callback=self.parse,dont_filter = True)
            return


        ##############################################################################################################################################
        # data gathering section
        ##############################################################################################################################################


        titles = response.css(".question-hyperlink::text").extract()
        votes = response.css(".js-vote-count.flex--item.d-flex.fd-column.ai-center.fc-black-500.fs-title::text").extract()
        words = response.css(".s-prose.js-post-body *::text").extract()
        dates = response.css(".flex--item.ws-nowrap.mr16.mb8 *").extract()
        views = response.css(".flex--item.ws-nowrap.mb8 ").extract()
        bookmarks = response.css(".js-bookmark-count::text").extract()
        tags = response.css(".post-tag::text").extract()
        firstAnswer = response.css(".answer.js-answer.accepted-answer").extract()


        comment = ""
        fullDoc = []
        voteList = []
        allLanguages = {'javascript','python','java','c#','php','html',"c++","css","sql","r",'c',"swift","ruby","xml","vba","typescript","bash","scala","powershell","matlab","kotlin","perl","dart","go","haskell","rust"}
        languages = ""


        #gets title
        title = titles[0]


        #gets number of bookmarks on the post
        bookmarkCount = 0
        if bookmarks:
            bookmarkCount = int(bookmarks[0])


        #gets number of views on the post
        viewCount = views[2][52:]
        viewCount = viewCount.split("times")[0]
        viewCount = re.sub("[^0-9]", "", viewCount)
        viewCount = int(viewCount)


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
            stripped = re.sub(r'[^a-zA-Z0-9]', '', str(item))
            if(stripped in allLanguages):
                languages += stripped + " "
            i += 1


        #go through to parse only the code portions
        allCode = ""
        parser = HTMLParser()
        for item in zip(firstAnswer):
            onlyCode = item[0]
            onlyCode = onlyCode.split("<code>")
            if(len(onlyCode) < 2):
                break
            onlyCode.pop(0)
            for snippets in onlyCode:
                snippets = snippets.split("</code>")
                newSnippet = snippets[0]
                newSnippet = parser.unescape(newSnippet)
                allCode += newSnippet
            print("here:::::")
            print(allCode)
            break

        


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
            'languages' : languages,
            'only code' : allCode,
            'url' : response.url
        }
        yield scraped_info
        i += 1


        ##############################################################################################################################################
        # end data gathering section
        ##############################################################################################################################################


        #goes to next forum post, after gathering all data
        print("here is the pageIndex: ",pageIndex)
        next_page = "https://stackoverflow.com" + postPage[pageIndex].split("\"")[1]
        pageIndex += 1
        print("next page: ",next_page)

        yield scrapy.Request(url=next_page, callback=self.parse,dont_filter = True)