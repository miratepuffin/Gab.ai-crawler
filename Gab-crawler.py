import psycopg2
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import redis

def getThyPage(postCount):
    req = Request('https://gab.ai/posts/'+str(postCount), headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    return str(webpage)

r = redis.Redis(
    host='localhost',
    port=6379)


for x in range(1, 10):
    try:
        r.set(str(x), getThyPage(x))
        print("Post "+str(x)+" Success")
        #print(r.get(str(x)))
    except HTTPError:
        pass
        #print("Post "+str(x)+" Unavailable")
