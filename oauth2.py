from requests_oauthlib import OAuth2Session
import requests
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('example.cfg')

client_id = config.get('Section1', 'client_id')
client_secret = config.get('Section1', 'client_secret')
redirect_uri = config.get('Section1', 'redirect_uri')

authorization_base_url = "https://platform.lifelog.sonymobile.com/oauth/2/authorize"
token_url = "https://platform.lifelog.sonymobile.com/oauth/2/token"
scope = [
    "lifelog.profile.read",
    "lifelog.activities.read",
    "lifelog.locations.read"
]
sony = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

# Redirect user to Sony for authorization
authorization_url, state = sony.authorization_url(authorization_base_url,
    # offline for refresh token
    # force to always make user click authorize
    access_type="offline", approval_prompt="force")
print 'Please go here and authorize,', authorization_url

# Get the authorization verifier code from the callback url
redirect_response = raw_input('Paste the full redirect URL here:')

# Fetch the access token
response=sony.fetch_token(token_url, client_secret=client_secret,
        authorization_response=redirect_response)
print sony.token.get('access_token')

# Fetch a protected resource, i.e. user profile
headers = {
    "Authorization": "Bearer "+str(sony.token.get('access_token'))
}
response = requests.get("https://platform.lifelog.sonymobile.com/v1/users/me", headers=headers)
#print content
print response.json()
