import redis

from rally.common import cfg
from rally.task import atomic
# from rally.task import scenario
from rally.task import utils
from rally.common import logging
from rally.task import types
from rally.task import validation
from rally_openstack import scenario
from rally_openstack import consts

from rally_openstack.scenarios.cinder import utils as cinder_utils
from rally_openstack.scenarios.neutron import utils as neutron_utils
from rally_openstack.scenarios.nova import utils as nova_utils
from rally_openstack.scenarios.vm import utils as vm_utils
# from rally_openstack.services.storage import block

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


@types.convert(image={"type": "glance_image"},
               flavor={"type": "nova_flavor"})
@validation.add("image_valid_on_flavor", flavor_param="flavor",
                image_param="image")
@validation.add("required_services",
                services=[ consts.Service.NOVA, consts.Service.CINDER])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["cinder", "nova"]},
                    name="ScenarioPlugin.cinder_storage_server_context", platform="openstack")
class NovaCinderTest3(cinder_utils.CinderBasic, vm_utils.VMScenario):


    def run(self, flavor, image,nics,auto_assign_nic, size, blank_volume, boot_server_kwargs, network_create_args=None, subport_count=10, create_volume_params=None):
        boot_server_kwargs = boot_server_kwargs or {}
        if blank_volume:
            create_volume_kwargs = {}
        else:
            create_volume_kwargs = {"imageRef":image}
        boot_server_kwargs["nics"] = nics
        boot_server_kwargs["auto_assign_nic"] = auto_assign_nic

        context = self.context

        iteration   = context['iteration'] - 1
        tenants_amount = len(context['tenants'])
        servers = context["tenant"]["servers"]
        server_index = int((iteration / tenants_amount) % len(servers))
        server = servers[server_index]

        # r = redis.Redis()
        iteration_number  = context['iteration']

        # server = self._boot_server(image, flavor, **boot_server_kwargs)

        server_id = server
        server_obj = self.clients("nova").servers.get(server_id)

        volume = self.cinder.create_volume(size, **create_volume_kwargs)
        volume_id = volume.id


        # r.hset('nova_cinder', iteration_number, uuid_sting)
        print("iteration {}  \n volume uuid {}  \n server uuid {}".format(iteration_number,volume_id,server_id))

        self._attach_volume(server_obj, volume)

        self._detach_volume(server_obj, volume)
        self.cinder.delete_volume(volume)
        # self._delete_server(server)

