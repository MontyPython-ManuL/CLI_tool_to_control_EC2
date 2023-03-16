import botocore.exceptions
import boto3
import click
import sys
import logging


class EC2Service:
    def __init__(self, ec2, instance_id):
        self.ec2 = ec2
        self.instance_id = instance_id

    def start_existing_instance(self):
        """Start an existing EC2 instance"""
        response = self.ec2.start_instances(
            InstanceIds=[self.instance_id],
            DryRun=False
        )
        click.echo(f"Instance {self.instance_id} started with response {response['ResponseMetadata']['HTTPStatusCode']}.")

    def stop_instance(self):
        """Stop EC2 instances"""
        response = self.ec2.stop_instances(InstanceIds=[self.instance_id])

        click.echo(f"Instance {self.instance_id} stopped with response {response['ResponseMetadata']['HTTPStatusCode']}.")

    def list_instances(self):
        """List all EC2 instances"""
        response = self.ec2.describe_instances()

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                print(f"Instance ID: {instance['InstanceId']}")
                print(f"Instance state: {instance['State']['Name']}")


def start_existing_instance(ec2, instance_id):
    """Start an existing EC2 instance"""
    EC2Service(ec2, instance_id).start_existing_instance()


def stop_instance(ec2, instance_id):
    try:
        EC2Service(ec2, instance_id).stop_instance()
        click.echo('EC2 instance has been successfully stopped.')
    except botocore.exceptions.WaiterError as e:
        logging.error(f"Instance state change failed to complete within the allotted time. Error: {e}")
        sys.exit(1)
    except botocore.exceptions.ParamValidationError as e:
        logging.error(f"Invalid parameters provided for stopping the instance. Error: {e}")
        sys.exit(1)
    except botocore.exceptions.EndpointConnectionError as e:
        logging.error(f"Unable to connect to the service endpoint to stop the instance. Error: {e}")
        sys.exit(1)
    except botocore.exceptions.ClientError as e:
        logging.error(f"An error occurred while stopping the instance. Error: {e}")
        sys.exit(1)


def list_instances(ec2, instance_id):
    """List all EC2 instances"""
    EC2Service(ec2, instance_id).list_instances()
    click.echo('Instance list:')


@click.command()
@click.option('--instance_id', prompt='input instance-id', required=True, help='EC2 instance ID')
@click.option('--action', prompt='choose action [STOP, START, LIST]', required=True, help='EC2 instance ID')
def auth(instance_id, action):
    session = boto3.Session()
    aws_access_key_id = session.get_credentials().access_key
    aws_secret_access_key = session.get_credentials().secret_key
    aws_region = session.region_name

    ec2 = boto3.client('ec2', region_name=aws_region, aws_access_key_id=aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key)
    if action == 'STOP':
        stop_instance(ec2, instance_id)
    elif action == 'START':
        start_existing_instance(ec2, instance_id)
    elif action == 'LIST':
        list_instances(ec2, instance_id)


if __name__ == '__main__':
    auth()
