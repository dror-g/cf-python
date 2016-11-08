from keystoneauth1 import loading
from keystoneauth1 import session
from novaclient import client
from cinderclient import client as cici
import logging
import json
import os
import time
logging.basicConfig()


with open("credentials.json") as data_file:
        options = json.load(data_file)


loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(auth_url=options["AUTH_URL"],
                                username=options["USERNAME"],
                                password=options["PASSWORD"],
                                user_domain_name=options["DOMAIN_NAME"],
                                project_id=options["PROJECT_ID"])
sess = session.Session(auth=auth)
nova = client.Client(options["VERSION"], session=sess)

servers = nova.servers.list()

print("\nAlexa, ask k5 how many servers have I got?")
print("you have %s servers.\n" % len(servers))

print("Alexa, ask k5 to start X servers")
print("Starting X servers")
newserv_num = 1

flavors = nova.flavors.list()
images = nova.images.list()
net_id = "2d051b82-cf4c-491f-a7aa-0b74800b6fd0"
nics = [{"net-id": net_id, "v4-fixed-ip": ''}]

cinder = cici.Client(options["VERSION"], session=sess)
volume = cinder.volumes.create(40)
#print(volume.id)

#blockmap = {"volume_size": "80", "volume_id": {get_resource: sys-vol_server1}, "delete_on_termination": True, "device_name": "/dev/vda"}

status = volume.status
while ( status == 'creating' or status == 'downloading'):
    time.sleep(5)
    print "status: %s" % status
    volume = cinder.volumes.get(volume.id)
    status = volume.status
print "status: %s" % status

blockmap = {'vda': volume.id}

for newserv in range(newserv_num):
	nova.servers.create("test"+str(newserv), "ffa17298-537d-40b2-a848-0a4d22b49df5", flavors[0], nics=nics, block_device_mapping=blockmap) 

#for server in servers:
#	print(server)
#	print(nova.servers.list_security_group(server))

