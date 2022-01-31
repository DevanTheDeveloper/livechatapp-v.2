from django.shortcuts import render

# Create your views here.
def index(request):
	context = {}
	return render(request, 'chat/index.html', context)


def room(request,roomName):
	context = {'roomName':roomName}
	return render(request, 'chat/room.html', context)