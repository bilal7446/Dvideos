from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Video
import random


# Create your views here.
def index(request,genre=None):

	#getting sort value
	if request.GET.get('sort') :
		sort= request.GET.get('sort')
		print(sort)
	else:
		sort="date"

	#sorting objects accept random sort
	if sort =="random":
		temp=Video.objects.order_by("title")
	else:

		temp=Video.objects.order_by(sort)

	#getting videos based on genres if exist and putting in a list called vid
	vid=[]
	for t in temp.values():
		if genre:
			if genre in t['genres']:
				vid.append(t)
		else:
			vid.append(t)

	#getting videos based on search value
	if request.GET.get('search') :
		search= request.GET.get('search')
		obj=vid
		vid=[]
		for v in obj:
			if str(search).lower() in v['title'].lower():
				vid.append(v)

	#random sort happns here
	if sort=="random":
		random.shuffle(vid)
	
	#get lif of all the generes that exist
	allgenres=[]
	for g in Video.objects.values('genres'):
		result = [x.strip() for x in g.get('genres').split(',')]
		for r in result:


			allgenres.append(r)
	allgenres=list(set(allgenres))

	#putting objects in pages
	paginator = Paginator(vid, 9)
	page = request.GET.get('page')
	vid = paginator.get_page(page)
	

	

	return render(request,'videos/index.html',{'vid':vid,'page':page,'sort':sort,'allgenres':allgenres,'genre':genre})
def play(request,vid):
	vidd=Video.objects.filter(id=vid)

	
	
	#splits each genre from video into list
	
	for e in vidd.values('id','genres'):

		genres = [x.strip() for x in e.get('genres').split(',')]
	
	#gets recomended videos from database based on genre of current video
	recomended=[]
	for e in Video.objects.values():
		for g in genres:
			
			if(g in e.get('genres')):
				if not (e in recomended):
					recomended.append(e)
	random.shuffle(recomended)
	recomended=recomended[:6]
	for e in recomended:

		print(e.get('id'))
	allgenres=[]
	for g in Video.objects.values('genres'):
		result = [x.strip() for x in g.get('genres').split(',')]
		for r in result:


			allgenres.append(r)
	allgenres=list(set(allgenres))

	return render(request,'videos/play.html',{'vid':vidd,'id':vid,'recomended':recomended,'allgenres':allgenres, 'genres':genres})
