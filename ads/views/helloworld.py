
from django.http import HttpResponse
from django.shortcuts import render_to_response


def hello(request):
    return render_to_response('index.html')

    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            return render_to_response('main.html', {'person_name': 'xia', 'company': 'gvc'})
    except:
        pass


    return render_to_response('login.html', {'person_name': 'xia', 'company': 'gvc'})

