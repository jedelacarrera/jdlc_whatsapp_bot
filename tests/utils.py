import re


def get_task_id_from_response(response):
    assert "Message scheduled correctly" in response
    pattern = '^Message scheduled correctly.\nSend me "delete ([0-9]+)" to remove it.$'
    match = re.match(pattern, response)
    assert match is not None

    task_id = int(match.group(1))
    assert task_id > 0

    return task_id
