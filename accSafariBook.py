from faker import Faker
import requests
from bs4 import BeautifulSoup
import string
import random
import json


def _id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


def _acc_generator():
    fake = Faker()
    name = fake.name().split(' ')
    firstName = name[0]
    lastName = name[1]
    email = fake.email()
    while email.split('@')[1] != 'gmail.com':
        email = fake.email()
    userName = email.split('@')[0]
    passWord = _id_generator()
    return {'first_name': firstName, 'last_name': lastName, 'email': email, 'username': userName,
            'password1': passWord}


def _register():
    s = requests.Session()
    URL_REGACC = 'https://www.safaribooksonline.com/register/'
    URL_REGTOPIC = 'https://www.safaribooksonline.com/register-topics/'
    try:
        s.headers = {'user-agent': 'Chrome/56.0.2924.87'}
        res = s.get(URL_REGACC)
        token = _getToken(res)
        body = merge_two_dicts(token, _acc_generator())
        body.update({'recently_viewed_bits': []})
        s.post(URL_REGACC, data=body, headers={"Referer": URL_REGACC})
        s.post(URL_REGTOPIC, data={'topics': 386},
               headers={"Referer": URL_REGTOPIC})
    except:
        return None
    else:
        return {'username': body['username'], 'password': body['password1']}


def _getToken(res):
    bsObj = BeautifulSoup(res.content, 'lxml')
    token = bsObj.find(attrs={"name": "csrfmiddlewaretoken"}).attrs['value']
    return {"csrfmiddlewaretoken": token}


def _isAccExist(username, password):
    s = requests.Session()
    URL_LOGIN = 'https://www.safaribooksonline.com/accounts/login/'
    s.headers = {'user-agent': 'Chrome/56.0.2924.87'}
    try:
        res = s.get(URL_LOGIN)
        token = _getToken(res)
        temp = {'email': username, 'password1': password,
                'login': 'Sign In', 'next': ''}
        body = merge_two_dicts(temp, token)
        s.post(URL_LOGIN, data=body, headers={"Referer": URL_LOGIN})
        api = s.get('https://www.safaribooksonline.com/api/v1/')
        getUser = json.loads(api.content.decode('utf-8'))['username']
    except:
        return False
    else:
        if getUser == username:
            return True
        else:
            return False


def login(username, password):
    s = requests.Session()
    URL_LOGIN = 'https://www.safaribooksonline.com/accounts/login/'
    s.headers = {'user-agent': 'Chrome/56.0.2924.87'}
    try:
        res = s.get(URL_LOGIN)
        token = _getToken(res)
        temp = {'email': username, 'password1': password,
                'login': 'Sign In', 'next': ''}
        body = merge_two_dicts(temp, token)
        s.post(URL_LOGIN, data=body, headers={"Referer": URL_LOGIN})
        api = s.get('https://www.safaribooksonline.com/api/v1/')
        getUser = json.loads(api.content.decode('utf-8'))['username']
    except:
        return False
    else:
        if getUser == username:
            return s
        else:
            return False


def reg():
    while True:
        registered = _register()
        if registered is not None:
            if _isAccExist(registered['username'], registered['password']):
                return registered
            else:
                continue
        else:
            return None
