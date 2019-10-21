from django.shortcuts import render
from django.http import HttpResponse
from .models import Video
import random


# Create your views here.
def index(request,page=1,sort="date",genre=None):

	if sort =="random":

		obj=Video.objects.order_by("title")
	else:

		obj=Video.objects.order_by(sort)

	count=1
	vid=[]
	show_amount=12

	no_pages=1    #to check how many pages gonna be made
	
 	#used a formula to make amount of content shown on a page and rest goes to other page
	for v in obj:
		if count <=page*show_amount and count >= page*show_amount -(show_amount-1):
			vid.append(v)
		if count%show_amount==0:
			no_pages+=1
		count+=1
	#logic forhow many page buttons will be shown.
	if  page-2 <= 1:
		p1=1
	else:
		p1=page-2

	if p1+5>no_pages:
		p2=no_pages
		p1=no_pages-4
		if p1<1:
			p1=1

	else:
		p2=p1+4
	#get all the generes list
	allgenres=[]
	for g in Video.objects.values('genres'):
		result = [x.strip() for x in g.get('genres').split(',')]
		for r in result:


			allgenres.append(r)
	allgenres=list(set(allgenres))
	if genre:
		obj=[]
		for e in Video.objects.order_by(sort).values():
			
				
			if(genre in e.get('genres')):
				if not (e in obj):
					obj.append(e)


	if sort=="random":
		random.shuffle(vid)



	

	

	return render(request,'videos/index.html',{'vid':vid,'page':page,'no_pages':range(p1,p2+1),'sort':sort,'allgenres':allgenres})


def genre(request,genre=None,page=1,sort="date"):

	obj=[]
	if sort =="random":

		temp=Video.objects.order_by("title")
	else:

		temp=Video.objects.order_by(sort)

	
	if genre:
		for t in temp.values():
			if genre in t['genres']:
				obj.append(t )
	

	count=1
	vid=[]
	show_amount=9

	no_pages=1    #to check how many pages gonna be made
	
 	#used a formula to make amount of content shown on a page and rest goes to other page
	for v in obj:
		if count <=page*show_amount and count >= page*show_amount -(show_amount-1):
			vid.append(v)
		if count%show_amount==0:
			no_pages+=1
		count+=1
	#logic forhow many page buttons will be shown.
	if  page-2 <= 1:
		p1=1
	else:
		p1=page-2

	if p1+5>no_pages:
		p2=no_pages
		p1=no_pages-4
		if p1<1:
			p1=1

	else:
		p2=p1+4
	#get all the generes list
	allgenres=[]
	for g in Video.objects.values('genres'):
		result = [x.strip() for x in g.get('genres').split(',')]
		for r in result:


			allgenres.append(r)
	allgenres=list(set(allgenres))
	if genre:
		obj=[]
		for e in Video.objects.values():
			
				
			if(genre in e.get('genres')):
				if not (e in obj):
					obj.append(e)
	if sort=="random":
		random.shuffle(vid)

	

	

	return render(request,'videos/genre.html',{'vid':vid,'page':page,'no_pages':range(p1,p2+1),'sort':sort,'allgenres':allgenres,'genre':genre})

def search(request,page=1):
	search=request.GET.get('search')
	
	obj=[]
	count=1
	vid=[]
	show_amount=12

	no_pages=1    #to check how many pages gonna be made
	for v in Video.objects.all():
		if str(search).lower() in v.title.lower():
			obj.append(v)


	for v in obj:
		if count <=page*show_amount and count >= page*show_amount -(show_amount-1):
			vid.append(v)
		if count%show_amount==0:
			no_pages+=1
		count+=1
	if  page-2 <= 1:
		p1=1
	else:
		p1=page-2

	if p1+5>no_pages:
		p2=no_pages
		p1=no_pages-4
		if p1<1:
			p1=1

	else:
		p2=p1+4


		


	return render(request,'videos/search.html',{'vid':vid,'page':page,'no_pages':range(p1,p2+1),'search':search})

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





	#for e in gen:
	#	print(e.get('genres') in genres)

	

	
	#for q in gen:
	#	print(q.get('genres'))
	return render(request,'videos/play.html',{'vid':vidd,'id':vid,'recomended':recomended,'allgenres':allgenres, 'genres':genres})
