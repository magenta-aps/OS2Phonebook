# https://magenta.dk
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
"""Import org units and employees from MO."""

import abc
import contextlib
import datetime
import json
import multiprocessing.dummy
import pathlib
import shutil
import traceback

import click
import pysolr

from os2mo_tools import mo_api

SECRET = 'Hemmelig'


def log(msg, *args, **kwargs):
    ts = datetime.datetime.now().strftime('%c')

    print(("[{}] " + msg).format(ts, *args, **kwargs))


def is_visible(a):
    """Decide if address is visible or protected (secret)."""
    # TODO: Change when backend starts using scope to indicate visibility.
    return not ('visibility' in a and a['visibility']['user_key'] == SECRET)


def get_root_uuid(ou):
    """Get root of current org unit."""
    ou_dict = ou.json

    while ou_dict['parent']:
        ou_dict = ou_dict['parent']
    return ou_dict['uuid']


def get_orgunit_data(ou):
    """Get the data we need to display for this particular org. func."""
    # Parent - UUID if exists, ROOT if not.
    parent = ou.json['parent']['uuid'] if ou.json['parent'] else 'ROOT'
    # For employees, we need job function, name and UUID.
    employees = [
        (
            e['person']['name'], e['person']['uuid'],
            e['engagement_type']['name'], e['job_function']['name']
        ) for e in ou.engagement
    ]
    # For associateds: Association type, job function, name and UUID.
    associated = [
        (
            a['person']['name'], a['person']['uuid'],
            a['association_type']['name']
        ) for a in ou.association if a
    ]

    # For departments, we need name and UUID.
    departments = [(c['name'], c['uuid']) for c in ou.children]
    # For locations, their type and content.
    locations = [
        (
            a['address_type']['name'], a['address_type']['user_key'],
            a['address_type']['scope'], a['name']
        ) for a in ou.address if is_visible(a)
    ]
    # For managers, manager type and name and UUID.
    managers = [
        (
            m['manager_type']['name'],
            m['person']['name'] if m['person'] else None,
            m['person']['uuid'] if m['person'] else None
        ) for m in ou.manager
    ]

    # Get root UUID of current org unit.
    root_uuid = get_root_uuid(ou)

    orgunit_data = dict(
        uuid=ou.json['uuid'],
        name=ou.json['name'],
        root_uuid=root_uuid,
        parent=parent,
        locations=locations,
        employees=employees,
        departments=departments,
        associated=associated,
        managers=managers
    )
    orgunit_data['document'] = json.dumps(orgunit_data, sort_keys=True)

    return orgunit_data


def get_employee_data(employee):
    """Get the data we need to display this employee."""
    # For locations, their type and content.
    locations = [
        (
            a['address_type']['scope'], a['name']
        ) for a in employee.address if is_visible(a)
    ]
    # For departments, department name, UUID as well as engagement and
    # job function name.
    departments = [
        (
            e['org_unit']['name'], e['org_unit']['uuid'],
            e['engagement_type']['name'], e['job_function']['name']
        ) for e in employee.engagement

    ]
    # Manager associations, if any
    managing = [
        (
            m['org_unit']['name'],
            m['org_unit']['uuid'], m['manager_type']['name']
        ) for m in employee.manager
    ]
    # Associated units - association type, name and UUID of association
    associated_units = [
        (
            a['org_unit']['name'],
            a['org_unit']['uuid'], a['association_type']['name']
         ) for a in employee.association
    ]
    employee_data = dict(
        uuid=employee.json['uuid'],
        name=employee.json['name'],
        locations=locations,
        departments=departments,
        managing=managing,
        associated=associated_units
    )
    employee_data['document'] = json.dumps(employee_data, sort_keys=True)

    return employee_data


def write_phonebook_data(writer, jobs):
    """Write data to store in backend DB.

    The ``writer`` argument are subclasses of
    :py:class:`AbstractWriter`.

    """
    ous = mo_api.get_ous()
    employees = mo_api.get_employees()

    def handler(getter, writer):
        def handle_this(obj):
            data = getter(obj)
            writer(data)
        return handle_this

    ou_handler = handler(get_orgunit_data, writer.write_unit)
    employee_handler = handler(get_employee_data, writer.write_employee)

    p = multiprocessing.dummy.Pool(jobs)
    # First, org units
    p.map(ou_handler, (mo_api.OrgUnit(ou['uuid']) for ou in ous))

    # Now, employees
    p.map(employee_handler, (mo_api.Employee(e['uuid']) for e in employees))

    # Finally, wait
    p.close()
    p.join()


class AbstractWriter(abc.ABC):
    def __init__(self, verbose=False):
        self.__verbose = verbose

    @abc.abstractmethod
    def write(self, type, data):
        pass

    @abc.abstractmethod
    def clean(self, type):
        pass

    def _do_write(self, type, data):
        if self.__verbose:
            log("{}: {}", type, data['uuid'])

        self.write(type, data)

    def write_unit(self, data):
        self._do_write('departments', data)

    def write_employee(self, data):
        self._do_write('employees', data)


class FileWriter(AbstractWriter):
    def __init__(self, base_dir, verbose=False):
        super().__init__(verbose)
        self.base_dir = pathlib.Path(base_dir)

    def clean(self):
        if self.base_dir.exists():
            shutil.rmtree(str(self.base_dir))

    def write(self, type, data):
        basename = data['uuid']
        destdir = self.base_dir / type
        destfile = destdir / (basename + '.json')

        destdir.mkdir(parents=True, exist_ok=True)

        with open(str(destfile), 'w') as fp:
            json.dump(data, fp, indent=2)


class SolrWriter(AbstractWriter):
    def __init__(self, base_url, verbose=False):
        super().__init__(verbose)
        self.base_url = base_url
        self.cores = {
            type: pysolr.Solr('/'.join((self.base_url, type)),
                              always_commit=True)
            for type in ('employees', 'departments')
        }

    def clean(self):
        for core in self.cores.values():
            core.delete(q='*:*')

    def write(self, type, data):
        self.cores[type].add([data])


@click.command(context_settings={
    'help_option_names': ('-h', '--help'),
})
@click.option('-v', '--verbose', is_flag=True)
@click.option('-u', '--url', 'output_url', envvar='SOLR_URL', show_envvar=True)
@click.option(
    '-l',
    '--log-file',
    'logf',
    type=click.File('a'),
    default='-',
    envvar='LOGFILE',
    show_envvar=True,
)
@click.option(
    '-d',
    '--dir',
    'output_dir',
    type=click.Path(dir_okay=True, file_okay=False),
    envvar='OUTPUT_DIR',
    show_envvar=True,
)
@click.option(
    '-j',
    '--jobs',
    metavar='N',
    envvar='IMPORT_JOBS',
    type=int,
    default=multiprocessing.cpu_count(),
    help='',
    show_envvar=True,
    show_default=True,
)
def main(output_dir, output_url, verbose, logf, jobs):  # pragma: no cover
    # Main program.
    if output_url:
        writer = SolrWriter(output_url, verbose=verbose)
    elif output_dir:
        writer = FileWriter(output_dir, verbose=verbose)
    else:
        raise click.UsageError('please specify a destination')

    with contextlib.redirect_stdout(logf), contextlib.redirect_stderr(logf):
        log("Cleaning...")

        writer.clean()

        log("Import begun...")

        try:
            write_phonebook_data(writer, jobs)
        except Exception:
            log("Import failed: " + traceback.format_exc())
            raise

        log("Import complete!")


if __name__ == '__main__':  # pragma: no cover
    main()
