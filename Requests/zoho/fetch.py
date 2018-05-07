import requests


# Fetches the Zoho API token using credentials
def token(email, password):
    # Post a request to create a token and retrieve it using Zoho API URL
    return requests.post("https://accounts.zoho.eu/apiauthtoken/nb/create", {
        # Specify API end point and Zoho account credentials
        "SCOPE": "ZohoMail/ZohoMailAPI",
        "EMAIL_ID": email,
        "PASSWORD": password
        # Extract the the token from response
    }).text.splitlines()[2].split("=")[1]


# Fetches Zoho account API URL
def account(auth):
    # Store Zoho account API root URL
    root_url = "https://mail.zoho.eu/api/accounts"
    # Get account id from API and concatenate it to root URL to form full URL
    return root_url + "/" + requests.get(root_url, headers={"Authorization": auth}).json()["data"][0]["accountId"] + "/messages"
