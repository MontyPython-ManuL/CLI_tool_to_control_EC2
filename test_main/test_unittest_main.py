import boto3
from click.testing import CliRunner
from unittest.mock import patch, Mock
from cli_tool_to_control_ec2.main import EC2Service, EC2Management, manage_ec2_instance


class TestEC2Service:
    def test_start_existing_instance(self):
        ec2 = Mock()
        instance_id = 'i-0123456789abcdef'
        service = EC2Service(ec2, instance_id)
        response = service.start_existing_instance()
        assert response == f"Instance {instance_id} started with response 200."

    def test_stop_instance(self):
        ec2 = Mock()
        instance_id = 'i-0123456789abcdef'
        service = EC2Service(ec2, instance_id)
        response = service.stop_instance()
        assert response == f"Instance {instance_id} stopped with response 200."


class TestEC2Management:
    @patch.object(EC2Service, 'start_existing_instance')
    def test_start_existing_instance(self, mock_start):
        ec2 = Mock()
        instance_id = 'i-0123456789abcdef'
        management = EC2Management(ec2, instance_id)
        management.start_existing_instance()
        mock_start.assert_called_once()

    @patch.object(EC2Service, 'stop_instance')
    def test_stop_instance(self, mock_stop):
        ec2 = Mock()
        instance_id = 'i-0123456789abcdef'
        management = EC2Management(ec2, instance_id)
        management.stop_instance()
        mock_stop.assert_called_once()

    @patch.object(EC2Service, 'list_instances')
    def test_list_instances(self, mock_list):
        ec2 = Mock()
        instance_id = 'i-0123456789abcdef'
        management = EC2Management(ec2, instance_id)
        management.list_instances()
        mock_list.assert_called_once()


class TestCLI:
    def test_manage_ec2_instance_start(self):
        runner = CliRunner()
        with patch.object(boto3, 'client') as mock_client:
            instance_id = 'i-0123456789abcdef'
            action = 'START'
            ec2 = Mock()
            management = EC2Management(ec2, instance_id)
            result = runner.invoke(management.start_existing_instance(), [action])
            assert result.exit_code == 0
            mock_client.assert_called_once_with('ec2', region_name=None, aws_access_key_id=None,
                                                aws_secret_access_key=None)

    def test_manage_ec2_instance_stop(self):
        runner = CliRunner()
        with patch.object(boto3, 'client') as mock_client:
            instance_id = 'i-0123456789abcdef'
            action = 'STOP'
            ec2 = Mock()
            management = EC2Management(ec2, instance_id)
            result = runner.invoke(management.stop_instance(), [action])
            assert result.exit_code == 0
            mock_client.assert_called_once_with('ec2', region_name=None, aws_access_key_id=None,
                                                aws_secret_access_key=None)
