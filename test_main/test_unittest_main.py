import unittest
from click.testing import CliRunner
from cli_tool_to_control_ec2.main import EC2Service


class TestEC2CLI(unittest.TestCase):

    def setUp(self):
        self.ec2_manager = EC2Manager()
        self.ec2_cli = EC2CLI(ec2_manager=self.ec2_manager)
        self.runner = CliRunner()

    def test_start_existing_instance(self):
        result = self.runner.invoke(self.ec2_cli.cli,
                                    ['start-existing-instance', '--instance-id', 'i-1234567890abcdefg'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Instance state change failed to complete within the allotted time', result.output)

    def test_stop_instance(self):
        result = self.runner.invoke(self.ec2_cli.cli, ['stop-instance', '--instance-id', 'i-1234567890abcdefg'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Something wrong', result.output)

    def test_list_instances(self):
        result = self.runner.invoke(self.ec2_cli.cli, ['list-instances'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('No instances found', result.output)


if __name__ == '__main__':
    unittest.main()