# zoho-refresh-machine
A machine to refresh zoho campaign token

## How to use Zoho

### Looking the information

It can be looking in [this site](https://api-console.zoho.com/).

The information that you will get:
- Client ID
- Secret ID
- Homepage URL
- Authorized Redirect URI

### Requesting the authorization

Visit this link to request the authorized:

    https://accounts.zoho.com/oauth/v2/auth?response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}&access_type=offline&prompt=consent

You will get this parameter value:
- code
- location
- accounts-server

Put that parameters on the database in `Zoho Refresh Machine`

### Run `access.py`

    python3 access.py {client_id}

### Run `refresh.py`

    python3 refresh.py {client_id} {second}

### Optional

On the Zoho Campaigns scope, disable the signup form to not need comfirmation from zoho.