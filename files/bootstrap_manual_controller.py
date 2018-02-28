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
# pylint: disable=c0111,c0301,c0325,c0103,r0913,r0902,e0401,C0302, R0914
import asyncio
import logging
import os
import hashlib
from pathlib import Path
from subprocess import check_output
import traceback
import sys
import yaml
from juju import tag
from juju.client import client
sys.path.append('/opt')
from sojobo_api import settings  #pylint: disable=C0413
from sojobo_api.api import w_datastore as datastore, w_juju as juju  #pylint: disable=C0413


class JuJu_Token(object):  #pylint: disable=R0903
    def __init__(self):
        self.username = settings.JUJU_ADMIN_USER
        self.password = settings.JUJU_ADMIN_PASSWORD
        self.is_admin = True


async def create_controller(name, url):
    try:
        logger.info('Adding controller to database')
        token = JuJu_Token()
        datastore.create_manual_controller(name, c_type, url)
        datastore.add_user_to_controller(name, 'admin', 'superuser')

        check_output(['juju', 'bootstrap', '--agent-version=2.3.0', 'manual/{}'.format(url), name])
        pswd = token.password

        logger.info('Setting admin password')
        check_output(['juju', 'change-user-password', 'admin', '-c', name],
                     input=bytes('{}\n{}\n'.format(pswd, pswd), 'utf-8'))

        logger.info('Updating controller in database')
        con_data = {}
        with open(os.path.join(str(Path.home()), '.local', 'share', 'juju', 'controllers.yaml'), 'r') as data:
            con_data = yaml.load(data)
        datastore.set_controller_state(
            name,
            'ready',
            con_data['controllers'][name]['api-endpoints'],
            con_data['controllers'][name]['uuid'],
            con_data['controllers'][name]['ca-cert'])

        logger.info('Connecting to controller')
        controller = Controller()

        logger.info('Adding existing credentials and default models to database')
        credentials = datastore.get_credentials(token.username)
        await controller.connect(con_data['controllers'][name]['api-endpoints'][0], token.username, token.password, con_data['controllers'][name]['ca-cert'])
        controller_facade = client.ControllerFacade.from_connection(controller.connection)
        models = await controller_facade.AllModels()
        for model in models.user_models:
            new_model = datastore.create_model(model.model.name, state='Model is being deployed', uuid='')
            datastore.add_model_to_controller(model.model.name, new_model["_key"])
            datastore.set_model_state(new_model["_key"], 'ready', credential=cred_name, uuid=model.model.uuid)
            datastore.set_model_access(new_model["_key"], token.username, 'admin')
        await controller.disconnect()
        logger.info('Controller succesfully created!')
    except Exception:  #pylint: disable=W0703
        datastore.destroy_controller(name)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for l in lines:
            logger.error(l)
        datastore.set_controller_state(name, 'error')


if __name__ == '__main__':
    logger = logging.getLogger('bootstrap_manual_controller')
    hdlr = logging.FileHandler('{}/log/bootstrap_manual_controller.log'.format(settings.SOJOBO_API_DIR))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    loop = asyncio.get_event_loop()
    loop.set_debug(False)
    loop.run_until_complete(create_manual_controller(sys.argv[1], sys.argv[2]))
    loop.close()
