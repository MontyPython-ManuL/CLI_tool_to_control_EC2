# EC2 CLI Tool

EC2 CLI Tool is a command-line tool that allows you to manage Amazon EC2 instances through a command-line interface. This tool provides the ability to launch, stop, and list EC2 instances.
## Installation
#### Before using EC2 CLI Tool, you need to install the following dependencies:

* boto3
* click
* botocore

## Usage

#### EC2 CLI Tool consists of the following commands:

* `start-instances`: launches new EC2 instances
* `start-existing-instance`: launches an existing EC2 instance
* `stop-instance`: stops an EC2 instance
* `list-instances`: lists all EC2 instances

Each command has its own parameters that can be passed through the command-line interface.
The `start-instances` command is used to launch new EC2 instances. Here's an example of using the command:
```python
python main.py start-instances --count 1 --image-id ami-xxxxxxxx --instance-type t2.micro --key-name my-key-pair --security-group sg-xxxxxxxx --subnet-id subnet-xxxxxxxx
```

The `start-existing-instance` command is used to launch an existing EC2 instance. Here's an example of using the command:
```python
python main.py start-existing-instance --instance-id i-xxxxxxxx
```
The `stop-instance` command is used to stop an EC2 instance. Here's an example of using the command:
```python
python main.py stop-instance --instance-id i-xxxxxxxx
```
The `list-instances` command is used to list all EC2 instances. Here's an example of using the command:
```python
python main.py list-instances
```

#### Author 

Носаченко Олег – MontyPython-ManuL