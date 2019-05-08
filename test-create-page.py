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
    expected_text = """<!DOCTYPE html>
<html>

<head>
    <title>Title</title>
</head>

<body bgcolor="#f9f9f9">
    <h4 align="center">Date</h4>
    <h1 align="center">Title</h1>
    <h3 style="color: orange; margin-left: 30%; margin-right: 30%">Subheading 1</h3>
    <p style="margin-left: 30%; margin-right: 30%; line-height: 2">
        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's
        standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make
        a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting,
        remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing
        Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions
        of Lorem Ipsum.
    </p>
    <pre
        style="margin-left: 30%; margin-right: 30%; border-style: solid; border-width: 1px; border-color: black; border-radius: 5px; font-size: 150%; padding: 10px">
const fs = require('fs')

exports.handler = async (event) => {
    const document = fs.readFileSync("document.html", "utf8")
    const response = {
        statusCode: 200,
        headers: {
            "content-type": "text/html"
        },
        body: document,
    }
    return response
}</pre>
    <h3 style="color: orange; margin-left: 30%; margin-right: 30%">Subheading 2</h3>
    <p style="margin-left: 30%; margin-right: 30%; line-height: 2">
        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's
        standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make
        a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting,
        remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing
        Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions
        of Lorem Ipsum.
    </p>
</body>

</html>"""
    assert response.text == expected_text
    print("\tPass")
    print("\tNow deleting page")
    cmd = "python3 delete-page.py " + page_name
    subprocess.check_call(cmd, shell=True)
    print("\tDone")

test_page_creation("lambdathing")
exit(0)