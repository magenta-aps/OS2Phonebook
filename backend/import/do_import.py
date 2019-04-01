# https://magenta.dk
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
"""Import org units and employees from MO."""

import os
import sys
import json
import datetime
import traceback

from multiprocessing.dummy import Pool

from os2mo_tools import mo_api

SECRET = 'Hemmelig'

IMPORT_LOG_FILE = os.environ.get('IMPORT_LOG_FILE', 'logfile.txt')


def is_visible(a):
    """Decide if address is visible or protected (secret)."""
    # TODO: Change when backend starts using scope to indicate visibility.
    return not ('visibility' in a and a['visibility']['user_key'] == SECRET)


def get_root(ou):
    """Get root of current org unit."""
    parent = ou.json['parent']
    if not parent:
        return ou
    else:
        parent = mo_api.OrgUnit(parent['uuid'])
        return get_root(parent)


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
    root = get_root(ou)

    orgunit_data = dict(
        uuid=ou.json['uuid'],
        name=ou.json['name'],
        root_uuid=root.json['uuid'],
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


def write_phonebook_data(orgunit_writer, employee_writer):
    """Write data to store in backend DB.

    The ``_writer`` arguments are functions to store/index employees and org
    units, respectively.
    """
    ous = mo_api.get_ous()
    employees = mo_api.get_employees()

    def handler(getter, writer):
        def handle_this(obj):
            data = getter(obj)
            writer(data)
        return handle_this

    ou_handler = handler(get_orgunit_data, orgunit_writer)
    employee_handler = handler(get_employee_data, employee_writer)

    p = Pool(10)
    # First, org units
    p.map(ou_handler, (mo_api.OrgUnit(ou['uuid']) for ou in ous))
    p.close()
    p.join()

    p = Pool(10)
    # Now, employees
    p.map(employee_handler, (mo_api.Employee(e['uuid']) for e in employees))
    p.close()
    p.join()


def file_writer(directory, field_name='uuid'):
    """Return a function that writes data to a given directory.

    The data must be JSON and is  stored in a file name taken from the
    data's field as indicated by the ``field_name`` parameter."""

    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'var')
    )
    target_dir = os.path.join(base_dir, directory)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    def writer(data):
        out_file = "{}.json".format(data[field_name].replace(' ', ''))
        out_file = os.path.join(target_dir, out_file)
        with open(out_file, 'w') as f:
            json.dump(data, f)

    return writer


def main():  # pragma: no cover
    # Main program.
    orgunit_writer = file_writer('ous')
    employee_writer = file_writer('employees')

    print("Writing data ...")
    try:
        write_phonebook_data(orgunit_writer, employee_writer)
    except Exception as e:
        with open(IMPORT_LOG_FILE, 'a') as log_file:
            tb = traceback.format_exc()
            now = datetime.datetime.now()
            print(
                "{} - Failed to import phonebook data: {}".format(now, str(e)),
                file=log_file
            )
            print('STACK TRACE:\n {}'.format(tb), file=log_file)
        sys.exit(-1)


if __name__ == '__main__':  # pragma: no cover
    main()
    print("done")
