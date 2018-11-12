#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import os
import sys
import json

from multiprocessing.dummy import Pool

import mo_api


def get_orgunit_data(uuid):
    """Get the data we need to display for this particular org. func."""
    ou = mo_api.MOOrgUnit(uuid)
    # Parent - UUID if exists, ROOT if not.
    parent = ou.json['parent']['uuid'] if ou.json['parent'] else 'ROOT'
    # For employees, we need job function, name and UUID.
    employees = [
        (
            e['person']['name'], e['person']['uuid'], e['job_function']['name']
        ) for e in ou.engagement
    ]
    # For associateds: Association type, job function, name and UUID.
    associated = [
        (
            a['person']['name'], a['person']['uuid'],
            a['association_type']['name'], a['job_function']['name']
        ) for a in ou.association
    ]
    # For departments, we need name and UUID.
    departments = [(c['name'], c['uuid']) for c in ou.children]
    # For locations, their type and content.
    locations = [
        (a['address_type']['scope'], a['name']) for a in ou.address
    ]
    # For managers, manager type and name and UUID.
    managers = [
        (
            m['manager_type']['name'],
            m['person']['name'] if m['person'] else None,
            m['person']['uuid'] if m['person'] else None
        ) for m in ou.manager
    ]

    return dict(
            uuid=ou.json['uuid'],
            name=ou.json['name'],
            parent=parent,
            locations=locations,
            employees=employees,
            departments=departments,
            associated=associated,
            managers=managers
    )


def get_employee_data(uuid):
    '''Get the data we need to display this employee'''
    employee = mo_api.MOEmployee(uuid)

    # For locations, their type and content.
    locations = [
        (a['address_type']['scope'], a['name']) for a in employee.address
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
            m['manager_type']['name'], m['org_unit']['name'],
            m['org_unit']['uuid']
        ) for m in employee.manager
    ]
    # Associated units - association type, name and UUID of association
    associated_units = [
        (
            a['association_type']['name'], a['org_unit']['name'],
            a['org_unit']['uuid']
         ) for a in employee.association
    ]
    return dict(
        uuid=employee.json['uuid'],
        name=employee.json['name'],
        locations=locations,
        departments=departments,
        managing=managing,
        associated=associated_units)


def write_phonebook_data(orgunit_writer, employee_writer):
    """Write data to store in backend DB.

    The _writer arguments are function to store/index employees and org
    units, respectively.
    """

    ous = mo_api.get_ous()
    employees = mo_api.get_employees()

    def handler(getter, writer):
        def handle_this(uuid):
            data = getter(uuid)
            writer(data)
        return handle_this

    ou_handler = handler(get_orgunit_data, orgunit_writer)
    employee_handler = handler(get_employee_data, employee_writer)

    p = Pool(10)
    # First, org units
    p.map(ou_handler, [ou['uuid'] for ou in ous])
    p.close()
    p.join()

    p = Pool(10)
    # Now, employees
    p.map(employee_handler, [e['uuid'] for e in employees])
    p.close()
    p.join()


def file_writer(directory, field_name='uuid'):

    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'var')
    )
    target_dir = os.path.join(base_dir, directory)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    def writer(data):
        out_file = f"{data[field_name].replace(' ', '')}.json"
        out_file = os.path.join(target_dir, out_file)
        with open(out_file, 'w') as f:
            json.dump(data, f)

    return writer


if __name__ == '__main__':

    orgunit_writer = file_writer('ous')
    employee_writer = file_writer('employees')

    print("Writing data ...")
    try:
        write_phonebook_data(orgunit_writer, employee_writer)
    except Exception as e:
        print(f"Failed to import phonebook data: {str(e)}", file=sys.stderr)
        sys.exit(-1)

    print("done")
