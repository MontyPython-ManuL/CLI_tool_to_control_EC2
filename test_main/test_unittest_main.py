import io
from unittest import mock
import unittest.mock
from botocore.exceptions import WaiterError, ParamValidationError, EndpointConnectionError
from cli_tool_to_control_ec2.main import EC2Service


class TestEC2Service(unittest.TestCase):

    @mock.patch('boto3.Session')
    def setUp(self, mock_session):
        self.mock_ec2_client = mock.MagicMock()
        mock_session.return_value.client.return_value = self.mock_ec2_client
        self.ec2_service = EC2Service(self.mock_ec2_client)

    def test_start_multiple_instances(self):
        instance_config = {
            'image_id': 'ami-123456',
            'instance_type': 't2.micro',
            'key_name': 'test_key',
            'security_group_id': 'sg-123456',
            'subnet_id': 'subnet-123456',
            'count': 3
        }

        self.mock_ec2_client.run_instances.return_value = {'Instances': [{'InstanceId': 'i-123456'},
                                                                         {'InstanceId': 'i-789012'},
                                                                         {'InstanceId': 'i-345678'}]}

        with mock.patch('builtins.print') as mock_print:
            self.ec2_service.start_multiple_instances(instance_config)
            mock_print.assert_any_call("Instance i-123456 started.")
            mock_print.assert_any_call("Instance i-789012 started.")
            mock_print.assert_any_call("Instance i-345678 started.")

        self.mock_ec2_client.run_instances.assert_called_once_with(
            ImageId=instance_config['image_id'],
            InstanceType=instance_config['instance_type'],
            KeyName=instance_config['key_name'],
            SecurityGroupIds=[instance_config['security_group_id']],
            SubnetId=instance_config['subnet_id'],
            MaxCount=instance_config['count'],
            MinCount=1
        )

    def test_start_existing_instance(self):
        instance_id = 'i-123456'

        self.mock_ec2_client.start_instances.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}

        with mock.patch('builtins.print') as mock_print:
            self.ec2_service.start_existing_instance(instance_id)
            mock_print.assert_called_once_with(f"Instance {instance_id} started with response 200.")

        self.mock_ec2_client.start_instances.assert_called_once_with(
            InstanceIds=[instance_id],
            DryRun=False
        )

    def test_stop_instance(self):
        instance_id = 'i-123456'

        self.mock_ec2_client.stop_instances.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}

        with mock.patch('builtins.print') as mock_print:
            self.ec2_service.stop_instance(instance_id)
            mock_print.assert_called_once_with(f"Instance {instance_id} stopped with response 200.")

        self.mock_ec2_client.stop_instances.assert_called_once_with(InstanceIds=[instance_id])

        # test WaiterError exception handling
        self.mock_ec2_client.stop_instances.side_effect = WaiterError('StopInstance', 'WaiterError', last_response={})
        with self.assertRaises(SystemExit):
            self.ec2_service.stop_instance(instance_id)

        # test ParamValidationError exception handling
        self.mock_ec2_client.stop_instances.side_effect = ParamValidationError(report='InvalidParameter')
        with self.assertRaises(SystemExit):
            self.ec2_service.stop_instance(instance_id)

        # test EndpointConnectionError exception handling
        self.mock_ec2_client.stop_instances.side_effect = EndpointConnectionError(endpoint_url='http://localhost:8000',
                                                                                  error_message='ConnectionError')
        with self.assertRaises(SystemExit):
            self.ec2_service.stop_instance(instance_id)

    def test_list_instances(self):
        instance_id = 'i-0a1234567890abcde'
        instance_state = {'Name': 'running'}
        instance = {'InstanceId': instance_id, 'State': instance_state}
        reservation = {'Instances': [instance]}
        response = {'Reservations': [reservation]}

        self.mock_ec2_client.describe_instances.return_value = response

        expected_output = f"Instance ID: {instance_id}\nInstance state: {instance_state['Name']}\n"

        with unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_output:
            self.ec2_service.list_instances()

        self.assertEqual(fake_output.getvalue(), expected_output)
        self.mock_ec2_client.describe_instances.assert_called_once()