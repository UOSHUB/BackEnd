from Requests import get_path
import requests

# Store paths for token and account files
token_path = get_path("token")
account_path = get_path("account")


# Fetches the Zoho API token using credentials
def fetch_token(email, password):
    # Store token in the token file
    open(token_path, "w").write(
        # Post a request to create a token and retrieve it using Zoho API URL
        requests.post("https://accounts.zoho.eu/apiauthtoken/nb/create", {
            # Specify API end point and Zoho account credentials
            "SCOPE": "ZohoMail/ZohoMailAPI",
            "EMAIL_ID": email,
            "PASSWORD": password
            # Extract the the token from response
        }).text.splitlines()[2].split("=")[1]
    )


# Fetches Zoho account API URL
def fetch_account():
    # Store Zoho account API root URL
    root_url = "https://mail.zoho.eu/api/accounts"
    # Store account URL in account file
    open(account_path, "w").write(
        # Get account id from API and concatenate it to root URL to form full URL
        root_url + "/" + requests.get(root_url, headers=auth).json()["data"][0]["accountId"] + "/messages"
    )


# fetch_token("", "")
# Get token from file and store it in dictionary
auth = {"Authorization": open(token_path).read()}

#  fetch_account()
# Get account URL from file and store it
url = open(account_path).read()
