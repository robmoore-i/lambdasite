# lambdasite

## Creating web pages

To create a new web page, run `python3 create-page.py <page name>`.

This will create a lambda, served through API gateway, and a folder for lambda. The lambda serves a HTML document found at `<page name>-website/src/document.html`. There is a script `<page name>-website/update-lambda.sh` which will automatically update the live lambda.

Each page's folder contains a file called `endpoint` which contains the URL from which the page is accessible.

## Deleting web pages

To delete a web page, run `python3 delete-page.py <page name>`.

This will delete the local folder containing that lambda, and delete the lambda and associated API gateway on AWS.

## Fetching web page source

To fetch a web page source, run `./fetch-page.sh <folder name>`

This will download a zip of the lambda code, then unzip it in the directory for the corresponding page

## Updating web page soure

To update the lambda for a page using the source in the corresponding directory, run `./update-page.sh <folder name>`

This will zip up the source files to create a deployment archive, then upload that to the corresponding lambda function.

## Tests

There is a test for `create-page.py`, called `test-create-page.py`. It can be run with `python3 test-create-page.py`.
