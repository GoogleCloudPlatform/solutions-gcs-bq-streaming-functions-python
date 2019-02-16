# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
This Cloud function moves a file from one bucket to another
'''

import base64
import os
import logging

from google.cloud import storage

CS = storage.Client()

def move_file(data, context):
    '''This function is executed from a Cloud Pub/Sub'''
    message = base64.b64decode(data['data']).decode('utf-8')
    file_name = data['attributes']['file_name']

    source_bucket_name = os.getenv('SOURCE_BUCKET')
    source_bucket = CS.get_bucket(source_bucket_name)
    source_blob = source_bucket.blob(file_name)

    destination_bucket_name = os.getenv('DESTINATION_BUCKET')
    destination_bucket = CS.get_bucket(destination_bucket_name)

    source_bucket.copy_blob(source_blob, destination_bucket, file_name)
    source_blob.delete()

    logging.info('File \'%s\' moved from \'%s\' to \'%s\': \'%s\'',
                 file_name,
                 source_bucket_name,
                 destination_bucket_name,
                 message)
