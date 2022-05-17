from logging import exception
import scrapy
import re
import time
from html.parser import HTMLParser  # Python 3
from html import unescape

urlVal = 8
pageNum = 1
postPage = []
pageIndex = 51
pageFinal = pageNum + 100
reqCounter = 0


class CaseSpider(scrapy.Spider):
    name = 'case'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/questions/9329446/for-each-over-an-array-in-javascript']
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
        firstAnswerTextOnly = response.css(".answer.js-answer.accepted-answer *::text").extract()


        comment = ""
        fullDoc = []
        voteList = []
        allLanguages = ['javascript','python','java','c#','php','html',"c++","css","sql","r","swift","ruby","xml","vba","typescript","bash","scala","powershell","matlab","kotlin","perl","dart","go","haskell","rust",'c']
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

        voteTotal = sum(voteList)


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
            stripped = re.sub(r'[^a-zA-Z0-9\#\+]', '', str(item))
            if(stripped in allLanguages):
                languages += stripped + " "
            i += 1
            print(stripped)
            print("new languages detected: ",languages)


        #go through to parse only the code portions
        allCode = ""
        #parser = HTMLParser()
        for item in zip(firstAnswer):
            onlyCode = item[0]
            onlyCode = onlyCode.split("<code>")
            if(len(onlyCode) < 2):
                break
            onlyCode.pop(0)
            for snippets in onlyCode:
                snippets = snippets.split("</code>")
                newSnippet = snippets[0]
                newSnippet = unescape(newSnippet)
                allCode += newSnippet
            break


        #first answer only
        answer = ""
        for item in zip(firstAnswerTextOnly):
            answer += item[0]

        


        #going to do the scraped info yield here
        i = 0
#        for item in fullDoc:
        scraped_info = {
            'title' : title,
            'comment' : allComments,
            'firstAnswer' : answer,
            'vote' : voteTotal,
            'views' : viewCount,
            'bookmarks' : bookmarkCount,
            'created' : created,
            'modified' : modified,
            'languages' : languages,
            'onlyCode' : allCode,
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

        evaluation0 = ["https://stackoverflow.com/questions/5767325/how-can-i-remove-a-specific-item-from-an-array", #Array URLs
        "https://stackoverflow.com/questions/237104/how-do-i-check-if-an-array-includes-a-value-in-javascript",
        "https://stackoverflow.com/questions/157944/create-arraylist-from-array",
        "https://stackoverflow.com/questions/586182/how-to-insert-an-item-into-an-array-at-a-specific-index-javascript",
        "https://stackoverflow.com/questions/3010840/loop-through-an-array-in-javascript",
        "https://stackoverflow.com/questions/1098040/checking-if-a-key-exists-in-a-javascript-object",
        "https://stackoverflow.com/questions/1129216/sort-array-of-objects-by-string-property-value",
        "https://stackoverflow.com/questions/4775722/how-can-i-check-if-an-object-is-an-array", #End array URLs
        "https://stackoverflow.com/questions/5963269/how-to-make-a-great-r-reproducible-example",
        "https://stackoverflow.com/questions/588004/is-floating-point-math-broken",
        "https://stackoverflow.com/questions/513832/how-do-i-compare-strings-in-java",
        "https://stackoverflow.com/questions/4660142/what-is-a-nullreferenceexception-and-how-do-i-fix-it",
        "https://stackoverflow.com/questions/14220321/how-to-return-the-response-from-an-asynchronous-call",
        "https://stackoverflow.com/questions/12573816/what-is-an-undefined-reference-unresolved-external-symbol-error-and-how-do-i-fix"]

        evaluation1 = ["https://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags", #Start of regex urls
        "https://stackoverflow.com/questions/22937618/reference-what-does-this-regex-mean",
        "https://stackoverflow.com/questions/201323/how-can-i-validate-an-email-address-using-a-regular-expression",
        "https://stackoverflow.com/questions/22444/my-regex-is-matching-too-much-how-do-i-make-it-stop",
        "https://stackoverflow.com/questions/123559/how-to-validate-phone-numbers-using-regex",
        "https://stackoverflow.com/questions/406230/regular-expression-to-match-a-line-that-doesnt-contain-a-word",
        "https://stackoverflow.com/questions/3512471/what-is-a-non-capturing-group-in-regular-expressions",
        "https://stackoverflow.com/questions/399078/what-special-characters-must-be-escaped-in-regular-expressions", #End of regex URLs
        "https://stackoverflow.com/questions/750486/javascript-closure-inside-loops-simple-practical-example",
        "https://stackoverflow.com/questions/20279484/how-to-access-the-correct-this-inside-a-callback",
        "https://stackoverflow.com/questions/10714251/how-to-avoid-using-select-in-excel-vba",
        "https://stackoverflow.com/questions/23667086/why-is-my-variable-unaltered-after-i-modify-it-inside-of-a-function-asynchron",
        "https://stackoverflow.com/questions/1452721/why-is-using-namespace-std-considered-bad-practice",]


        yield scrapy.Request(url=evaluation1[pageIndex], callback=self.parse,dont_filter = True)