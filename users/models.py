from django.db import models



class users(models.Model):
	email = models.EmailField(primary_key=True)
	first = models.CharField(max_length=30)
	last = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	def __str__(self):#displayed columns as string
		return '%s' % (self.email)
	
	#class Admin: pass
class update(models.Model):
	user = models.ForeignKey(users)
	time = models.DateTimeField()
	text = models.CharField(max_length=250)
	def __str__(self):#displayed columns as string
		return '%s %s %s'  % (self.user, self.text, self.time)
	def get_absolute_url(self):#required for rss feeds
		return '/update/%s/' % (self.id)


class friend(models.Model):
	#since friend has two foreign keys and cannot be classed as many to many(user may have no friend/s)
	user1 = models.ForeignKey(users, related_name="user_id")
	user2 = models.ForeignKey(users, related_name="friend_id")
	def __str__(self):#displayed columns as string
		return '%s %s'  % (self.user1, self.user2)
		
