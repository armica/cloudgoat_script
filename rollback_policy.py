import boto3
import json

session = boto3.session.Session(profile_name='seon', region_name='ap-northeast-2')
client = session.client('iam')

policy_details = []
count_id = 0

response = client.get_account_authorization_details()
while response['IsTruncated']:
	response = client.get_account_authorization_details(Marker=response['Marker'])
	if response.get('Policies'):
		policy_details.extend(response['Policies'])

with open('./check_IAM_PRIVESC_BY_ROLLBACK.txt', 'w+') as f:
	for version in policy_details:
		for id in version['PolicyVersionList']:
			if int(id['IsDefaultVersion']) == 0:
				count_id += 1
		if count_id > 1:
			f.write('Arn : ' + version['Arn'])
			print('Arn : ' + version['Arn'])        
			for id in version['PolicyVersionList']:
				f.write('VersionId : ' + id['VersionId'])
				f.write('IsDefaultVersion : ' + str(id['IsDefaultVersion']))            
				print('VersionId : ' + id['VersionId'])
				print('IsDefaultVersion : ' + str(id['IsDefaultVersion']))
			f.write('\n')                
			print('\n')
		count_id = 0