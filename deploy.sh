#!/bin/bash

# 1. Build your Docker image using the following command
make build-image > build.log 2>&1

# 2. After the build completes, tag your image so you can push the image to this repository:
docker tag grounded_segment_anything:latest 832473540695.dkr.ecr.us-east-1.amazonaws.com/grounded_segment_anything:latest

# 3. Retrieve an authentication token and authenticate your Docker client to your registry.
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 832473540695.dkr.ecr.us-east-1.amazonaws.com

# 4. Run the following command to push this image to your newly created AWS repository:
docker push 832473540695.dkr.ecr.us-east-1.amazonaws.com/grounded_segment_anything:latest

# 5. Deploy the lambda
sls deploy -s prod

# 6. Remove the .serverless folder
rm -rf .serverless
