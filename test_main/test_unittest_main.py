import unittest
from unittest import mock
import boto3
from moto import mock_ec2
import sys
from cli_tool_to_control_ec2.main import EC2Service, cli


class TestEC2Service(unittest.TestCase):

    def setUp(self):
        self.ec2 = boto3.client('ec2', region_name='us-east-1')

    @mock_ec2
    def test_start_instances(self):
        with mock.patch.object(sys, 'exit') as mock_exit:
            instance_config = {
                'image_id': 'ami-1234abcd',
                'instance_type': 't2.micro',
                'key_name': 'my_key_pair',
                'security_group_id': 'sg-1234abcd',
                'subnet_id': 'subnet-1234abcd',
                'count': 1
            }
            ec2_service = EC2Service(self.ec2)
            ec2_service.start_multiple_instances(instance_config)
            self.assertTrue(mock_exit.called)
            self.assertEqual(mock_exit.call_args[0][0], 1)


if __name__ == '__main__':
    unittest.main()

