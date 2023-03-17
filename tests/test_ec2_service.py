import boto3
from unittest.mock import patch
import unittest
from moto import mock_ec2
from cli_tool_to_control_ec2.main import EC2Service, EC2Management

session = boto3.Session()
aws_access_key_id = session.get_credentials().access_key
aws_secret_access_key = session.get_credentials().secret_key
aws_region = session.region_name
ec2 = boto3.client('ec2', region_name=aws_region, aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key)
instance_id = 'i-0f587a48713a80472'


class TestEC2Service(unittest.TestCase):
    def test_start_existing_instance(self):
        response = EC2Service(ec2, instance_id).start_existing_instance()
        assert response == f"Instance {instance_id} started with response 200."
        ec2.close()

    def test_stop_instance(self):
        response = EC2Service(ec2, instance_id).stop_instance()
        assert response == f"Instance {instance_id} stopped with response 200."
        ec2.close()

    def test_list_instances(self):
        response = EC2Service(ec2, instance_id).list_instances()
        assert response == "List_instances already downloaded"
        ec2.close()


class TestEC2Management(unittest.TestCase):
    @patch.object(EC2Service, 'start_existing_instance')
    def test_start_existing_instance(self, mock_start):
        management = EC2Management(ec2, instance_id)
        management.start_existing_instance()
        mock_start.assert_called_once()

    @patch.object(EC2Service, 'stop_instance')
    def test_stop_instance(self, mock_stop):
        management = EC2Management(ec2, instance_id)
        management.stop_instance()
        mock_stop.assert_called_once()

    @patch.object(EC2Service, 'list_instances')
    def test_list_instances(self, mock_list):
        management = EC2Management(ec2, instance_id)
        management.list_instances()
        mock_list.assert_called_once()

    def test_start_existing_instance_with_invalid_state(self):
        instance_id = 'i-0123456789abcdef0'
        response = EC2Service(ec2, instance_id).start_existing_instance()
        assert response == f"An error occurred while starting the instance. Error: The instance '{instance_id}' is in a state that is not valid for this operation."
        ec2.close()

    def test_stop_instance_with_invalid_id(self):
        invalid_instance_id = 'invalid_id'
        response = EC2Service(ec2, invalid_instance_id).stop_instance()
        assert response == f"An error occurred while stopping the instance. Error: The instance ID '{invalid_instance_id}' does not exist"
        ec2.close()

    def test_ec2management_with_invalid_id(self):
        invalid_instance_id = 'invalid_id'
        management = EC2Management(ec2, invalid_instance_id)
        response = management.start_existing_instance()
        assert response == f"An error occurred while starting the instance. Error: The instance ID '{invalid_instance_id}' does not exist"
        response = management.stop_instance()
        assert response == f"An error occurred while stopping the instance. Error: The instance ID '{invalid_instance_id}' does not exist"
        response = management.list_instances()
        assert response == f"An error occurred while listing instances. Error: The instance ID '{invalid_instance_id}' does not exist"
        ec2.close()


if __name__ == '__main__':
    unittest.main()
