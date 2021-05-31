import logging
import boto3
from botocore.exceptions import ClientError
import subprocess
# TODO learn how to use botostubs properly
import botostubs

# TODO adding functional module to allow the code identify which OS it is using and decide the correct shell command
subprocess.run(['clear'])

# TODO tidy up the entire code and reinvent the function documentions
# this function return the list of objects (files) already existing in the given bucket
def get_existing_objects(bucket_name):
    
    existing_objs_list = []
    s3_resource = boto3.resource('s3')  # type: botostubs.S3
    
    # get the bucket with name = bucket_name
    bucket = s3_resource.Bucket(bucket_name)

    # get filenames (keys) of all objects with Prefix = prefix
    for obj in bucket.objects.all():
        object_name = obj.key  # remove prefix from object key to get just the key
        if len(object_name) > 0:
            existing_objs_list.append(object_name)

    return existing_objs_list


# the function to upload the file to the given bucket
def upload_file(file_name, bucket, object_name=None):
    """This function is used to upload file from local machine to AWS S3 bucket

    Args:
        file_name (string): [description]
        bucket (string): [description]
        object_name (string, optional): [description]. Defaults to None.

    Returns:
        bool: output boolean information to identify whether the file is successfully uploaded
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')  # type: botostubs.S3
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False

    return True


# START OF MAIN

print('### Utility to Upload files to S3: ###\n')

# getting the list of files to choose from the local computer
# TODO convert all the back-slash (\) inside of the path string into forward-slash (/)
path = 'G:\Coding\AWS\AWS_project\AWS_UKDER1_Rekognition\Image_to_upload'
output = subprocess.run(['ls', path], stdout=subprocess.PIPE, text=True).stdout.split('\n')

# the bucket where the uploads are going to
bucket_name = 'ukder1-image-recognition'

options_list = []
for file in output:
    if len(file) > 0:
        options_list.append(file)

print('The existing files are:')
for num, option in enumerate(options_list):
    print(str(num + 1) + " - " + option)

file_option = int(input('\nEnter the file option (e.g. 1) from the list provided:'))

if file_option > 0 and file_option <= len(options_list):  # If valid file option
    file_name = options_list[file_option - 1]
    print('File to Upload: ', file_name)
    uploadYN = input('Proceed with Upload Y/N?').upper()

    if uploadYN == 'Y':

        # get the list of existing file to compare to the file we want to upload
        existing_objs_list = get_existing_objects(bucket_name)

        if not file_name in existing_objs_list:  # if file to upload doesn't exist in the existing_obj_list
            print('\nUploading ' + file_name + '...')

            if upload_file(path + '\\' + file_name, bucket_name, file_name):
                print('Upload Successful!')
            else:
                print('Error trying to upload!')
        else:
            print(f'{file_name} already exists in {bucket_name}')
            print('Upload aborted!')

else:
    print('Invalid option!')
