#!/bin/bash

# Set up the layer buckets.

source configuration.sh


aws s3api create-bucket             \
    --bucket $LAYERS_BUCKET         \
    --acl bucket-owner-full-control \
    --no-cli-pager
