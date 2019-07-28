if [[ $# != "1" ]]
then
  echo "Usage: $0 <lambda name/folder name>"
  exit 1
fi

lambda_name=`basename $1`

download_link=`aws lambda get-function --function-name ${lambda_name} --query 'Code.Location' | xargs`
timestamp=`date -Iseconds | cut -c1-19`
zip_file="${lambda_name}-downloadedAt-${timestamp}.zip"
wget -O ${zip_file} ${download_link}
unzip ${zip_file} -d ${lambda_name}/src
rm ${zip_file}