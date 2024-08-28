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
                    name="ScenarioPlugin.cinder_storage_four", platform="openstack")
class NovaCinderTest2(cinder_utils.CinderBasic, vm_utils.VMScenario):


    def run(self, flavor, image,nics,auto_assign_nic, size, boot_server_kwargs, network_create_args=None, subport_count=10, create_volume_params=None):
        boot_server_kwargs = boot_server_kwargs or {}
        create_volume_kwargs = {}
        boot_server_kwargs["nics"] = nics
        boot_server_kwargs["auto_assign_nic"] = auto_assign_nic



        # r = redis.Redis()
        iteration_number  = self.context['iteration']

        server = self._boot_server(image, flavor, **boot_server_kwargs)

        server_id = server.id

        volume = self.cinder.create_volume(size, **create_volume_kwargs)
        volume_id = volume.id


        # r.hset('nova_cinder', iteration_number, uuid_sting)
        print("iteration {}  \n volume uuid {}  \n server uuid {}".format(iteration_number,volume_id,server_id))

        self._attach_volume(server, volume)

        self._detach_volume(server, volume)
        self.cinder.delete_volume(volume)
        self._delete_server(server)

