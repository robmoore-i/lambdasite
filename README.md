# lambdasite

## Creating web pages

To create a new web page, run `python3 create-page.py <page name>`.

This will create a lambda, served through API gateway, and a folder for lambda. The lambda serves a HTML document found at `<page name>/src/document.html`. There is a script `<page name>/update-lambda.sh` which will automatically update the live lambda.

## Deleting web pages

To delete a web page, run `python3 delete-page.py <page name>`.

This will delete the local folder containing that lambda, and delete the lambda and associated API gateway on AWS.

## Tests

There is a test for `create-page.py`, called `test-create-page.py`. It can be run with `python3 test-create-page.py`.