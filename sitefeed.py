#Rss feed class, shows content of latest 5 updates from all users.
#Fedd is found at /latest/feed/ (eg. /loalchost:8000/latest/feed/)
#----------------------------------------------------------------------
from django.contrib.syndication.views import Feed
from users.models import update

class LatestEntriesFeed(Feed):
    title = "Friendz Updates!"
    link = "/latest/feed/"
    description = "updates of user"
    
    def items(self):
        return update.objects.order_by('-time')[:5]

 
