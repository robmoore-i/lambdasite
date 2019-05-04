import subprocess
import requests
cmd = "python3 create-page.py test"
output = list(filter(lambda s: s != '', subprocess.check_output(cmd, shell=True).decode("utf8").split("\n")))
last_line = output[len(output) - 1]
url = last_line
print("Got url " + url)
response = requests.get(url)
expected_text = '<!DOCTYPE html>\n<html>\n    <body>\n        <p>Stubbed lambda</p>\n    </body>\n</html>\n'
assert response.text == expected_text
print("Pass")
print("Now deleting page")
cmd = "python3 delete-page.py test"
subprocess.check_call(cmd, shell=True)
print("Done")
exit(0)