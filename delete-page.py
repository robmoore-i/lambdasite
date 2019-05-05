import sys
import subprocess
import json
import shutil

if (len(sys.argv) != 2):
    print("Usage: python3 delete-page.py <page name>")
    exit(1)

page_name = sys.argv[1]

lambda_name = page_name + "-webpage"
api_name = page_name + "-API"
folder_name = lambda_name

def aws_cmd(cmd):
    return json.loads(subprocess.check_output(cmd, shell=True).decode("utf8"))

def get_api_id(api_name):
    cmd = "aws apigateway get-rest-apis --query 'items[?name==`" + api_name + "`]'"
    return aws_cmd(cmd)[0]["id"]

def delete_api(api_id):
    cmd = "aws apigateway delete-rest-api --rest-api-id " + api_id
    subprocess.check_call(cmd, shell=True)

def delete_lambda(lambda_name):
    cmd = "aws lambda delete-function --function-name " + lambda_name
    subprocess.check_call(cmd, shell=True)

def delete_folder(folder_name):
    shutil.rmtree(folder_name)

delete_api(get_api_id(api_name))
delete_lambda(lambda_name)
delete_folder(folder_name)