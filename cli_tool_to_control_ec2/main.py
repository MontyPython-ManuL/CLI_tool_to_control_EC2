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

    def start_existing_instance(self, instance_id):
        """Start an existing EC2 instance"""
        response = self.ec2.start_instances(
            InstanceIds=[instance_id],
            DryRun=False
        )
        print(f"Instance {instance_id} started with response {response['ResponseMetadata']['HTTPStatusCode']}.")

    def stop_instance(self, instance_id):
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


@click.group()
@click.option('--profile', '-p', default='default', help="AWS profile to use.")
@click.pass_context
def cli(ctx, profile):
    """AWS EC2 instance management"""
    session = boto3.Session(profile_name=profile)
    ec2_client = session.client('ec2')

    ec2_service = EC2Service(ec2_client)
    ctx.obj = ec2_service


@cli.command()
@click.option('--image-id', '-i', required=True, help="EC2 instance AMI ID")
@click.option('--instance-type', '-t', required=True, help="EC2 instance type")
@click.option('--key-name', '-k', required=True, help="Key pair name")
@click.option('--security-group-id', '-sg', required=True, help="Security group ID")
@click.option('--subnet-id', '-sn', required=True, help="Subnet ID")
@click.option('--count', '-c', default=1, help="Number of instances to start")
@click.pass_context
def start_instances(ctx, image_id, instance_type, key_name, security_group_id, subnet_id, count):
    """Start EC2 instances"""
    instance_config = {
        'image_id': image_id,
        'instance_type': instance_type,
        'key_name': key_name,
        'security_group_id': security_group_id,
        'subnet_id': subnet_id,
        'count': count
    }

    ec2_service = ctx.obj
    ec2_service.start_multiple_instances(instance_config)


@cli.command()
@click.argument('instance-id')
@click.pass_obj
def start_existing_instance(ec2_service, instance_id):
    """Start an existing EC2 instance"""
    response = ec2_service.ec2.start_instances(
        InstanceIds=[instance_id],
        DryRun=False
    )
    print(f"Instance {instance_id} started with response {response['ResponseMetadata']['HTTPStatusCode']}.")


@cli.command()
@click.option('--instance-id', required=True, help='EC2 instance ID')
@click.pass_obj
def stop_instance(self, instance_id):
    """Stop an EC2 instance"""

    try:
        self.ec2_service.stop_instance(instance_id)
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
    else:
        print(f"Instance {instance_id} stopped successfully.")
