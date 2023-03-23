#!/bin/bash

source configuration.sh

VERBOSITY=quiet
# VERBOSITY=verbose


echo "Ensure bucket: s3://$LAMBDA_BUCKET"
aws s3api create-bucket             \
    --bucket $LAMBDA_BUCKET         \
    --acl bucket-owner-full-control \
    --no-cli-pager
echo ""

echo "Ensure folder: s3://$LAMBDA_BUCKET/$LAMBDA_FOLDER/"
aws s3api put-object                \
    --bucket $LAMBDA_BUCKET         \
    --key $LAMBDA_FOLDER/           \
    --acl bucket-owner-full-control \
    --no-cli-pager
echo ""


pushd src

echo "Zip lambda file: $LAMBDA_NAME.zip"
zip -r $LAMBDA_NAME.zip *

echo "Update lambda file."
aws s3 cp $LAMBDA_NAME.zip "s3://$LAMBDA_BUCKET/$LAMBDA_FOLDER/$LAMBDA_NAME.zip"
echo ""

rm $LAMBDA_NAME.zip

popd


aws cloudformation deploy                               \
    --stack-name    "$STACK_NAME"                       \
    --template-file ./"$TEMPLATE_FILE"                  \
    --capabilities  CAPABILITY_IAM CAPABILITY_NAMED_IAM \
    --parameter-overrides                               \
        LambdaName="$LAMBDA_NAME"                       \
        LambdaBucket="$LAMBDA_BUCKET"                   \
        LambdaKey=$LAMBDA_FOLDER/$LAMBDA_NAME.zip       \
        LayersBucket="$LAYERS_BUCKET"                   \
        Verbosity="$VERBOSITY"
