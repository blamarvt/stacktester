

from stacktester import openstack

import json
import unittest
from subprocess import call

FIXTURES = [
    {"flavorid": 1, "name": "m1.tiny", "ram": 512, "vcpus": 1, "disk": 0},
    {"flavorid": 2, "name": "m1.small", "ram": 2048, "vcpus": 1, "disk": 20},
    {"flavorid": 3, "name": "m1.medium", "ram": 4096, "vcpus": 2, "disk": 40},
    {"flavorid": 4, "name": "m1.large", "ram": 8192, "vcpus": 4, "disk": 80},
    {"flavorid": 5, "name": "m1.xlarge", "ram": 16384, "vcpus": 8, "disk": 160},
] 


class FlavorsTest(unittest.TestCase):

    def setUp(self):
        self.os = openstack.Manager()
        self.flavors = {}
        for FIXTURE in FIXTURES:
            self.flavors[FIXTURE["name"]] = FIXTURE
            self._add_flavor(FIXTURE)

    def tearDown(self):
       for FIXTURE in FIXTURES:
           self._delete_flavor(FIXTURE["name"])

    def _add_flavor(self, flavor):
        #TODO: Get connection info from config
        call(["ssh", "root@nova1", "nova-manage instance_type create", 
                        str(flavor["name"]),
                        str(flavor["ram"]),
                        str(flavor["vcpus"]),
                        str(flavor["disk"]),
                        str(flavor["flavorid"]),
        ]) 

    def _delete_flavor(self, flavor_name):
        #TODO: Get connection info from config
        call(["ssh", "root@nova1", "nova-manage instance_type delete ",
                    flavor_name,
                    "--purge",
            ]) 

    def test_get_flavor_details(self):
        """
        Verify the expected details are returned for a flavor
        """
        self.assertEqual(len(self.flavors.items()), len(FIXTURES))
        for (flavor_name, expected) in self.flavors.items():
            url = '/flavors/%s' % (expected['flavorid'])
            response, body = self.os.nova_api.request('GET', url)
            self.assertEqual(response['status'], '200')
            actual = json.loads(body)['flavor']
            self.assertEqual(expected['name'], actual['name'])
            self.assertEqual(expected['ram'], actual['ram'])
            self.assertEqual(expected['disk'], actual['disk'])

    def test_get_flavors(self):
        """
        Verify the expected flavors are returned
        """

        url = '/flavors'
        response, body = self.os.nova_api.request('GET', url)
        self.assertEqual(response['status'], '200')
        actuals = json.loads(body)['flavors']

        for actual in actuals:
            print actual
            
            expected= self.flavors[actual['name']]

            self.assertEqual(response['status'], '200')
            self.assertEqual(expected['name'], actual['name'])

    def test_get_flavors_detail(self):
        """
        Verify the expected flavors are returned
        """

        url = '/flavors/detail'
        response, body = self.os.nova_api.request('GET', url)
        self.assertEqual(response['status'], '200')
        actuals = json.loads(body)['flavors']

        for actual in actuals:
            print actual
            
            expected= self.flavors[actual['name']]

            self.assertEqual(response['status'], '200')
            self.assertEqual(expected['name'], actual['name'])
            self.assertEqual(expected['disk'], actual['disk'])
            self.assertEqual(expected['ram'], actual['ram'])
