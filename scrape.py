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
	'Host':'berkeley.collegescheduler.com',
	'Referer':'https://berkeley.collegescheduler.com/spa',
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest'
}

if __name__ == '__main__':
	if len(sys.argv) != 2:
		raise ValueError('Needs a cookie!!!')
	cookie = sys.argv[1]
	#cookie = '__RequestVerificationToken=J2MBeJ4VGXKqRbz2x1KLuwQDfXA92BKQG43k4r3UhLfZlSNPN0rZWWh3r9rKWPIU0kmeVVaAWilAnwcbtK0myx28tDM1; .ASPXAUTH=3EABCD9CE75711D198C28005A1C9BB2AD382A683D3BFFE16554C1DA16BB602498082876DA54594C0710B61B694C2DD2EB394B33B27939C492D64911F84CB8E6C607E2E34DF2CB87235737B6AE7081BA91805663B9FFCEB093D39E6D4186EA21C397BDBF359F6FB1BB7EF6817B86754A7953A24F8'
	headers_d['Cookie'] = cookie



def scrape_subject_ids():
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

#subject_ids = scrape_subject_ids()

def scrape_subject_data(subject_ids):
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

#course_numbers = scrape_subject_data(subject_ids)

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

def scrape_courses(course_numbers):
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
					break
				except:
					print('TOO MANY REQUESTS, GONNA GET BANNED')
					time.sleep(60)
			course_data = response.json()
			with open('courses/{0}/{0}{1}'.format(subject, course_number), 'w') as f:
				json.dump(course_data, f)


course_numbers = get_course_number_from_json()
scrape_courses(course_numbers)