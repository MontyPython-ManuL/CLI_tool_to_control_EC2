import botocore.exceptions
import boto3
import click
import sys


class EC2Service:
    def __init__(self, ec2_client):
        self.ec2 = ec2_client

    def start_multiple_instances(self, instance_config):
        """Start EC2 instances"""
        instances = self.ec2.run_instances(
            ImageId=instance_config['image_id'],
            InstanceType=instance_config['instance_type'],
            KeyName=instance_config['key_name'],
            SecurityGroupIds=[instance_config['security_group_id']],
            SubnetId=instance_config['subnet_id'],
            MaxCount=instance_config['count'],
            MinCount=1
        )

        for instance in instances['Instances']:
            print(f"Instance {instance['InstanceId']} started.")

    def start_running_instance(self, instance_id):
        """Start an existing EC2 instance"""
        response = self.ec2.start_instances(
            InstanceIds=[instance_id],
            DryRun=False
        )
        print(f"Instance {instance_id} started with response {response['ResponseMetadata']['HTTPStatusCode']}.")

    def stop_instances(self, instance_id):
        """Stop EC2 instances"""
        response = self.ec2.stop_instances(InstanceIds=[instance_id])

        print(f"Instance {instance_id} stopped with response {response['ResponseMetadata']['HTTPStatusCode']}.")

    def list_instances(self):
        """List all EC2 instances"""
        response = self.ec2.describe_instances()

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                print(f"Instance ID: {instance['InstanceId']}")
                print(f"Instance state: {instance['State']['Name']}")
                print(f"Instance type: {instance['InstanceType']}")
                print(f"Launch time: {instance['LaunchTime']}")
                print("-------------------------------")


@click.group()
@click.option('--access-key-id', required=True, help='AWS access key ID')
@click.option('--secret-access-key', required=True, help='AWS secret access key')
@click.pass_context
def cli(ctx, access_key_id, secret_access_key):
    """Command line interface for EC2 management"""
    ctx.obj = EC2Service(
        boto3.client('ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    )


@cli.command()
@click.option('--count', default=1, help='Number of instances to start')
@click.option('--image-id', required=True, help='AMI image ID')
@click.option('--instance-type', default='t2.micro', help='Instance type')
@click.option('--key-name', required=True, help='Key pair name')
@click.option('--security-group', required=True, help='Security group ID')
@click.option('--subnet-id', required=True, help='Subnet ID')
@click.pass_obj
def start_instances(self, instance_config):
    try:
        self.ec2_service.start_multiple_instances(instance_config)
    except self.ec2.exceptions.SecurityGroupNotFound as e:
        print(f"Security group not found: {e}")
        sys.exit(1)
    except self.ec2.exceptions.SubnetNotFound as e:
        print(f"Subnet not found: {e}")
        sys.exit(1)
    except self.ec2.exceptions.KeyPairNotFound as e:
        print(f"Key pair not found: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Something went wrong: {e}")
        sys.exit(1)


@cli.command()
@click.option('--instance-id', required=True, help='EC2 instance ID')
@click.pass_obj
def start_existing_instance(self, instance_id):
    """Start an existing EC2 instance"""
    try:
        self.ec2_start.start_existing_instance(instance_id)
    except botocore.exceptions.WaiterError as e:
        print(f"Instance state change failed to complete within the allotted time. Error: {e}")
        sys.exit(1)
    except botocore.exceptions.ParamValidationError as e:
        print(f"Invalid parameters provided for starting the instance. Error: {e}")
        sys.exit(1)
    except botocore.exceptions.EndpointConnectionError as e:
        print(f"Unable to connect to the service endpoint to start the instance. Error: {e}")
        sys.exit(1)
    except botocore.exceptions.ClientError as e:
        print(f"An error occurred while starting the instance. Error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--instance-id', required=True, help='EC2 instance ID')
@click.pass_obj
def stop_instance(self, instance_id):
    """Stop an EC2 instance"""
    try:
        self.ec2_stop.stop_instances(instance_id)
    except botocore.exceptions.WaiterError as e:
        print(f"Instance state change failed to complete within the allotted time. Error: {e}")
        sys.exit(1)
    except botocore.exceptions.ParamValidationError as e:
        print(f"Invalid parameters provided for stopping the instance. Error: {e}")
        sys.exit(1)
    except botocore.exceptions.EndpointConnectionError as e:
        print(f"Unable to connect to the service endpoint to stop the instance. Error: {e}")
        sys.exit(1)
    except botocore.exceptions.ClientError as e:
        print(f"An error occurred while stopping the instance. Error: {e}")
        sys.exit(1)


@cli.command()
@click.pass_obj
def list_instances(self):
    """List all EC2 instances"""
    try:
        self.ec2_list.list_instances()
    except Exception as e:
        print(f"Something wrong Error: {e}")
        sys.exit(1)
