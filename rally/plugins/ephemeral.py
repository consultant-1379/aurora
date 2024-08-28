import json
import os
import pkgutil
import time
import redis
from rally.common import logging
from rally.common import sshutils
from rally.common import validation
from rally import exceptions
from rally.plugins.common import validators
from rally.task import atomic
from rally.task import types

from rally_openstack import consts
from rally_openstack import scenario
from rally_openstack.scenarios.cinder import utils as cinder_utils
from rally_openstack.scenarios.vm import utils as vm_utils
from rally_openstack.scenarios.nova import utils as nova_utils
from rally_openstack.services import heat

@types.convert(image={"type": "glance_image"},
               flavor={"type": "nova_flavor"})
@validation.add("image_valid_on_flavor", flavor_param="flavor",
                image_param="image")
@validation.add("required_services", services=[consts.Service.NOVA])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["nova"]},
                    name="ScenarioPlugin.Ephemeral_Storage",
                    platform="openstack")
class Ephemeral_Storage(nova_utils.NovaScenario):

    def run(self, image, flavor,nics, auto_assign_nic, **kwargs):

        """Boot a server from flavor with ephemeral storage.

        Assumes that cleanup is done elsewhere.

        :param image: image to be used to boot an instance
        :param flavor: flavor to be used to boot an instance
        :param auto_assign_nic: True if NICs should be assigned
        :param kwargs: Optional additional arguments for server creation
        """
        kwargs["nics"] = nics

        iteration_number = self.context['iteration']
        server = self._boot_server(image, flavor,
                          auto_assign_nic=auto_assign_nic, **kwargs)

        server_id = server.id

        # r = redis.Redis()
        # r.hset(['nova_ephemeral'], iteration_number, server_id)

        print("iteration {}  \n server uuid {}".format(iteration_number,server_id))

        self._delete_server(server)

