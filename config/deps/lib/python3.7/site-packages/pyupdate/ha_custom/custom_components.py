"""Logic to handle custom_components."""
import os
import re
import sys
import requests
from requests import RequestException
from pyupdate.ha_custom import common
from pyupdate.log import Logger


class CustomComponents():
    """Custom component class."""

    def __init__(self, base_dir, custom_repos):
        """Init."""
        self.base_dir = base_dir
        self.custom_repos = custom_repos
        self.remote_info = {}
        self.log = Logger(self.__class__.__name__)

    async def get_info_all_components(self, force=False):
        """Return all remote info if any."""
        await self.log.debug(
            'get_info_all_components', 'Started with force ' + str(force))
        if not force and self.remote_info:
            return self.remote_info
        remote_info = {}
        repos = await common.get_repo_data('component', self.custom_repos)
        for url in repos:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    for name, component in response.json().items():
                        try:
                            if name in remote_info:
                                entry = remote_info.get(name, {})
                            else:
                                entry = {}
                            for attr in component:
                                entry['name'] = name
                                entry[attr] = component[attr]
                            remote_info[name] = entry
                        except KeyError:
                            print('Could not get remote info for ' + name)
            except RequestException:
                print('Could not get remote info for ' + url)
        stats = {'count': len(remote_info), 'components': remote_info.keys()}
        await self.log.debug('get_info_all_components', stats)
        self.remote_info = remote_info
        return remote_info

    async def get_sensor_data(self, force=False):
        """Get sensor data."""
        await self.log.debug(
            'get_sensor_data', 'Started with force ' + str(force))
        components = await self.get_info_all_components(force)
        cahce_data = {}
        cahce_data['domain'] = 'custom_components'
        cahce_data['has_update'] = []
        count_updateable = 0
        if components:
            for name, component in components.items():
                remote_version = component['version']
                local_file = self.base_dir + str(component['local_location'])
                local_version = await self.get_local_version(local_file)
                has_update = (
                    remote_version and remote_version != local_version)
                not_local = (remote_version and not local_version)
                if (not not_local and remote_version):
                    if has_update and not not_local:
                        count_updateable = count_updateable + 1
                        cahce_data['has_update'].append(name)
                    cahce_data[name] = {
                        "local": local_version,
                        "remote": remote_version,
                        "has_update": has_update,
                        "not_local": not_local,
                        "repo": component['visit_repo'],
                        "change_log": component['changelog'],
                    }
        await self.log.debug(
            'get_sensor_data', '[{}, {}]'.format(cahce_data, count_updateable))
        return [cahce_data, count_updateable]

    async def update_all(self):
        """Update all components."""
        await self.log.debug('update_all', 'Started')
        updates = await self.get_sensor_data()
        updates = updates[0]['has_update']
        if updates is not None:
            await self.log.debug('update_all', updates)
            for name in updates:
                await self.upgrade_single(name)
            await self.get_info_all_components(force=True)
        else:
            await self.log.debug('update_all', 'No updates avaiable')

    async def upgrade_single(self, name):
        """Update one component."""
        await self.log.info('upgrade_single', name + ' started')
        remote_info = await self.get_info_all_components()
        remote_info = remote_info[name]
        remote_file = remote_info['remote_location']
        local_file = self.base_dir + str(remote_info['local_location'])
        await common.download_file(local_file, remote_file)
        await self.downlaod_component_resources(name)
        await self.update_requirements(local_file)
        await self.log.info('upgrade_single', name + ' finished')

    async def install(self, name):
        """Install single component."""
        sdata = await self.component_data(name)
        await self.log.debug('install', name)
        if sdata:
            await self.log.debug('install', sdata)
            path = None
            comppath = self.base_dir + str(sdata['local_location'])
            await self.log.debug('install', comppath)
            if '.' in name:
                remove = comppath.split('/')[-1]
                path = comppath.split(remove)[0]
            elif comppath.split('/')[-1] == '__init__.py':
                path = comppath.split('__init__')[0]
            await self.log.debug('install', path)
            if path is not None:
                await self.log.debug('install', 'Creating dirs ' + path)
                os.makedirs(path, exist_ok=True)
            await self.upgrade_single(name)

    async def get_local_version(self, localpath):
        """Return the local version if any."""
        await self.log.debug('get_local_version', 'Started for ' + localpath)
        return_value = ''
        if os.path.isfile(localpath):
            filename = localpath
            directory, module_name = os.path.split(filename)
            module_name = os.path.splitext(module_name)[0]
            path = list(sys.path)
            sys.path.insert(0, directory)
            try:
                module = __import__(module_name)
            except Exception as err:  # pylint: disable=W0703
                module = None
                await self.log.debug('get_local_version', str(err))
            if module is not None:
                try:
                    return_value = module.__version__
                except Exception as err:  # pylint: disable=W0703
                    await self.log.debug('get_local_version', str(err))
                try:
                    return_value = module.VERSION
                except Exception as err:  # pylint: disable=W0703
                    await self.log.debug('get_local_version', str(err))
            sys.path[:] = path  # restore
            if module_name in sys.modules:
                del sys.modules[module_name]
        await self.log.debug('get_local_version', return_value)
        return return_value

    async def update_requirements(self, path):
        """Update the requirements for a python file."""
        await self.log.debug('update_requirements', 'Started for ' + path)
        requirements = None
        if os.path.isfile(path):
            with open(path, 'r') as local:
                ret = re.compile(r"^\bREQUIREMENTS\s*=\s*(.*)")
                for line in local.readlines():
                    matcher = ret.match(line)
                    if matcher:
                        val = str(matcher.group(1))
                        val = val.replace('[', '')
                        val = val.replace(']', '')
                        val = val.replace(',', ' ')
                        val = val.replace("'", "")
                        requirements = val
            local.close()
            if requirements is not None:
                for package in requirements.split(' '):
                    await self.log.info('update_requirements ', package)
                    await common.update(package)

    async def component_data(self, name):
        """Return component_data."""
        data = {}
        if self.remote_info is None:
            await self.get_info_all_components(True)
        component = self.remote_info.get(name, {})
        if component:
            data = component
        return data

    async def downlaod_component_resources(self, name):
        """Download extra resources for component."""
        await self.log.debug('downlaod_component_resources', 'Started')
        componentdata = await self.component_data(name)
        iscomponent = False
        if componentdata['local_location'].split('/')[-1] == '__init__.py':
            iscomponent = True
        if iscomponent:
            resources = componentdata.get('resources', [])
            await self.log.debug('downlaod_component_resources', resources)
            for resource in resources:
                target = self.base_dir + componentdata['local_location']
                target = target.split('__init__')[0]
                target = "{}{}".format(target, resource.split('/')[-1])
                await self.log.debug(
                    'downlaod_component_resources', 'resource: ' + resource)
                await self.log.debug(
                    'downlaod_component_resources', 'target: ' + target)
                await common.download_file(target, resource)
