import sys
import mysql.connector as mariadb
import requests
import json
import config.database as dbcon

key     = sys.argv[1]

con     = dbcon.con
main_db = mariadb.connect(**con)
cursor  = main_db.cursor(dictionary=True)

cursor.execute(f"SELECT `client_id`, `client_secret`, `redirect_uri`, `code` FROM `zoho` WHERE `client_id` = '{key}' ")
result          = cursor.fetchone()
client_id       = result["client_id"        ]
client_secret   = result["client_secret"    ]
redirect_uri    = result["redirect_uri"     ]
code            = result["code"             ]

print(f"client_id: {client_id}")
print(f"client_secret: {client_secret}")
print(f"redirect_uri: {redirect_uri}")
print(f"code: {code}")

main_db.close()

url             = "https://accounts.zoho.com/oauth/v2/token"
payload         = {
    "client_id"     : client_id,
    "grant_type"    : "authorization_code",
    "client_secret" : client_secret,
    "redirect_uri"  : redirect_uri,
    "code"          : code
}
response        = requests.post(url, data = payload)
form_param      = json.loads(response.text)

print("")
print(form_param)
print("")

main_db = mariadb.connect(**con)
cursor  = main_db.cursor()

if "access_token"   in form_param:
    access_token    = form_param["access_token"     ]
    cursor.execute("ROLLBACK;"  )
    cursor.execute("BEGIN;"     )
    cursor.execute(f"UPDATE `zoho` SET `access_token` = '{access_token}', `when_update` = NOW()  WHERE `client_id` = '{key}' ")
    cursor.execute("COMMIT;"    )
if "refresh_token"  in form_param:
    refresh_token   = form_param["refresh_token"    ]
    cursor.execute("ROLLBACK;"  )
    cursor.execute("BEGIN;"     )
    cursor.execute(f"UPDATE `zoho` SET `refresh_token` = '{refresh_token}', `when_update` = NOW()  WHERE `client_id` = '{key}' ")
    cursor.execute("COMMIT;"    )
if "api_domain"     in form_param:
    api_domain      = form_param["api_domain"       ]
    cursor.execute("ROLLBACK;"  )
    cursor.execute("BEGIN;"     )
    cursor.execute(f"UPDATE `zoho` SET `api_domain` = '{api_domain}', `when_update` = NOW()  WHERE `client_id` = '{key}' ")
    cursor.execute("COMMIT;"    )

main_db.close()
