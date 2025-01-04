#!/bin/python3

import os
from os.path import dirname, join
from typing import Union

from dotenv import load_dotenv
from hcloud import Client as HetznerClient
from hcloud.images import Image
from hcloud.server_types import ServerType
from linode_api4 import LinodeClient

"""
Set current working directory to repository root.
"""
os.chdir(join(dirname(__file__), ".."))


"""
Load linode and hetzner API key from dotenv file
"""

load_dotenv(".env")
LINODE_API_KEY = os.environ.get("LINODE_API_KEY")
HETZNER_API_KEY = os.environ.get("HETZNER_API_KEY")

"""
Instantiate linode and hetzner API client with key
"""
linode_client = LinodeClient(LINODE_API_KEY)
hetzner_client = HetznerClient(token = HETZNER_API_KEY)
"""
Print available linode types, regions, and images
"""
# ltypes = client.linode.types()
# regions = client.regions()
# images = client.images()
# for ltype in ltypes:
#     print(ltype)
# for region in regions:
#     print(region)
# for image in images:
#     print(image)


class DesiredLinode:
    def __init__(self, name: str, region: str, image: str, size: str):
        self.name = name
        self.region = region
        self.image = image
        self.size = size

class DesiredHetzner:
    def __init__(self, name: str, image: Image, size: ServerType):
        self.name = name
        self.image = image
        self.size = size

class CreatedLinode:
    def __init__(self, desired_linode: DesiredLinode, public_ip: str, private_ip: str):
        self.name = desired_linode.name
        self.region = desired_linode.region
        self.image = desired_linode.image
        self.public_ip = public_ip
        self.private_ip = private_ip


def create_linode(desired_linode: DesiredLinode) -> Union[CreatedLinode, Exception]:
    """
    Create new linodes. This fails if linodes with these names already exist.
    """
    try:
        new_linode, _password = linode_client.linode.instance_create(
            "g6-nanode-1",
            desired_linode.region,
            private_ip=True,
            label=desired_linode.name,
            image=desired_linode.image,
            authorized_keys="~/.ssh/id_ed25519.pub",
        )

        public_ip = new_linode.ips.ipv4.public[0].address
        private_ip = new_linode.ips.ipv4.private[0].address

        return CreatedLinode(desired_linode, public_ip, private_ip)
    except Exception as e:
        return e
