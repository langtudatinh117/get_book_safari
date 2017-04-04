import accSafariBook
from pymongo import MongoClient
import datetime
from datetime import date

client = MongoClient("ds137340.mlab.com", 37340)
db = client['acc_safari_book']
db.authenticate('daoan', '0903293343')
acc = db['acc']

now = datetime.datetime.now()
day = datetime.date(now.year, now.month, now.day)


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


def _regAndSaveAcc():
    try:
        expDay = {'exp': str(day + datetime.timedelta(days=8))}
        _accReg = accSafariBook.reg()
        acc.insert_one(merge_two_dicts(expDay, _accReg))
    except:
        return None
    return _accReg


def _findAcc():
    try:
        for doc in acc.find():
            exp_list = list(map(int, doc['exp'].split('-')))
            db_day = date(exp_list[0], exp_list[1], exp_list[2])
            if (db_day - day).days > 0:
                return doc
            else:
                acc.remove(doc)
    except:
        return None


def get():
    accFound = _findAcc()
    if accFound is None:
        accOK = _regAndSaveAcc()
        if accOK is not None:
            return accOK
        else:
            print('ERROR: Ko the insert acc vao database!!!')
            return None
    else:
        return accFound


# print(get()['username'])
