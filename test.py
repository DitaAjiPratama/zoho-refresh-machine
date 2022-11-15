import mysql.connector as mariadb
import requests
import json

con = {
    'host'      :'localhost',
    'user'      :'root',
    'password'  :'',
    'database'  :'zrm',
    'autocommit':True,
}

main_db = mariadb.connect(**con)
cursor  = main_db.cursor()

cursor.execute(f"SELECT `access_token` FROM `zoho` ")
result          = cursor.fetchone()
access_token    = result[0]

url             = "https://campaigns.zoho.com/api/v1.1/addlistsubscribersinbulk"
payload         = {
    "listkey"   :"YOUR_LIST_KEY",
    "resfmt"    :"JSON",
    "emailids"  :"user@example.com"
}
headers         = {
    "Authorization" : f"Zoho-oauthtoken {access_token}",
    "Content-Type"  : "application/x-www-form-urlencoded"
}
response        = requests.post(url, data = payload, headers = headers)
json_response   = json.loads(response.text)

print( json.loads(response.text) )
