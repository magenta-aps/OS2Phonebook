from collections import defaultdict
import pprint

import requests

from cached_property import cached_property


def mo_get(url):
    result = requests.get(url)
    if not result:
        result.raise_for_status()
    else:
        return result.json()


DEFAULT_MO_URL = 'http://morademo.atlas.magenta.dk/service'



class MOData:

    @cached_property
    def json(self):
        return mo_get(self.url)

    @cached_property
    def children(self):
        return mo_get(self.url + '/children')

    @cached_property
    def _details(self):
        return mo_get(self.url + '/details/')

    @cached_property
    def detail_fields(self):
        return list(self._details.keys())

    def _get_detail(self, detail):
        return mo_get(self.url + '/details/' + detail)

    def __getattr__(self, name):
        """Get details if field in details for object.

         Available details for OrgFunc are: address, association,
         engagement, it, leave, manager, org_unit, role
         """
        if name in self._details:
            if name not in self._stored_details and self._details[name]:
                self._stored_details[name] = self._get_detail(name)
            return self._stored_details[name]
        else:
            return object.__getattribute__(self, name)

    def __str__(self):
        return str(self.json)

class MOOrgUnit(MOData):

    def __init__(self, uuid, mo_url=DEFAULT_MO_URL):
        self.uuid = uuid
        self._stored_details = defaultdict(list)
        self.url = mo_url + '/ou/' + self.uuid


class MOEmployee(MOData):

    def __init__(self, uuid, mo_url=DEFAULT_MO_URL):
        self.uuid = uuid
        self._stored_details = defaultdict(list)
        self.url = mo_url + '/e/' + self.uuid


def get_orgunit_data(uuid):
    '''Get the data we need to display for this particular org. func.'''
    ou = MOOrgUnit(uuid)
    # For employees, we need job function, name and UUID.
    employees = [
        (
            e['person']['name'], e['person']['uuid'], e['job_function']['name']
        ) for e in ou.engagement
    ]
    # For associates: Association type, job function, name and UUID.
    associates = [
        (
            a['person']['name'], a['person']['uuid'],
            a['association_type']['name'], a['job_function']['name']
        ) for a in ou.association
    ]
    # For departments, we need name and UUID.
    departments = [(c['name'], c['uuid']) for c in ou.children]
    # For locations, their type and content.
    locations = [
        (a['address_type']['name'], a['name']) for a in ou.address
    ]
    # For managers, manager type and name and UUID.
    managers = [
        (
            m['manager_type']['name'], m['person']['name'], m['uuid']
        ) for m in ou.manager
    ]

    return dict(
            name=ou.json['name'],
            parent=ou.json['parent'],
            locations=locations,
            employees=employees,
            departments = departments,
            associates=associates,
            managers=managers
    )


def get_employee_data(uuid):
    '''Get the data we need to display this employee'''
    employee = MOEmployee(uuid)

    # For locations, their type and content.
    locations = [
        (a['address_type']['name'], a['name']) for a in employee.address
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
        name=employee.json['name'],
        locations=locations,
        departments=departments,
        managing=managing,
        associated_units=associated_units)



def get_org_units(root_id):
    "Get all org units by traversing the tree."
    my_ou = mo_get(mo_url + '/ou/' + root_id)
    my_children = mo_get(mo_url + '/ou/' + root_id + '/children')
    org_units = [my_ou]
    for c in my_children:
        org_units += get_org_units(c['uuid'])
    return org_units


def get_ous(org_id):
    return mo_get(mo_url + '/o/' + org_id + '/ou/')['items']


def get_employees(org_id):
    return mo_get(mo_url + '/o/' + org_id + '/e/')['items']


def get_organisation(mo_url):
    org_root = mo_get(mo_url + '/o/')
    [org_root] = org_root
    org_info = mo_get(mo_url + '/o/' + org_root['uuid'])
    org_children = mo_get(mo_url + '/o/' + org_root['uuid'] + '/children')
    [root_org_unit] = org_children  # Assume there's only one!

    # This is, finally, the root OU of our organization
    root_id = root_org_unit['uuid']
    org_units = get_org_units(root_id)

    return org_units


ORG_ROOT = mo_get(DEFAULT_MO_URL + '/o/')[0]['uuid']
ROOT_ORG_UNIT = mo_get(DEFAULT_MO_URL + '/o/' + ORG_ROOT + '/children')[0]['uuid']
# ORG_ROOT = '3a87187c-f25a-40a1-8d42-312b2e2b43bd'
# ROOT_ORG_UNIT = '9f42976b-93be-4e0b-9a25-0dcb8af2f6b4'

if __name__ == '__main__':

    print(ROOT_ORG_UNIT)
    # data = get_orgunit_data(ROOT_ORG_UNIT)
    data = get_employee_data('a7b5c37b-3b5b-4110-a8d7-1d6f36861be4')
    pprint.pprint(data)
