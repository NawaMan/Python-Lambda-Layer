#!/bin/bash

source configuration.sh


aws cloudformation delete-stack --stack-name $STACK_NAME
