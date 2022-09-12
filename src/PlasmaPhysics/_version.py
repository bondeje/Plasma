import json

version_json = '''
{
 "date": "2022-04-07T17:46:00-0000",
 "full-revisionid": "000",
 "version": "0.0.0.dev1",
 "python": "3.9"
}
'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)
