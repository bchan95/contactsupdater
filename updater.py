#################################################
# Author: Brendan Chan
#Python script that pulls most recent Squarespace Orders by date and adds them as contacts to Freshsales



from freshsales import FreshsalesAnalytics
import requests as r
import datetime
from fake_useragent import UserAgent
import json

ua = UserAgent()

freshapi_file = open("secrets/freshapiKey", "r")
freshapiKey = freshapi_file.read()
freshapi_file.close()

sqspaceapiKeyFile = open("secrets/sqspaceapiKey", "r")
sqspaceapiKey = sqspaceapiKeyFile.read()
sqspaceapiKeyFile.close()

lastupdatedfile = open("lastupdated", "r")
lastupdated = lastupdatedfile.read()
lastupdatedfile.close()

freshsales = FreshsalesAnalytics("https://dragonveterinary.freshsales.io", freshapiKey)

headers = {'Authorization': "Bearer "+ sqspaceapiKey,
           'User-agent': str(ua.chrome)}
print(lastupdated)
if lastupdated == "":
    order = r.get("https://api.squarespace.com/1.0/commerce/orders?modifiedAfter=2017-12-30T12:00:00Z&modifiedBefore=2018-04-10T14:07:00Z", headers=headers)

else:
    order = r.get("https://api.squarespace.com/1.0/commerce/orders?modifiedAfter="+lastupdated+"Z&modifiedBefore="+datetime.datetime.now().replace(microsecond=0).isoformat()+"Z", headers=headers)



data = order.text
jsonData = json.loads(data)

for item in jsonData['result']:
    if isinstance(item, dict):
        name = item['billingAddress']['firstName']
        lastName = item['billingAddress']['lastName']
        email = item['customerEmail']
        phone = item['billingAddress']['phone']
        product = item['lineItems'][0]['productName']
        orderNumber = item['orderNumber']
        if ('Veterinary' not in product) & ('Animal' not in product):
            product = 'Med'

        else:
            product = 'Vet'

        user_options = {
            "fs_contact": True,
            'First name': name,
            'Last name': lastName,
            'Email': email,
            'Order Number': orderNumber,
            'Primary Phone': phone,
            'Med or Vet': product
            }
        freshsales.identify(email, user_options)
medKeyFile = open("secrets/medKey", "r")
medKey = medKeyFile.read()
medKeyFile.close()

headers = {'Authorization': "Bearer "+ medKey,
           'User-agent': str(ua.chrome)}

if lastupdated == "":
    order = r.get("https://api.squarespace.com/1.0/commerce/orders?modifiedAfter=2017-12-30T12:00:00Z&modifiedBefore=2018-04-10T14:07:00Z", headers=headers)

else:
    order = r.get("https://api.squarespace.com/1.0/commerce/orders?modifiedAfter="+lastupdated+"Z&modifiedBefore="+datetime.datetime.now().replace(microsecond=0).isoformat()+"Z", headers=headers)



data = order.text
jsonData = json.loads(data)

for item in jsonData['result']:
    if isinstance(item, dict):
        print(item['createdOn'])
        name = item['billingAddress']['firstName']
        print(name)
        lastName = item['billingAddress']['lastName']
        email = item['customerEmail']
        phone = item['billingAddress']['phone']
        product = item['lineItems'][0]['productName']
        orderNumber = item['orderNumber']
        purchaseDate = item['createdOn']
        if ('Veterinary' not in product) & ('Animal' not in product):
            product = 'Med'

        else:
            product = 'Vet'

        user_options = {
            "fs_contact": True,
            'First name': name,
            'Last name': lastName,
            'Email': email,
            'Order Number': orderNumber,
            'Primary Phone': phone,
            'Med or Vet': product,
            'Puchase Date': purchaseDate
            }
        freshsales.identify(email, user_options)


date = datetime.datetime.now().replace(microsecond=0)
lastupdated = date.isoformat()

lastupdatedfile = open('lastupdated', 'w')
lastupdatedfile.write(lastupdated)
lastupdatedfile.close()

# user_options = {
#     "fs_contact": True,
#     'First name': 'Testie',
#     'Last name': 'McContact',
#     'email': 'testie@test.com',
#     'Primary Phone':'666-666-6666',
#     'Med or Vet': 'Vet'
# }
# freshsales.identify('testie@test.com', user_options)