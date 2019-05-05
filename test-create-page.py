import subprocess
import requests

def test_page_creation(page_name):
    print("Testing page creation for a page called '" + page_name + "'")
    cmd = "python3 create-page.py " + page_name
    output = list(filter(lambda s: s != '', subprocess.check_output(cmd, shell=True).decode("utf8").split("\n")))
    last_line = output[len(output) - 1]
    url = last_line
    print("\tGot url " + url)
    response = requests.get(url)
    expected_text = '<!DOCTYPE html>\n<html>\n    <body>\n        <p>Stubbed lambda</p>\n    </body>\n</html>\n'
    assert response.text == expected_text
    print("\tPass")
    print("\tNow deleting page")
    cmd = "python3 delete-page.py " + page_name
    subprocess.check_call(cmd, shell=True)
    print("\tDone")

test_page_creation("lambdathing")
exit(0)