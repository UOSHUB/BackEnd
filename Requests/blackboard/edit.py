from .values import __dismiss_update_url
import requests


# Dismisses an update in Blackboard
def dismiss_update(session, update):
    # Post a request to dismiss an update on Blackboard stream viewer
    requests.post(__dismiss_update_url, cookies=session, data={
        # Send all mandatory fields
        "callCount": "1",
        "scriptSessionId": "",
        "c0-scriptName": "NautilusViewService",
        "c0-methodName": "removeRecipient",
        "c0-id": "0",
        # Specify update id to be dismissed
        "c0-param0": "string:" + str(update),
        "batchId": "0"
    })
