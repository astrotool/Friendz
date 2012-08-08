#------------------views.py created by Ali Alavi-----------------------
#
#
#----------------------------------------------------------------------
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from users.models import users, update, friend
from django.shortcuts import render_to_response
from regform import regForm
from django.core.context_processors import csrf#Defend against cross-site request forgery attacks, by default in Django it is required in relation to a POST query

#User login
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
			#Create a session
			request.session['ses_id'] = m.email
			#Append ses_id on to unamed = request.session['ses_id']
			#Fetch homepage once logged in
			return homepage(request)#{'uname': uname, 'sesid': d})#render_to_response('home.html', {'uname': uname})
		else:
			errors.append('Incorrect username or password. Please check login information.')
			return render_to_response('welcome.html', {'errors': errors})
	return render_to_response('welcome.html')

#This function was only used for testing, I was new to django :D
def welcome(request):
    return render_to_response('welcome.html')

#This function loads the main user page a after succesful login
def homepage(request):
	try:#Get the session id
		request.session['ses_id']
		#if session is available save it to 'sesid' which contains user name
		sesid = request.session['ses_id']
	except KeyError:#if no session present return to login page
		return render_to_response('welcome.html')
	#Display user name
	m = users.objects.get(email=sesid)
	first  = []
	first.append(m.first)
	first.append(m.last)
	uname = first
	#Get and display updates
	upd = update.objects.filter(user=sesid).order_by('-time')[:5]
	if (upd == 0):
		pass
		#pass #updates = ['No updates!']
	#Check if user has any 'friends' in friend table, at least 1
	friendz = friend.objects.filter(user1=sesid)[:1]
	if friendz:
		#Fetch a friend from table
		frlookup = friend.objects.filter(user1=sesid)[:1]
		if frlookup:
			#Fetch 5 friend updates
			fid = frlookup[0].user2
			fup = update.objects.filter(user=fid).order_by('-time')[:5]
			#Get friends name
			fnameList =[]
			fnameList.append(fid.first)
			fnameList.append(fid.last)
			fname = fnameList
			return render_to_response('home.html', {'uname': uname, 'sesid': sesid, 'updates': upd, 'fupdates': fup, 'fname': fname})#'uname': uname, 
	else:
		return render_to_response('home.html', {'uname': uname, 'updates': upd, 'sesid': sesid})#'uname': uname, 
	    
def logout(request):
    try:
		del request.session['ses_id']#removes session
    except KeyError:#if session is already removed and another logout(del session) is called skip error msg
		pass
    return render_to_response('welcome.html')
    
def addupdate(request):
	#sesid = request.session['ses_id']
	if request.method == 'POST':
		sesid = request.session['ses_id']
		upd = request.POST['update']
		updata = update(user_id=sesid, time=datetime.datetime.now(), text=upd)
		updata.save()
		return homepage(request)
	else:
		return render_to_response('welcome.html')

#Only for testing sessions are working correctly 	
def getsess(request):
	sesid = request.session['ses_id']
	return HttpResponse(sesid)

#Displays most recent updates, made to use with rss feed	
def viewupdates(request):
	upd = update.objects.order_by('-time')[:5]
	return render_to_response('updates.html', {'upd': upd})

#When a url '/update/xx/' the function below will display the update text	
def getupdate(request, upid):
	upid = int(upid)
	#Get and assign the id number for the last entry from updates table
	lastup = update.objects.latest('time')
	last_id = lastup.id
	if (upid<=last_id):
		upd = update.objects.get(id=upid)
		#For any errors on the page, insert into 'errors'
		errors = ''
	else:
		#Return no update but display error message
		upd = ''
		errors = 'No such update.'		
	return render_to_response('updates.html', {'upd': upd, 'upid': upid, 'errors': errors })

#Register a new user
def register(request):
    if request.method == 'POST':
        form = regForm(request.POST)
        if form.is_valid():
			#If all fields are present make data python presentable
            cd = form.cleaned_data
            #If passwords match add information to 'users' database
            if (cd['password'] == cd['confirm']):
				x = users(email=cd['email'].lower(), first=cd['firstName'].lower(), last=cd['lastName'].lower(), password=cd['password'])
				x.save()
				return HttpResponse('Registered! Now you can <a href="/login/">login</a>.')
            else:
				error = 'Passwords did not match. Please re-enter.'
				return render_to_response('reg_form.html', {'form': form, 'error': error})
    else:
        form = regForm()
    return render_to_response('reg_form.html', {'form': form})

#Search for a suer and add them as a friend	
def search(request):
	if request.method == 'GET':
		query = request.GET.get('q', '')
		#Split query string
		if ' ' in query:
			query = query.split()
		#If query returns both first and last name save to 'reults'
		if query:
			qset = ( Q(first__exact=query[0].lower())&Q(last__exact=query[1].lower()))
			results = users.objects.filter(qset).distinct()
		else:
			results = []
	return render_to_response('search.html', {'results': results, 'query': query})

#Adding a friendship to the database
def adduser(request, userid):
	#This function is only intiated after a search returns a list of friends
	error=''
	#Get the id of logged in user
	sesid = request.session['ses_id']
	#Check no friendship already exists
	if userid:
		lookup = friend.objects.filter(user1=sesid, user2=userid)
		if lookup:
			error = 'Friend already exists <a href="/home/">Return home</a>'
			return HttpResponse(error)
		else:
			#Create friendship by adding entry to 'friend' db
			x = friend(user1_id=str(sesid), user2_id=userid)
			x.save()
	return HttpResponse('Added! <a href="/home/">Return home</a>', error)
	
