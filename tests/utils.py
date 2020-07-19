import re


def get_task_id_from_response(response):
    pattern = '^Message scheduled correctly.\nSend me "delete ([0-9]+)" to remove it.$'
    match = re.match(pattern, response)
    return int(match.group(1))
