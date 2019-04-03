#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
"""Tests for the importer and the API."""

import os
import json

import pytest

from os2mo_tools import mo_api
import do_import

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def my_mo_get(url):
    url_file = '.test_data/mo/' + url.replace('/', '#') + '.json'
    url_file = os.path.join(CURRENT_DIR, url_file)
    with open(url_file, 'r') as f:
        return json.load(f)


def test_mo_data():
    """Test the two classes derived from MOData."""
    employee_uuid = '0014209a-8832-44b3-b7a0-4cc209a71993'
    ou_uuid = '0418617c-242f-4d9a-81cc-abb269ad27b4'

    ou = mo_api.OrgUnit(ou_uuid)
    ou.get = my_mo_get
    e = mo_api.Employee(employee_uuid)
    e.get = my_mo_get

    # Test json function
    assert ou.json['name'] == 'Østervrå børnehus'
    assert e.json['name'] == 'Henry Olesen Steno Ahmad'
    assert str(e) == str(e.json)
    assert str(ou) == str(ou.json)


def test_get_employee_data():
    """Test the get_employee_data function in the do_import module."""
    employee_uuid = '0014209a-8832-44b3-b7a0-4cc209a71993'
    e = mo_api.Employee(employee_uuid)
    e.get = my_mo_get
    e_data = do_import.get_employee_data(e)
    # Normalize to convert tuples to lists - JSON doesn't have tuples.
    e_data = json.loads(json.dumps(e_data))
    data_file = os.path.join(
        CURRENT_DIR, '.test_data/output/' + employee_uuid + '.json'
    )
    with open(data_file, 'r') as f:
        target_e_data = json.load(f)
        assert e_data == target_e_data
        return e_data


def test_get_orgunit_data():
    """Test the get_orgunit_data function in the do_import module."""
    orgunit_uuid = '0f09cea1-58d7-41c9-85cd-692bd84adf38'
    ou = mo_api.OrgUnit(orgunit_uuid)
    ou_data = do_import.get_orgunit_data(ou)
    ou.get = my_mo_get
    # Normalize to convert tuples to lists - JSON doesn't have tuples.
    ou_data = json.loads(json.dumps(ou_data))
    data_file = os.path.join(
        CURRENT_DIR, '.test_data/output/' + orgunit_uuid + '.json'
    )
    with open(data_file, 'r') as f:
        target_ou_data = json.load(f)
        assert ou_data == target_ou_data
        return ou_data


def test_file_writer():
    writer = do_import.FileWriter(CURRENT_DIR + '/test')
    writer.clean()
    writer.write_employee({'test': 'Hej', 'uuid': '42'})
    writer.write_unit({'test': 'Hej', 'uuid': '42'})
    writer.clean()
    assert True


def test_nosuchattribute():
    orgunit_uuid = '0418617c-242f-4d9a-81cc-abb269ad27b4'
    ou = mo_api.OrgUnit(orgunit_uuid)
    ou.get = my_mo_get
    with pytest.raises(AttributeError):
        print(ou.nosuchattribute)
