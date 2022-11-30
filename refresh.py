import sys
import time
import datetime
import mysql.connector as mariadb
import requests
import json
import config.database as dbcon



print("""\033[32;1m
  _____     _             ____       __               _       __  __            _     _
 |__  /___ | |__   ___   |  _ \ ___ / _|_ __ ___  ___| |__   |  \/  | __ _  ___| |__ (_)_ __   ___
   / // _ \| '_ \ / _ \  | |_) / _ \ |_| '__/ _ \/ __| '_ \  | |\/| |/ _` |/ __| '_ \| | '_ \ / _ \\
  / /| (_) | | | | (_) | |  _ <  __/  _| | |  __/\__ \ | | | | |  | | (_| | (__| | | | | | | |  __/
 /____\___/|_| |_|\___/  |_| \_\___|_| |_|  \___||___/_| |_| |_|  |_|\__,_|\___|_| |_|_|_| |_|\___|

\033[m""")

def refresh_token():

    key     = sys.argv[1]

    con     = dbcon.con
    main_db = mariadb.connect(**con)
    cursor  = main_db.cursor(dictionary=True)

    cursor.execute(f"SELECT `client_id`, `client_secret`, `refresh_token` FROM `zoho` WHERE `client_id` = '{key}' ")
    result          = cursor.fetchone()
    client_id       = result["client_id"        ]
    client_secret   = result["client_secret"    ]
    refresh_token   = result["refresh_token"    ]

    # print("client_id: {client_id}")
    # print("client_secret: {client_secret}")
    # print("refresh_token: {refresh_token}")

    main_db.close()

    url             = "https://accounts.zoho.com/oauth/v2/token"
    payload         = {
        "client_id"     : client_id,
        "grant_type"    : "refresh_token",
        "client_secret" : client_secret,
        "refresh_token" : refresh_token
    }
    response        = requests.post(url, data = payload)
    form_param      = json.loads(response.text)

    # print("")
    # print(form_param)
    # print("")

    main_db = mariadb.connect(**con)
    cursor  = main_db.cursor()

    if "access_token"   in form_param:
        access_token    = form_param["access_token"     ]
        cursor.execute("ROLLBACK;"  )
        cursor.execute("BEGIN;"     )
        cursor.execute(f"UPDATE `zoho` SET `access_token` = '{access_token}', `when_update` = NOW() WHERE `client_id` = '{key}' ")
        # It could be dangerous in update query, because it don't have WHERE statement
        cursor.execute("COMMIT;"    )
    if "refresh_token"  in form_param:
        refresh_token   = form_param["refresh_token"    ]
        cursor.execute("ROLLBACK;"  )
        cursor.execute("BEGIN;"     )
        cursor.execute(f"UPDATE `zoho` SET `refresh_token` = '{refresh_token}', `when_update` = NOW() WHERE `client_id` = '{key}' ")
        # It could be dangerous in update query, because it don't have WHERE statement
        cursor.execute("COMMIT;"    )
    if "api_domain"     in form_param:
        api_domain      = form_param["api_domain"       ]
        cursor.execute("ROLLBACK;"  )
        cursor.execute("BEGIN;"     )
        cursor.execute(f"UPDATE `zoho` SET `api_domain` = '{api_domain}', `when_update` = NOW() WHERE `client_id` = '{key}' ")
        # It could be dangerous in update query, because it don't have WHERE statement
        cursor.execute("COMMIT;"    )

    main_db.close()

    if "error"          in form_param:
        print(f"[\033[35;1m{datetime.datetime.now()}\033[m] Error: {form_param['error']}")

    print(f"[\033[35;1m{datetime.datetime.now()}\033[m] Refresh")

while True:
    refresh_token()
    time.sleep(int(sys.argv[2])) # Expired in 3600
