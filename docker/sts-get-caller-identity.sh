#!/bin/bash

identity=$(aws sts get-caller-identity)

export AWS_ASSUMED_ACCOUNT_ID=$(echo $identity | jq .Account | xargs)
export AWS_ASSUMED_ROLE_ARN=$(echo $identity | jq .Arn | xargs)
