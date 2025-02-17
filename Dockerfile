# Copyright 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

FROM ubuntu:bionic
RUN apt-get update \
 && apt-get install gnupg -y

RUN \
 apt-get update \
 && echo "deb http://repo.sawtooth.me/ubuntu/nightly bionic universe" >> /etc/apt/sources.list  \
 && (apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 44FC67F19B2466EA \
 || apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 44FC67F19B2466EA) \
 && apt-get update

RUN apt-get install -y --allow-unauthenticated -q python3-grpcio-tools \
    python3-pip \
    python3-sawtooth-rest-api \
    python3-sawtooth-sdk

RUN apt install libpq-dev python3-dev -y

RUN pip3 install \
    aiohttp \
    aiopg \
    bcrypt \
    itsdangerous \
    pycrypto \
    requests \
    psycopg2-binary \
    pymongo \
    nest_asyncio \
    aiohttp_cors \
    requests

WORKDIR /project/sawtooth-b4e

ENV PATH $PATH:/project/sawtooth-b4e/bin

CMD ['b4e-tp']
