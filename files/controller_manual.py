# !/usr/bin/env python3
# Copyright (C) 2017  Qrama
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# pylint: disable=c0111,c0301,c0325, r0903,w0406,e0401
import json
from subprocess import check_output

def create_controller(name, url):
    output = check_output(['juju', 'bootstrap', '--agent-version=2.3.0', 'manual/{}'.format(url), name])
    return output


def get_supported_series():
    return ['trusty', 'xenial', 'yakkety']


def generate_cred_file(name, credentials):
    result = {
        'type': 'jsonfile',
        'name': name,
        'key': {'file': str(json.dumps(credentials))}
    }
    return result


def get_supported_regions():
    return []
