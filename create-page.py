import sys
import subprocess
import json
import shutil
import os

if (len(sys.argv) != 2):
    print("Usage: python3 create-page.py <page name>")
    exit(1)

page_name = sys.argv[1]

def aws_cmd(cmd):
    return json.loads(subprocess.check_output(cmd, shell=True).decode("utf8"))

def create_new_api_gateway(page_name):
    cmd = "aws apigateway create-rest-api --name " + page_name + "-API --region eu-west-2"
    return aws_cmd(cmd)["id"]

def delete_api_command(api_id):
    return "aws apigateway delete-rest-api --rest-api-id " + api_id

def get_root_resource_id(api_id):
    cmd = "aws apigateway get-resources --rest-api-id " + api_id + " --region eu-west-2"
    return aws_cmd(cmd)["items"][0]["id"]

def create_api_resource(api_id, lambda_name):
    root_resource_id = get_root_resource_id(api_id)
    cmd = "aws apigateway create-resource --rest-api-id " + api_id + " --region eu-west-2 --parent-id " + root_resource_id + " --path-part " + lambda_name
    return aws_cmd(cmd)["id"]

def assign_get_method_to_resource(api_id, resource_id):
    cmd = "aws apigateway put-method --rest-api-id " + api_id + " --region eu-west-2 --resource-id " + resource_id + " --http-method GET --authorization-type \"NONE\""
    return aws_cmd(cmd)

def assign_get_method_response(api_id, resource_id):
    cmd = "aws apigateway put-method-response --region eu-west-2 --rest-api-id " + api_id + " --resource-id " + resource_id + " --http-method GET --status-code 200"
    return aws_cmd(cmd)

def create_lambda(page_name):
    archive_zip_file = "initial-code.zip"
    cmd = "aws lambda create-function --function-name " + page_name + "-webpage --runtime nodejs8.10 --role arn:aws:iam::081744355171:role/service-role/DefaultRole --handler index.handler --zip-file fileb://" + archive_zip_file
    return aws_cmd(cmd)["FunctionArn"]

def delete_lambda_command(lambda_arn):
    return "aws lambda delete-function --function-name " + lambda_arn

def create_lambda_integration(api_id, resource_id, lambda_arn):
    cmd = "aws apigateway put-integration --region eu-west-2 --rest-api-id " + api_id + " --resource-id " + resource_id + " --http-method GET --type AWS_PROXY --integration-http-method POST --uri arn:aws:apigateway:eu-west-2:lambda:path/2015-03-31/functions/" + lambda_arn + "/invocations"
    return aws_cmd(cmd)

def assign_lambda_integration_response(api_id, resource_id):
    cmd = "aws apigateway put-integration-response --region eu-west-2 --rest-api-id " + api_id + " --resource-id " + resource_id + " --http-method GET --status-code 200 --selection-pattern \"\""
    return aws_cmd(cmd)

def create_deployment(api_id):
    cmd = "aws apigateway create-deployment --rest-api-id " + api_id + " --stage-name default --region eu-west-2"
    return aws_cmd(cmd)

def get_api_arn(api_id, lambda_arn, lambda_name):
    return lambda_arn.replace("lambda", "execute-api").replace("function:" + lambda_name, api_id)

def add_lambda_execution_permissions(lambda_name, api_arn):
    cmd = "aws lambda add-permission --function-name " + lambda_name + " --statement-id apigateway-" + lambda_name + " --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn " + api_arn + "/default/GET/" + lambda_name + " --region eu-west-2"
    return aws_cmd(cmd)

def get_lambda_invocation_url(api_id, lambda_name):
    return "https://" + api_id + ".execute-api.eu-west-2.amazonaws.com/default/" + lambda_name

def copy_initial_page_folder(page_name):
    shutil.copytree("initial_page", page_name)

def update_page_folder_endpoint_file(page_name, lambda_invocation_url):
    with open(os.path.join(page_name, "endpoint"), "w") as endpoint_file:
        endpoint_file.write(lambda_invocation_url)

api_id = create_new_api_gateway(page_name)
root_resource_id = get_root_resource_id(api_id)
lambda_name = page_name + "-webpage"
resource_id = create_api_resource(api_id, lambda_name)
assign_get_method_to_resource(api_id, resource_id)
assign_get_method_response(api_id, resource_id)
lambda_arn = create_lambda(page_name)
create_lambda_integration(api_id, resource_id, lambda_arn)
assign_lambda_integration_response(api_id, resource_id)
create_deployment(api_id)
api_arn = get_api_arn(api_id, lambda_arn, lambda_name)
add_lambda_execution_permissions(lambda_name, api_arn)
lambda_invocation_url = get_lambda_invocation_url(api_id, lambda_name)
copy_initial_page_folder(page_name)
update_page_folder_endpoint_file(page_name, lambda_invocation_url)
print(lambda_invocation_url)