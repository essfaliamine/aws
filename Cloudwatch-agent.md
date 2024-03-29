# Cloudwatch | Monitor Memory $ disk




## Step 1: Create an IAM role and Attach CloudWatch and SSM Full Access
## Step 2: Create a parameter in Systems Manger with the name "/Alarm/AWS-CWAgentConfig" and store the value:
```bash
{
	"metrics": {
		"append_dimensions": {
			"InstanceId": "${aws:InstanceId}"
		},
		"namespace": "LinuxInstances",
		"metrics_collected": {
			"mem": {
				"measurement": [
					{"name": "mem_used_percent", "rename": "MemoryUtilization"}
					"mem_used_percent"
					],
					"metrics_collection_interval": 60
				},
			"disk": {
        			"measurement": [
                  			{"name": "used_percent", "rename": "DiskSpaceUtilization"}
        				],
        				"metrics_collection_interval": 60,
        				"resources": [
                 				 "*"
        				]
        			}
		}
	}
}
```

## Step 3: Create an EC2 Instance, Attach the role created in Step 1 and Add the following commands in the Userdata Section:

```bash
#!/bin/bash
wget https://s3.amazonaws.com/amazoncloudwatch-agent/linux/amd64/latest/AmazonCloudWatchAgent.zip
unzip AmazonCloudWatchAgent.zip
sudo ./install.sh
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c ssm:/Alarm/AWS-CWAgentConfig -s
```

## Check the status of the CWAgent:
```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -m ec2 -a status
```


## Reference/Additional Reading:
1. https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent-New-Instances-CloudFormation.html
2. https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-Configuration-File-Details.html

