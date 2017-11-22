from .values import __dismiss_update_url, __submit_files_url, __new_submission_url, __get_nonce
from .general import __id
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


# Submits an assignment file(s) to Blackboard
def submit_files(session, course_id, content_id, files):
    # Store course and content ids in their Blackboard format
    course_id, content_id = __id(course_id), __id(content_id)
    # Get & Store assignment's nonce id using Regex
    nonce, nonce_ajax = __get_nonce.search(
        # Retrieve course submission page
        requests.get(
            # Using course submission URL and Blackboard cookies
            __new_submission_url.format(course_id, content_id),
            cookies=session
        ).text
    ).groups()
    # Initialize submission request's known data so far
    data = [
        ("blackboard.platform.security.NonceUtil.nonce", nonce),
        ("blackboard.platform.security.NonceUtil.nonce.ajax", nonce_ajax),
        ("course_id", course_id),
        ("content_id", content_id),
        ("dispatch", "submit")
    ]
    # Loop though sent file and format them for submission
    files = [(
        # Add file in (newFile_LocalFile0, file) pairs
        ("newFile_LocalFile" + str(index), file),
        # For every file
        data.extend([
            # Add its title and attachment type to data
            ("newFile_linkTitle", file[0]),
            ("newFile_attachmentType", "L")
        ])
        # Loop though files while keeping index
    )[0] for index, file in enumerate(
        # Make files into an array if it isn't already
        files if isinstance(files, list) else [files]
    )]
    # Post file(s) to Blackboard submission URL while passing cookies and data
    requests.post(__submit_files_url, cookies=session, files=files, data=data)
