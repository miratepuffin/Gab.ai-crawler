from urllib.request import Request, urlopen
from urllib.error import HTTPError
import redis

def getThyPage(postCount):
    req = Request('https://gab.ai/posts/'+str(postCount), headers={'User-Agent': 'Mozilla/5.0'}) #Pretend to be Mozilla
    webpage = urlopen(req).read()
    return str(webpage)

r = redis.Redis(
    host='localhost',
    port=6379)

lastPost = r.lindex("gab-posts",0) #get the last post which was saved to redis
if(lastPost==None):
    lastPost=1
else:
    lastPost=int(lastPost)+1

for x in range(lastPost, 30000000): #From the last post to roughly all posts on GAB
    try:
         r.set(str(x), getThyPage(x)) #save the post as a string
         r.lpush("gab-posts", x) #and add successful posts to the list to know where to continue from if we crash
         print("Post "+str(x)+" Success")
#        #print(r.get(str(x)))
    except HTTPError:
        pass
        #print("Post "+str(x)+" Unavailable")
