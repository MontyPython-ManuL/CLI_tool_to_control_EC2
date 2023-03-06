import boto3
import click
s3 = boto3.resource('s3')


class Service:
    @click.command()
    @click.option('--count', default=1, help='Number of instances to start')
    @click.option('--image-id', required=True, help='AMI image ID')
    @click.option('--instance-type', default='t2.micro', help='Instance type')
    @click.option('--key-name', required=True, help='Key pair name')
    @click.option('--security-group', required=True, help='Security group ID')
    @click.option('--subnet-id', required=True, help='Subnet ID')
    def start_instances(self, count, image_id, instance_type, key_name, security_group, subnet_id):
        """Start EC2 instances"""
        instances = s3.create_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroupIds=[security_group],
            SubnetId=subnet_id,
            MaxCount=count,
            MinCount=1
        )
        for instance in instances:
            print(f"Instance {instance.id} started.")

    @click.command()
    @click.option('--instance-id', required=True, help='EC2 instance ID')
    def stop_instances(self, instance_id):
        """Stop EC2 instances"""
        instance = s3.Instance(instance_id)
        response = instance.stop()
        print(f"Instance {instance_id} stopped with response {response['ResponseMetadata']['HTTPStatusCode']}.")

    @click.command()
    def list_instances(self):
        """List all EC2 instances"""
        response = s3.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                print(f"Instance ID: {instance['InstanceId']}")
                print(f"Instance state: {instance['State']['Name']}")
                print(f"Instance type: {instance['InstanceType']}")
                print(f"Launch time: {instance['LaunchTime']}")
                print("-------------------------------")
