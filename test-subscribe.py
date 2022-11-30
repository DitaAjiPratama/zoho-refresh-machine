import mysql.connector as mariadb
import requests
import json
import config.database as dbcon

con     = dbcon.con
main_db = mariadb.connect(**con)
cursor  = main_db.cursor()

cursor.execute(f"SELECT `access_token` FROM `zoho` WHERE `client_id` = 'YOUR_CLIENT_ID' ")
result          = cursor.fetchone()
access_token    = result[0]

sijeson = """
{"First Name":"YOUR_FIRST_NAME","Last Name":"YOUR_LAST_NAME","Contact Email":"user@example.com"}
"""

url             = "https://campaigns.zoho.com/api/v1.1/json/listsubscribe"
payload         = {
    "resfmt"        :"JSON",
    "listkey"       :"YOUR_LIST_KEY",
    "contactinfo"   : sijeson
}
headers         = {
    "Authorization" : f"Zoho-oauthtoken {access_token}",
    "Content-Type"  : "application/x-www-form-urlencoded"
}
response        = requests.post(url, data = payload, headers = headers)
json_response   = json.loads(response.text)

print( payload )
print( json.loads(response.text) )
