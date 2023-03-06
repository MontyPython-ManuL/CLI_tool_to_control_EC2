import boto3
import click


class EC2Service:
    def __init__(self):
        self.ec2 = boto3.client('ec2')

    def start_instances(self, image_id, instance_type, key_name, security_group, subnet_id, count=1):
        """Start EC2 instances"""
        instances = self.ec2.run_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroupIds=[security_group],
            SubnetId=subnet_id,
            MaxCount=count,
            MinCount=1
        )

        for instance in instances['Instances']:
            print(f"Instance {instance['InstanceId']} started.")

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


class EC2Manager:
    def __init__(self, ec2_service):
        self.ec2_service = ec2_service

    def start_existing_instance(self, instance_id):
        """Start an existing EC2 instance"""
        response = self.ec2_service.ec2.start_instances(
            InstanceIds=[instance_id],
            DryRun=False
        )
        print(f"Instance {instance_id} started with response {response['ResponseMetadata']['HTTPStatusCode']}.")


@click.group()
@click.pass_context
def cli(ctx):
    """Command line interface for EC2 management"""
    ctx.obj = EC2Manager(EC2Service())


@cli.command()
@click.option('--count', default=1, help='Number of instances to start')
@click.option('--image-id', required=True, help='AMI image ID')
@click.option('--instance-type', default='t2.micro', help='Instance type')
@click.option('--key-name', required=True, help='Key pair name')
@click.option('--security-group', required=True, help='Security group ID')
@click.option('--subnet-id', required=True, help='Subnet ID')
@click.pass_obj
def start_instances(ec2_manager, count, image_id, instance_type, key_name, security_group, subnet_id):
    """Start EC2 instances"""
    ec2_manager.ec2_service.start_instances(image_id, instance_type, key_name, security_group, subnet_id, count)


@cli.command()
@click.option('--instance-id', required=True, help='EC2 instance ID')
@click.pass_obj
def start_existing_instance(ec2_manager, instance_id):
    """Start an existing EC2 instance"""
    ec2_manager.start_existing_instance(instance_id)


@cli.command()
@click.option('--instance-id', required=True, help='EC2 instance ID')
@click.pass_obj
def stop_instances(ec2_manager, instance_id):
    """Stop EC2 instances"""
    ec2_manager.ec2_service.stop_instances(instance_id)


@cli.command()
@click.pass_obj
def list_instances(ec2_manager):
    """List all EC2 instances"""
    ec2_manager.ec2_service.list_instances()
