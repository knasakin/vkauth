from django.shortcuts import render, redirect
from vk_api import VkApi
from urllib import parse


client_id = '******'
client_secret = '********************'
display = 'page'
redirect_uri = 'http://localhost:8000/auth/'
scope = 'friends'
response_type = 'code'
v = 5.131


def index(request):
    context = {'title': 'Authorization'}
    return render(request, 'vkauth/index.html', context=context)


def get_code_url(request):
    params = {'client_id': client_id,
              'display': display,
              'redirect_uri': redirect_uri,
              'scope': scope,
              'response_type': response_type,
              'v': v
              }

    querystring = parse.urlencode(params)
    url = f'https://oauth.vk.com/authorize?{querystring}'

    return redirect(url)


def get_code(request):
    code = request.GET.get('code')

    session = VkApi(app_id=client_id, client_secret=client_secret)
    session.code_auth(code=code, redirect_url=redirect_uri)
    user_id = session.token['user_id']
    token = session.token['access_token']

    return redirect(f'token/?access_token={token}&user_id={user_id}')


def get_content(request):
    token = request.GET['access_token']
    user_id = request.GET['user_id']

    session = VkApi(token=token)
    vk = session.get_api()
    friends = vk.friends.get(order='random', count=5, fields=['domain', 'first_name', 'last_name'])

    context = {'title': 'Friends', 'id': user_id} | {'Friends': friends}
    return render(request, 'vkauth/content.html', context=context)
