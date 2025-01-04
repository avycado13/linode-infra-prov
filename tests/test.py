import unittest
from unittest.mock import MagicMock, patch

from src.linode_infra_prov.infra import CreatedLinode, DesiredLinode, create_linode


class TestDesiredLinode(unittest.TestCase):
    def setUp(self):
        self.desired_linode = DesiredLinode("test", "us-east", "ubuntu")

    def test_init(self):
        self.assertEqual(self.desired_linode.name, "test")
        self.assertEqual(self.desired_linode.region, "us-east")
        self.assertEqual(self.desired_linode.image, "ubuntu")


class TestCreatedLinode(unittest.TestCase):
    def setUp(self):
        self.desired_linode = DesiredLinode("test", "us-east", "ubuntu")
        self.created_linode = CreatedLinode(self.desired_linode, "192.168.1.1", "10.0.0.1")

    def test_init(self):
        self.assertEqual(self.created_linode.name, "test")
        self.assertEqual(self.created_linode.region, "us-east")
        self.assertEqual(self.created_linode.image, "ubuntu")
        self.assertEqual(self.created_linode.public_ip, "192.168.1.1")
        self.assertEqual(self.created_linode.private_ip, "10.0.0.1")


class TestCreateLinode(unittest.TestCase):
    @patch("your_module.LinodeClient")
    def test_create_linode(self, mock_client):
        mock_instance = MagicMock()
        mock_instance.ips.ipv4.public = [MagicMock(address="192.168.1.1")]
        mock_instance.ips.ipv4.private = [MagicMock(address="10.0.0.1")]
        mock_client.return_value.linode.instance_create.return_value = (mock_instance, "password")

        desired_linode = DesiredLinode("test", "us-east", "ubuntu")
        created_linode = create_linode(desired_linode)

        self.assertEqual(created_linode.name, "test")
        self.assertEqual(created_linode.region, "us-east")
        self.assertEqual(created_linode.image, "ubuntu")
        self.assertEqual(created_linode.public_ip, "192.168.1.1")
        self.assertEqual(created_linode.private_ip, "10.0.0.1")


if __name__ == "__main__":
    unittest.main()
