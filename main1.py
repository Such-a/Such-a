import boto3
import os
from os import getenv
from dotenv import load_dotenv
from botocore.exceptions import ClientError, NoCredentialsError
import argparse
import logging
import json
import requests
from collections import defaultdict

load_dotenv()


def init_client():
    client = boto3.client(
        "s3",
        aws_access_key_id=getenv("aws_access_key_id"),
        aws_secret_access_key=getenv("aws_secret_access_key"),
        aws_session_token=getenv("aws_session_token"),
        region_name=getenv("aws_region_name")
    )
    client.list_buckets()
    print(client.list_buckets())
    return client


def bucket_exists(aws_s3_client, bucket_name) -> bool:
    try:
        response = aws_s3_client.head_bucket(Bucket=bucket_name)
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            return True
    except ClientError:
        # print(e)
        return False


def purge_bucket(aws_s3_client, bucket_name):
    object_keys = [{'Key': obj['Key']} for obj in aws_s3_client.list_objects(Bucket=bucket_name)['Contents']]
    response = aws_s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': object_keys})
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    return status_code == 200


def versioning(aws_s3_client, bucket_name, status: bool):
    versioning_status = "Enabled" if status else "Suspended"
    aws_s3_client.put_bucket_versioning(
        Bucket=bucket_name, VersioningConfiguration={"Status": versioning_status})


def rollback_to_version(aws_s3_client, bucket_name, file_name, version):
    aws_s3_client.copy_object(
        Bucket=bucket_name,
        Key=file_name,
        CopySource={'Bucket': bucket_name, 'Key': file_name, 'VersionId': version}
    )


def list_object_versions(aws_s3_client, bucket_name):
    response = aws_s3_client.list_object_versions(Bucket=bucket_name)
    for version in response.get('Versions', []):
        print(f"Version ID: {version['VersionId']}, Key: {version['Key']}")


def public_read_policy(bucket_name):
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*",
            }
        ],
    }

    return json.dumps(policy)


def multiple_policy(bucket_name):
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "s3:ListBucketVersions",
                    "s3:PutObjectAcl",
                    "s3:GetObject",
                    "s3:GetObjectAcl",
                    "s3:DeleteObject"
                ],
                "Resource": "*",
                "Effect": "Allow",
                "Principal": "*"
            }
        ]
    }

    return json.dumps(policy)


def assign_policy(aws_s3_client, policy_function, bucket_name):
    policy = None
    response = None
    if policy_function == "public_read_policy":
        policy = public_read_policy(bucket_name)
        response = "public read policy assigned!"
    elif policy_function == "multiple_policy":
        policy = multiple_policy(bucket_name)
        response = "multiple policy assigned!"

    if (not policy):
        print('please provide policy')
        return

    aws_s3_client.delete_public_access_block(Bucket=bucket_name)
    aws_s3_client.put_bucket_policy(
        Bucket=bucket_name, Policy=policy
    )

    print(response)


def read_bucket_policy(aws_s3_client, bucket_name):
    policy = aws_s3_client.get_bucket_policy(Bucket=bucket_name)

    status_code = policy["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        return policy["Policy"]
    return False


def set_object_access_policy(aws_s3_client, bucket_name, file_name):
    response = aws_s3_client.put_object_acl(
        ACL="public-read",
        Bucket=bucket_name,
        Key=file_name
    )
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        return True
    return False


class S3Uploader:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

    def upload_file(self, file_path, object_name):
        self.s3_client.upload_file(file_path, self.bucket_name, object_name)
        print(f"File '{file_path}' uploaded as '{object_name}' using upload_file.")

    def upload_fileobj(self, file_path, object_name):
        with open(file_path, 'rb') as file:
            self.s3_client.upload_fileobj(file, self.bucket_name, object_name)
        print(f"File '{file_path}' uploaded as '{object_name}' using upload_fileobj.")

    def put_object(self, file_path, object_name):
        self.s3_client.put_object(Bucket=self.bucket_name, Key=object_name, Body=open(file_path, 'rb'))
        print(f"File '{file_path}' uploaded as '{object_name}' using put_object.")


def get_objects(aws_s3_client, bucket_name) -> None:
    for key in aws_s3_client.list_objects(Bucket=bucket_name)['Contents']:
        print(f"Object Key: {key['Key']}, Size: {key['Size']} bytes")


def download_and_upload_file(url, local_filename, bucket_name):
    # Download file from URL
    response = requests.get(url)
    with open(local_filename, 'wb') as f:
        f.write(response.content)

    # Upload file to S3 bucket
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(local_filename, bucket_name, os.path.basename(local_filename))
        print("Upload Successful")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")

def count_extensions_usage(aws_s3_client, bucket_name):
    try:
        response = aws_s3_client.list_objects(Bucket=bucket_name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            return "Bucket does not exist"
        else:
            return f"Error: {e}"

    if 'Contents' not in response:
        return "No objects in the bucket"

    extensions_usage = defaultdict(lambda: {'count': 0, 'usage': 0.0})

    for obj in response['Contents']:
        key = obj['Key']
        size_bytes = obj['Size']
        size_mb = size_bytes / (1024 * 1024)

        extension = key.split('.')[-1]
        extensions_usage[extension]['count'] += 1
        extensions_usage[extension]['usage'] += size_mb

    output = ""
    for ext, data in extensions_usage.items():
        output += f"{ext}: {data['count']}, usage: {data['usage']:.2f} MB\n"

    return output



def main():
    global bucket_name
    parser = argparse.ArgumentParser(
        description="CLI program that helps with S3 buckets.",
        prog='main.py',
        epilog='DEMO APP - 2 FOR BTU_AWS'
    )
    parser.add_argument("-be",
                        "--bucket_exists",
                        help="flag to check if bucket exists",
                        choices=["False", "True"],
                        type=str,
                        nargs="?",
                        const="True",
                        default="False")

    parser.add_argument("-pos",
                        "--purge_objects",
                        help="purges objects",
                        action='store_true')

    parser.add_argument("-vers",
                        "--versioning",
                        type=str,
                        help="enable or disable versioning",
                        choices=["True", "False"])

    parser.add_argument("-r_b_t",
                        "--roll_back_to",
                        type=str,
                        help="rollback to",
                        default=None)

    parser.add_argument("-l_v",
                        "--list_versions",
                        help="list versions",
                        action='store_true')

    parser.add_argument("-rp",
                        "--read_policy",
                        help="flag to read bucket policy.",
                        choices=["False", "True"],
                        type=str,
                        nargs="?",
                        const="True",
                        default="False")

    parser.add_argument("-arp",
                        "--assign_read_policy",
                        help="flag to assign read bucket policy.",
                        choices=["False", "True"],
                        type=str,
                        nargs="?",
                        const="True",
                        default="False")

    parser.add_argument("-amp",
                        "--assign_missing_policy",
                        help="flag to assign read bucket policy.",
                        choices=["False", "True"],
                        type=str,
                        nargs="?",
                        const="True",
                        default="False")

    parser.add_argument("-sobap",
                        "--set_object_access_policy",
                        help="set object access policy",
                        action='store_true')

    parser.add_argument("-rpp",
                        "--read_public_policy",
                        help="flag to read public bucket policy.",
                        action='store_true')

    parser.add_argument('name', nargs="?", type=str, help="Pass object name.")
    parser.add_argument('bucket_name', type=str, help="Pass bucket name.")
    parser.add_argument("-du", "--download_upload", choices=["False", "True"], help="Download and upload to bucket",
                        type=str, nargs="?", const="True", default="False")
    parser.add_argument("-ol", "--object_link", type=str, help="Link to download and upload to bucket", default=None)
    parser.add_argument("-loc_o", "--local_object", type=str, help="Upload local object", default=None)
    parser.add_argument("-k_f_n", "--keep_file_name", help="File name", action='store_false')
    parser.add_argument("-u_t", "--upload_type", type=str, help="Upload function type",
                        choices=["upload_file", "upload_fileobj", "put_object", "multipart_upload"])
    parser.add_argument("-lo", "--list_objects", type=str, help="List bucket objects", nargs="?", const="True",
                        default="False")

    parser.add_argument("-cer", "--count_extensions_usage", type=str, help="Count extensions usage")

    args = parser.parse_args()
    s3_client = init_client()
    uploader = S3Uploader(bucket_name=args.bucket_name)

    print("Parsed arguments:")
    print(args)

    if args.bucket_exists == "True":
        bucket_name = input("Enter bucket name: ")
        exists = bucket_exists(s3_client, bucket_name)
        print(f"Bucket {bucket_name} exists: {exists}")

    if (args.purge_objects):
        bucket_name = input("Enter bucket name to purge objects: ")
        success = purge_bucket(s3_client, bucket_name)
        print(f'Purged objects from bucket {bucket_name}: {success}')

    if args.versioning is not None:
        bucket_name = input("Enter bucket name to enable/disable versioning: ")
        if args.versioning == "True":
            versioning(s3_client, bucket_name, True)
            print("Enabled versioning on bucket %s." % bucket_name)
        elif args.versioning == "False":
            versioning(s3_client, bucket_name, False)
            print("Disabled versioning on bucket %s." % bucket_name)

    if args.roll_back_to:
        bucket_name = input("Enter bucket name: ")
        file_name = input("Enter file name: ")
        version = args.roll_back_to
        rollback_to_version(s3_client, bucket_name, file_name, version)
        print(f"Rolled back {file_name} to version {version}.")

    if args.list_versions:
        bucket_name = input("Enter bucket name: ")
        list_object_versions(s3_client, bucket_name)

    if args.read_policy == "True":
        if args.read_public_policy:
            # Read the public policy directly
            bucket_policy = public_read_policy(args.bucket_name)
        else:
            # Read the bucket policy from AWS S3
            bucket_policy = read_bucket_policy(s3_client, args.bucket_name)
        print(bucket_policy)

    if args.read_policy == "True":
        bucket_name = input("Enter bucket name: ")
        print(read_bucket_policy(s3_client, bucket_name))

    if args.assign_read_policy == "True":
        bucket_name = input("Enter bucket name: ")
        assign_policy(s3_client, "public_read_policy", bucket_name)

    if args.assign_missing_policy == "True":
        bucket_name = input("Enter bucket name: ")
        assign_policy(s3_client, "multiple_policy", bucket_name)

    if args.set_object_access_policy:
        bucket_name = input("Enter bucket name: ")
        file_name = input("Enter file name: ")
        success = set_object_access_policy(s3_client, bucket_name, file_name)
        if success:
            print(f"Object access policy set for {file_name} in bucket {bucket_name}.")
        else:
            print(f"Failed to set object access policy for {file_name} in bucket {bucket_name}.")

    if args.upload_type == "upload_file":
        print("Calling upload_file function")
        uploader.upload_file(args.local_object, args.name)
    elif args.upload_type == "upload_fileobj":
        print("Calling upload_fileobj function")
        uploader.upload_fileobj(args.local_object, args.name)
    elif args.upload_type == "put_object":
        print("Calling put_object function")
        uploader.put_object(args.local_object, args.name)
    else:
        print("Invalid upload type specified.")


    if args.list_objects:
        if args.bucket_name:
            get_objects(s3_client, args.bucket_name)
        else:
            print("Bucket name is required to list objects.")
    else:
        pass

    if args.download_upload:
        if args.object_link and args.local_object and args.bucket_name:
            download_and_upload_file(args.object_link, args.local_object, args.bucket_name)
        else:
            print("Please provide a valid URL, local file path, and bucket name for download and upload.")
            return

    if args.count_extensions_usage:
        bucket_name = input("Enter bucket name: ")
        output = count_extensions_usage(s3_client, bucket_name)
        print(output)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        main()
    except ClientError as error:
        if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            logging.warning("Bucket already exists! Using it.")
        else:
            logging.error(error)
    except ValueError as error:
        logging.error(error)



