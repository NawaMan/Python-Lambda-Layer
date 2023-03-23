#!/bin/bash

# This example create a layer that includes "Pillow" modules.


source configuration.sh


get-lambda-name() {
    aws cloudformation describe-stacks                                                                      \
        --stack-name $STACK_NAME                                                                            \
        --query 'Stacks[0].Outputs[?ExportName==`'$STACK_NAME'-CreateLayerLambdaFunctionName`].OutputValue' \
        --output text
}


LAMBDA_NAME=`get-lambda-name`


aws lambda invoke                                       \
    --function-name $LAMBDA_NAME                             \
    --payload '{"body":"{\"layer\":\"layer-pillow\",\"requirements\": [\"Pillow\"]}"}' \
    --cli-binary-format raw-in-base64-out \
    --output json \
    --no-cli-pager \
    /dev/stdout \
    | jq '.'