from django.http import HttpResponse
from users.models import users, update, friend
from django.shortcuts import render_to_response
from django.core.context_processors import csrf#Defend against cross-site request forgery attacks, by default in Django it is required in relation to a POST query


def login(request):
	if request.method == 'POST':
		c = {}
		c.update(csrf(request))#csrf request
		errors = []
		u = request.POST['user']
		p = request.POST['pw']
		#Check password matches
		if users.objects.filter(email=u, password=p):
			#fetch user details
			m = users.objects.get(email=u)
			#show user name
			first  = []
			first.append(m.first)
			first.append(m.last)
			uname = [' '.join(first)]
			#Create a session
			request.session['ses_id'] = m.email
			#Append ses_id on to uname
			d = request.session['ses_id']
			#uname.append(d)
			return homepage(request)#{'uname': uname, 'sesid': d})#render_to_response('home.html', {'uname': uname})
		else:
			errors.append('Incorrect username or password. Please check login information.')
			return render_to_response('welcome.html', {'errors': errors})

def welcome(request):
    return render_to_response('welcome.html')

def homepage(request):
	try:#Get the session id
		request.session['ses_id']
		#if session is vailable save it
		sesid = request.session['ses_id']
	except KeyError:#if no session present return to login page
		return render_to_response('welcome.html')
	m = users.objects.get(email=sesid)
	first  = []
	first.append(m.first)
	first.append(m.last)
	uname = [' '.join(first)]
	#Get and display updates
	upd = update.objects.filter(user=sesid).order_by('-time')
	if upd:
		count = 0
		updates= []
		while (count < 2):
			updates.append(str(upd[count].text))
			count += 1
	else:
		updates = ['No updates!']
	frlookup = friend.objects.get(user1=sesid)
	if frlookup:
		fid = frlookup.user2
		fup = update.objects.filter(user=fid).order_by('-time')
		i = 0
		fupdates = []
		while (i < 2):
			fupdates.append(str(fup[i].text))
			i += 1
		
	fnameList =[]
	fnameList.append(fid.first)
	fnameList.append(fid.last)
	fname = [' '.join(fnameList)] 
	return render_to_response('home.html', {'uname': uname, 'sesid': sesid, 'updates': updates, 'fupdates': fupdates, 'fname': fname})#'uname': uname, 
    
def logout(request):
    try:
		del request.session['ses_id']#removes session
    except KeyError:#if session is already removed and another logout(del session) is called skip error msg
		pass
    return render_to_response('welcome.html')
    
def addupdate(request):
	pass
	
def getsess(request):
	sesid = request.session['ses_id']
	return HttpResponse(sesid)
    
