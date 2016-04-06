import requests
import json
import time
import os
import sys


headers_d = {
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding':'gzip, deflate, sdch',
	'Accept-Language':'en-US,en;q=0.8',
	'Connection':'keep-alive',
	'Cookies':'__RequestVerificationToken=J2MBeJ4VGXKqRbz2x1KLuwQDfXA92BKQG43k4r3UhLfZlSNPN0rZWWh3r9rKWPIU0kmeVVaAWilAnwcbtK0myx28tDM1; .ASPXAUTH=BDA05B2E543E5E03761458124DB49A6E0EE50400C84AF4B2FCF3895202A60FB5081E240533F3B78A23BA29F6612354D8DCFE7628E55B8F6BDB65C40172B7ECEF4A4CE5EFCB36C07BC794BB2A11D9F7D8029566F46EEAE6398C4985E3136852165F6570467E7D7DFC262F8FB338BA6C520FEE919B',
	'Cache-Control':'max-age=0',
	'Host':'berkeley.collegescheduler.com',
	'Referer':'https://berkeley.collegescheduler.com/spa',
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest'
}


"""
if __name__ == '__main__':
	if len(sys.argv) != 2:
		raise ValueError('Needs a cookie!!!')
	cookie = sys.argv[1]
"""
headers_d['Cookie'] = '__RequestVerificationToken=J2MBeJ4VGXKqRbz2x1KLuwQDfXA92BKQG43k4r3UhLfZlSNPN0rZWWh3r9rKWPIU0kmeVVaAWilAnwcbtK0myx28tDM1; .ASPXAUTH=BDA05B2E543E5E03761458124DB49A6E0EE50400C84AF4B2FCF3895202A60FB5081E240533F3B78A23BA29F6612354D8DCFE7628E55B8F6BDB65C40172B7ECEF4A4CE5EFCB36C07BC794BB2A11D9F7D8029566F46EEAE6398C4985E3136852165F6570467E7D7DFC262F8FB338BA6C520FEE919B'



def get_subject_ids():
	subjects_url = 'https://berkeley.collegescheduler.com/api/terms/2016%20Fall/subjects'
	response = requests.get(url=subjects_url, headers=headers_d)
	subjects_data = response.json()
	subject_ids = [d['id'] for d in subjects_data]

	if not os.path.exists('all_subjects/'):
		os.makedirs('all_subjects/')

	subject_json = 'all_subjects/subjects.json'
	with open(subject_json, 'w') as f:
		json.dump(subjects_data, f)
	return subject_ids

def get_subject_data(subject_ids):
	course_numbers = {}

	if not os.path.exists('subjects/'):
		os.makedirs('subjects/')

	for subject_id in subject_ids:
		subject_url = 'https://berkeley.collegescheduler.com/api/terms/2016%20Fall/subjects/{}/courses'.format(subject_id)
		time.sleep(3)
		print(subject_id)
		response = requests.get(url=subject_url, headers=headers_d)
		subject_data = response.json()
		course_numbers[subject_id] = [d['number'] for d in subject_data]
		with open('subjects/{}.json'.format(subject_id), 'w') as f:
			json.dump(subject_data, f)
	return course_numbers

def get_courses(course_numbers):
	for subject in course_numbers:
		course_path = 'courses/{}/'.format(subject)
		if not os.path.exists(course_path):
			os.makedirs(course_path)

		for course_number in course_numbers[subject]:
			course_url = 'https://berkeley.collegescheduler.com/api/terms/2016%20Fall/subjects/{0}/courses/{1}/regblocks'.format(subject, course_number)
			time.sleep(5)
			print(subject ,course_number)
			while True:
				try:
					response = requests.get(url=course_url, headers=headers_d)
					course_data = response.json()
					if "message" in course_data:
						raise IOError('Not authorized')		
					break
				except:
					print('TOO MANY REQUESTS, GONNA GET BANNED')
					time.sleep(60)
			course_data = response.json()
			with open('courses/{0}/{0}{1}'.format(subject, course_number), 'w') as f:
				json.dump(course_data, f)

def get_course_number_from_json():
	l_files = os.listdir('subjects/')
	course_numbers = {}
	for f in l_files:
		with open('subjects/{}'.format(f)) as json_f:
			#contains all courses of a given subject
			subject_data = json.load(json_f)
			subject_id = f.split('.')[0]
			course_numbers[subject_id] = [d['number'] for d in subject_data]
	return course_numbers

def set_cookie(cookie):
	headers_d['Cookie'] = cookie

if __name__ == '__main__':
	course_numbers = get_course_number_from_json()
	get_courses(course_numbers)