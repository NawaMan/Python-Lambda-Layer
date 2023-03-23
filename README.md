# Python-Lambda-Layer
An AWS application to create a proper Python Lambda Layer.

Python-Lambda-Layer is an AWS application that allows users to create a well-structured Python Lambda Layer.
This application simplifies the process of creating and managing Lambda Layers in AWS, making it easier for users to package their Python libraries and dependencies.
Particularly those who has no access to proper environment needed to create compatible layers (Python 3.9 on Linux).

With Python-Lambda-Layer, users can easily create a Layer that can be shared across multiple AWS Lambda functions.
This makes it possible to reuse the same code across different functions, which saves time and reduces the risk of errors.
The application is user-friendly and provides a straightforward interface that simplifies the entire process of creating and managing Lambda Layers.

# Background

__TLDR__: I need it.

AWS Lambda layer allows sharing of common components among AWS Lambda.
Using layers, the lambda code can stay lean and focus.
This also increasing the chance that the lambda code will stay in the limit of the online code editor
    which is very desirable as quick troubleshooting and tuning can be done there.

The layer zip file must be:
- packaged in a specific way, and
- include Linux x86/AMD that match the Lambda runtime environment.

The second requirement can be tricky for those not using Linux for development.
A common solution for this is to do it in a docker instance.
But that too can be problematic if the development machine is not capable of using docker (like my 7yo Mac Book Air).

This AWS application can create compatible layer zip files to be used for Python Lambda.
Being a lambda function it self means that it run on a compatible environment so it can produce a compatible layer zip file.

# Usage

__TLDR__: See [Setup](#setup) and [`example-Pillow.sh`](example-Pillow.sh).

The lambda accept request with layer (the name of the layer) and the list of requirements as input.

- The `layer` represents the name of the layer zip file to be produced.
- The `requirements` are the list of modules to be included with the layer.
  Each requirement item is simply the a line in PIP `requirements.txt` file.

Both values are to be serialized as JSON.

__Example__:
```
{"body":"{\"layer\":\"layer-pillow\",\"requirements\": [\"Pillow==9.4.0\"]}"}
```
This example create `layer-pillow.zip` that include `Pillow 9.4.0` module.

See [`example-Pillow.sh`](example-Pillow.sh).

The result layer zip file will be upload to the S3 bucket (known as the layer bucket -- see the configuration section below).
The lambda also returns the information about the result file.

Here is the result from the example:
```
{
  "statusCode": 200,
  "body": {
    "bucket": "nawaman-lambda-layers",
    "key": "layer-pillow.zip"
  }
}
```
where `nawaman-lambda-layers` is the layer bucket and `layer-pillow.zip` is the name of the layer zip file.

__NOTE:__ It is worth noting that you do not need to create a layer for `boto`. AWS already have those included in the lambda runtime.


# Setup

__TLDR__: See [Setup](#setup) and [`example-Pillow.sh`](example-Pillow.sh).

This application is consist of one lambda function which can take a list of required Python modules with a name
  and it creates a compatible layer zip file uploaded to an S3 bucket (the layer bucket).

## Configurations
Adjust the configuration in `configurations.sh`.
Except for S3 buckets (`LAMBDA_BUCKET` and `LAYERS_BUCKET`), most of the configuration can be left as they are.

Mandatory settings
- `LAMBDA_BUCKET` is the bucket that this lambda code will be stored for the deployment.
- `LAYERS_BUCKET` is the bucket that the result layer zip file will be uploaded.
  This value can also be overridden using environmental variable of the lambda (can be done without stack redeployment).

Other settings
- `STACK_NAME` is the name of the CloudFormation stack to be deployed on.
- `TEMPLATE_FILE` is the relative path the CloudFormation template file.
- `LAMBDA_NAME` is the name of the lambda to do this work.
- `LAMBDA_FOLDER` is the name of the folder inside the `LAMBDA_BUCKET` that this lambda code will be stored for the deployment.

Environmental Variables
- `LAYERS_BUCKET` -- see above.
- `VERBOSITY` is a flag indicating if the lambda should be logging its operation -- defaulted to `quiet`.
  Possible values are `quiet` and `verbose`.

## Bucket Creation
Since S3 bucket is global and only need to be created (no other settings that can be changed),
  the action of creating them are separated from other deployment.

Simply run the following command:
```
./setup-bucket.sh
```

## Deployment
This step deploys the application.

Simply run the following command:
```
./deploy.sh
```

## Update
Since CloudFormation does not check for update if lambda codes are stored in S3,
  any change made to the lambda are ignored.
Thus, if those are the change you made, you will need to re-deploy ([undeploy](#undeploy) then [deploy](#deployment)) explicitly. :frowning: -- sorry.

## Undeploy
Don't want it anymore -- trash it!

Simply run the following command:
```
./undeploy.sh
```
