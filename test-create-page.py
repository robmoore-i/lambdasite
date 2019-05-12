import subprocess
import requests

def check_request_content_matches_file(filename, url):
    response = requests.get(url)
    expected_text = ""
    with open(filename, "r") as expected_document:
        expected_text = expected_document.read()
    assert response.text == expected_text


def test_page_creation(page_name):
    print("Testing page creation for a page called '" + page_name + "'")
    cmd = "python3 create-page.py " + page_name
    output = list(filter(lambda s: s != '', subprocess.check_output(cmd, shell=True).decode("utf8").split("\n")))
    last_line = output[len(output) - 1]
    url = last_line
    print("\tGot url " + url)
    print("\tChecking html")
    check_request_content_matches_file("initial-page/src/document.html", url)
    print("\tChecking css")
    check_request_content_matches_file("initial-page/src/document.css", url + "?resource=css")
    print("\tAll Passed")
    print("\tNow deleting page")
    cmd = "python3 delete-page.py " + page_name
    subprocess.check_call(cmd, shell=True)
    print("\tDone")

test_page_creation("lambdathing")
exit(0)