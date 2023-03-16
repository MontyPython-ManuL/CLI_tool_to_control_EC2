# EC2 Control CLI Tool

This is a command-line interface tool built in Python to control Amazon Elastic Compute Cloud (EC2) instances. It provides various commands to start, stop, and list EC2 instances. It uses the boto3 library to interact with the AWS API.## Installation
### Getting Started:
1. Clone this repository using the following command:
```bash
git clone https://github.com/MontyPython-ManuL/CLI_tool_to_control_EC2.git
```

2. Navigate to the project directory:
```bash
cd CLI_tool_to_control_EC2
```
3. Configure the AWS credentials using aws configure or by setting the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.:
4. Run the tool using the following command
```
python ec2_control.py [OPTIONS] COMMAND [ARGS]...
```
## Commands

#### This tool provides the following commands:
### `start-instance`

Starts an EC2 instance.
```
python ec2_control.py start-instance --instance-id INSTANCE_ID
```
Options:
* `--instance-id`: Required. The ID of the instance to start.
### `stop-instance`

Stops an EC2 instance.
```
python ec2_control.py stop-instance --instance-id INSTANCE_ID
```
Options:
* `--instance-id`: Required. The ID of the instance to stop.

### `list-instances`

Lists all EC2 instances.
```
python ec2_control.py list-instances
```

## Examples
1. Start an EC2 instance:
```
python ec2_control.py start-instance --instance-id i-0123456789abcdef0
```
2. Stop an EC2 instance:
```
python cli_tool_to_control_ec2/main.py stop_instance --instance-id * --region_name * --aws_access_key_id * 
--aws_secret_access_key *
```
3. List all EC2 instances:
```
python ec2_control.py list-instances
```
### Contributing
Contributions are welcome! Please open an issue or submit a pull request.

#### Author 

Носаченко Олег – MontyPython-ManuL