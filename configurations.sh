#!/bin/bash

# Application related configurations
STACK_NAME=lambda-layer-creator
TEMPLATE_FILE=src/infrastructure.yml
LAMBDA_NAME=create-layer-lambda-function
LAMBDA_BUCKET=nawaman-lambdas
LAMBDA_FOLDER=create-layer

# Output configurations
LAYERS_BUCKET=nawaman-lambda-layers
