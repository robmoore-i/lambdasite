if [[ $# != "1" ]]
then
  echo "Usage: $0 <lambda name/folder name>"
  exit 1
fi

lambda_name=`basename $1`
cd ${lambda_name}

mkdir -p build
timestamp=`date -Iseconds | cut -c1-19`
archive_zip_file="build/${lambda_name}-${timestamp}.zip"
source_files=`ls src`

# Copy-spill source files into current directory
for source_file in $source_files
do
    cp src/$source_file .
done

# Zip up index to make the initial archive
zip $archive_zip_file "index.js"
# Update the archive with all the other files
for source_file in $source_files
do
    zip -u $archive_zip_file $source_file
done

# Clean up the spilled files
for source_file in $source_files
do
    rm $source_file
done

aws lambda update-function-code --function-name ${lambda_name} --zip-file fileb://$archive_zip_file --publish
cd ..
cat ${lambda_name}/endpoint
