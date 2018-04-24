from urllib.request import Request, urlopen
from urllib.error import HTTPError
import redis
from multiprocessing import Pool


def getThyPage(postCount):
    req = Request('https://gab.ai/posts/'+str(postCount), headers={'User-Agent': 'Mozilla/5.0'}) #Pretend to be Mozilla
    webpage = urlopen(req).read()
    return str(webpage)

def saveToRedis(x):
    r = redis.Redis(host='localhost',port=6379)
    try:
         r.set(str(x), getThyPage(x)) #save the post as a string
         r.lpush("gab-posts", x) #and add successful posts to the list to know where to continue from if we crash
         #print(r.get(str(x)))
    except HTTPError:
        r.lpush("gab-broken-posts", x)
        #print("Post "+str(x)+" Unavailable")
    except (KeyboardInterrupt, SystemExit):
        sys.exit()

print("Starting scraper")
r = redis.Redis(host='localhost',port=6379)
goodPosts = [int(x) for x in r.lrange("gab-posts",0,-1)]
print("Pulled all good posts")
brokePosts = [int(x) for x in r.lrange("gab-broken-posts",0,-1)]
print("Pulled all bad posts")
allposts = set(goodPosts+brokePosts)
print("Combined posts")
print("Calculating how many posts are left to scrape...")
leftPosts = [x for x in set(range(1, 25000000)) if x not in allposts] #removed posts already checked

print(str(len(allposts)) + " posts checked " + str(len(leftPosts)) + " remaining.")

with Pool(200) as p:
    p.map(saveToRedis, leftPosts)
