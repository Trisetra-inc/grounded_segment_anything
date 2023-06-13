FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-devel

# Arguments to build Docker Image using CUDA
ARG USE_CUDA=0
ARG TORCH_ARCH=
# Define custom function directory
ARG FUNCTION_DIR="/home/appuser/Grounded-Segment-Anything"

ENV AM_I_DOCKER True
ENV BUILD_WITH_CUDA "${USE_CUDA}"
ENV TORCH_CUDA_ARCH_LIST "${TORCH_ARCH}"
ENV CUDA_HOME /usr/local/cuda/

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}
RUN mkdir -p ${FUNCTION_DIR}

RUN apt-get update && apt-get install --no-install-recommends wget ffmpeg=7:* \
    libsm6=2:* libxext6=2:* git=1:* nano=2.* \
    vim=2:* -y \
    && apt-get clean && apt-get autoremove && rm -rf /var/lib/apt/lists/*

# (Optional) Add Lambda Runtime Interface Emulator and use a script in the ENTRYPOINT for simpler local runs
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
ENTRYPOINT [ "/home/appuser/Grounded-Segment-Anything/entry.sh" ]
CMD [ "lambda.handler" ]

COPY . ${FUNCTION_DIR}

# Install python dependencies
RUN python -m pip install --no-cache-dir -r requirements.txt
