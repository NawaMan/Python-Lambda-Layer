# Lambda to create lambda layer.

import json
import os
import boto3
import subprocess
import zipfile
from io import BytesIO
import tempfile
import traceback
from layer import create


s3 = boto3.client('s3')


def upload(dir: str, target:str, layer: str, verbose: bool):
    path=f"{dir}/{layer}.zip"
    key=f"{layer}.zip"
    with open(path, 'rb') as file:
        s3.upload_fileobj(file, target, key)

    if verbose:
        print(f"Uploading path={path} to bucket={target} key={key}")


def process(dir: str, target: str, layer: str, requirements: list[str], verbose: bool):
    with tempfile.TemporaryDirectory() as dir:
        create(dir, layer, requirements, verbose)
        upload(dir, target, layer, verbose)


def handler(event, context):
    target  = os.environ['LAYERS_BUCKET']
    verbose = os.environ['VERBOSITY'].lower() == 'verbose'
    
    payload      = json.loads(event['body'])
    layer        = payload['layer']
    requirements = payload['requirements']

    if verbose:
        print(f"Creating layer={layer} for requirements={requirements}")

    try:
        with tempfile.TemporaryDirectory() as dir:
            process(str(dir), target, layer, requirements, verbose)

        return {
            'statusCode': 200,
            'body': {
                "bucket": target,
                "key":    f"{layer}.zip"
            }
        }
    except Exception as e:
        stack_trace = traceback.format_exc()
        return {
            'statusCode': 500,
            'body': 'An error occurred: ' + str(e),
            'stackTrace': stack_trace
        }
