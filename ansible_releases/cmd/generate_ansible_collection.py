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

import pbr.version

from ruamel.yaml import YAML


def generate_version_info():
    version_info = pbr.version.VersionInfo('random')
    semantic_version = version_info.semantic_version()

    yaml = YAML()
    yaml.explicit_start = True
    yaml.indent(sequence=4, offset=2)

    config = yaml.load(open('galaxy.yml'))

    try:
        galaxy_version = str(config['version']).replace("-", ".")
        galaxy_version = pbr.version.SemanticVersion.from_pip_string(
            galaxy_version)
    except (ValueError, TypeError):
        galaxy_version = semantic_version

    release_version = max(galaxy_version, semantic_version)
    release_string = release_version._long_version('-')
    config['version'] = release_string

    with open('galaxy.yml', 'w') as fp:
        yaml.dump(config, fp)
    print(f"{config['namespace']}-{config['name']}-{config['version']}.tar.gz")


def main():
    generate_version_info()
