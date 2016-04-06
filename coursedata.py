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
	'Cache-Control':'max-age=0',
	'Host':'berkeley.collegescheduler.com',
	'Referer':'https://berkeley.collegescheduler.com/spa',
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest'
}

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
	completed_ya = ['LGBT', 'FINNISH', 'MEDST', 'HEBREW', 'INDENG', 'UGIS', 'PLANTBI', 'PBHLTH', 'FILIPN', 'LINGUIS', 'BIOPHY', 'DEVENG', 'SANSKR', 'SCANDIN', 'PSYCH', 'SOCIOL', 'ITALIAN', 'BANGLA', 'ARABIC', 'BIOLOGY', 'PHYSED', 'GREEK', 'XMCELLB', 'XCOLWRI', 'MATSCI', 'SCMATHE', 'SEASIAN', 'ENVDES', 'ELENG', 'COGSCI', 'SSEASN', 'SEMITIC', 'NATAMST', 'XEPS', 'STAT', 'XRHETOR', 'COLWRIT', 'KOREAN', 'XESPM', 'PUNJABI', 'XCLASSI', 'COMLIT', 'JOURN', 'MCELLBI', 'DEVSTD', 'PHDBA', 'LATAMST', 'DEMOG', 'CRITTH', 'STS', 'KHMER', 'VISSCI', 'XENGLIS', 'EPS', 'FOLKLOR', 'EUST', 'ARMENI', 'MILAFF', 'NESTUD', 'CHEM', 'XHISTOR', 'POLISH', 'FRENCH', 'BOSCRSR', 'XMATH', 'NUSCTX', 'ASTRON', 'DUTCH', 'HISTART', 'SPANISH', 'UGBA', 'XPSYCH', 'INFO', 'XMUSIC', 'XGEOG', 'GPP', 'MEDIAST', 'PHYSICS', 'MBA', 'LANPRO', 'GMS', 'EGYPT', 'AEROSPC', 'INTEGBI', 'CHMENG', 'CZECH', 'NEUROSC', 'XFILM', 'NSE', 'PUBPOL', 'EWMBA', 'HISTORY', 'THAI', 'ANTHRO', 'OPTOM', 'ESPM', 'XPHILOS', 'XHISTAR', 'XASAMST', 'CMPBIO', 'LATIN', 'MATH', 'XSOCIOL', 'EECS', 'XETHSTD', 'YIDDISH', 'DANISH', 'ISF', 'LDARCH', 'SWEDISH', 'XLINGUI', 'AFRICAM', 'LEGALST', 'ASAMST', 'MONGOLN', 'ASIANST', 'CUNEIF', 'MILSCI', 'TAMIL', 'TURKISH', 'SASIAN', 'GERMAN', 'TELUGU', 'PERSIAN', 'TIBETAN', 'LS', 'VISSTD', 'MECENG', 'XLEGALS', 'XMESTU', 'GWS', 'NORWEGN', 'EALANG', 'POLECON', 'AST', 'XINTEGB', 'ECON', 'ARCH', 'EDUC', 'MALAYI', 'PACS', 'ENGIN', 'NUCENG', 'ENGLISH', 'CIVENG', 'THEATER', 'DEVP', 'MFE', 'PHILOS', 'COMPSCI', 'RUSSIAN', 'ENVECON', 'VIETNMS', 'NWMEDIA', 'RHETOR', 'SOCWEL', 'CHINESE', 'JEWISH', 'XSTAT', 'CATALAN', 'CYPLAN', 'NAVSCI', 'XGWS', 'BURMESE', 'CLASSIC', 'HUNGARI', 'BUDDSTD', 'CELTIC', 'FILM', 'COMPBIO', 'XPOLSCI', 'ART', 'AMERSTD', 'BIOENG', 'ARESEC', 'ENERES', 'MESTU', 'ICELAND', 'XASTRON', 'POLSCI', 'PORTUG', 'ETHSTD', 'CHICANO', 'JAPAN', 'NATRES', 'SLAVIC', 'GEOG']



	for subject in course_numbers:
		if subject in completed_ya:
			continue
		course_path = 'courses/{}/'.format(subject)
		if not os.path.exists(course_path):
			os.makedirs(course_path)

		for course_number in course_numbers[subject]:
			course_url = 'https://berkeley.collegescheduler.com/api/terms/2016%20Fall/subjects/{0}/courses/{1}/regblocks'.format(subject, course_number)
			time.sleep(3)
			print(subject ,course_number)
			while True:
				try:
					response = requests.get(url=course_url, headers=headers_d)
					course_data = response.json()
					if "message" in course_data:
						raise IOError('Not authorized')		
					break
				except IOError as e:
					print(e)
					print('Not Authorized?')
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
	cookie = '__RequestVerificationToken=J2MBeJ4VGXKqRbz2x1KLuwQDfXA92BKQG43k4r3UhLfZlSNPN0rZWWh3r9rKWPIU0kmeVVaAWilAnwcbtK0myx28tDM1; .ASPXAUTH=438FFEC72E53A4879F86C412F3C43210D81D146EB943B05F17731EED9B9965D9737890237CC18057510A33E3F3EFBA410A70A8C80BC1BF34220BA29F94B1CFD0CEF36F990FCC4E555AAC8C99F6D641EB97868AD23C18DF92B64226173ABBA1A79DD26918DC155E43809742C001693E4C40F01AF5'
	set_cookie(cookie)
	course_numbers = get_course_number_from_json()
	get_courses(course_numbers)