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


def submit_files(session, course_id, content_id, files):
    course_id, content_id = __id(course_id), __id(content_id)
    nonce, nonce_ajax = __get_nonce.search(
        requests.get(
            __new_submission_url.format(course_id, content_id),
            cookies=session
        ).text
    ).groups()
    data = [
        ("blackboard.platform.security.NonceUtil.nonce", nonce),
        ("blackboard.platform.security.NonceUtil.nonce.ajax", nonce_ajax),
        ("course_id", course_id),
        ("content_id", content_id),
        ("dispatch", "submit")
    ]
    files = [(
        ("newFile_LocalFile" + str(index), file),
        data.extend([
            ("newFile_linkTitle", file[0]),
            ("newFile_attachmentType", "L")
        ])
    )[0] for index, file in enumerate(
        files if isinstance(files, list) else [files]
    )]
    return requests.post(
        __submit_files_url,
        cookies=session,
        files=files,
        data=data
    )
