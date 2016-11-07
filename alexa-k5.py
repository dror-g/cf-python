from keystoneauth1 import loading
from keystoneauth1 import session
from novaclient import client
import logging
import json
import os
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
for server in servers:
	print(server)
	print(nova.servers.list_security_group(server))

