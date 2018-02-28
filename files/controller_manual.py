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
from sojobo_api import settings
from subprocess import check_output, Popen

def create_controller(name, data):
    Popen(["python3", "{}/scripts/bootstrap_manual_controller.py".format(settings.SOJOBO_API_DIR), name, data['url']])
    return 202, 'Environment {} is being created on url {}'.format(name, data['url'])

def get_supported_series():
    return ['trusty', 'xenial', 'yakkety']

def generate_cred_file(name, credentials):
    raise NotImplementedError

def get_supported_regions():
    raise NotImplementedError

def check_valid_credentials(credentials):
    raise NotImplementedError

def add_credential(user, data):
    raise NotImplementedError
