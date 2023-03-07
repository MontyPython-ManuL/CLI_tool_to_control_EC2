import boto3
import click
import sys


class EC2Service:
    def __init__(self, ec2_client):
        self.ec2 = ec2_client

    def start_instances(self, instance_config):
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

    def start_existing_instance(self, instance_id):
        """Start an existing EC2 instance"""
        response = self.ec2.describe_instances(
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


class EC2Client:
    def __init__(self, access_key_id, secret_access_key):
        try:
            self.ec2 = boto3.client(
                'ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
            self.ec2_service = EC2Service(self.ec2)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    @click.group()
    @click.pass_context
    def cli(ctx):
        """Command line interface for EC2 management"""
        ctx.obj = EC2Client(access_key_id='<your_aws_access_key_id>', secret_access_key='<your_aws_secret_access_key>')

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
            self.ec2_service.start_instances(instance_config)
        except Exception as e:
            print(f"Something is wrong with the input parameters.: {e}")
            sys.exit(1)

    @cli.command()
    @click.option('--instance-id', required=True, help='EC2 instance ID')
    @click.pass_obj
    def start_existing_instance(self, instance_id):
        """Start an existing EC2 instance"""
        try:
            self.ec2_service.start_existing_instance(instance_id)
        except Exception as e:
            print(f"Something wrong Error: {e}")
            sys.exit(1)

    @cli.command()
    @click.option('--instance-id', required=True, help='EC2 instance ID')
    @click.pass_obj
    def stop_instance(self, instance_id):
        """Stop an EC2 instance"""
        try:
            self.ec2_service.stop_instances(instance_id)
        except Exception as e:
            print(f"Something wrong Error: {e}")
            sys.exit(1)

    @cli.command()
    @click.pass_obj
    def list_instances(self):
        """List all EC2 instances"""
        try:
            self.ec2_service.list_instances()
        except Exception as e:
            print(f"Something wrong Error: {e}")
            sys.exit(1)
