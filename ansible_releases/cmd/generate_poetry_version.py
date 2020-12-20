# Copyright 2019 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os

import pbr.version


def generate_version_info():
    version_info = pbr.version.VersionInfo('random')
    semantic_version = version_info.semantic_version()
    release_string = semantic_version._long_version('-')

    cmd = 'poetry version %s' % release_string
    print(release_string)
    os.system(cmd)


def main():
    generate_version_info()
