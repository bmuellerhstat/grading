import os
import pprint

##### colors #####

PURPLE = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

##### functions #####

def color_line(line,pattern,color):
	start = line.find(pattern)
	return line[0:start] + color + pattern + ENDC + line[start+len(pattern):]

# print(color_line('my code snippet','code',RED))

def run_tests(path,student,slug,patterns,show_matches):
	test_log = {
		"file": "",
		"patterns": {},
		"summary": {
			"correct":0,
			"total":0
		}
	}
	for pattern in patterns:
		test_log["summary"]["total"] = test_log["summary"]["total"] + 1
		test_log["patterns"][pattern] = False
		test_log["file"] = slug

		if(show_matches):
			print(CYAN + slug + ": " + pattern + ENDC)

		with open(f'{path}/{student}/{slug}', 'rt') as f:
			lines = [line.rstrip('\n') for line in f]
			for line in lines:
				# print(line)
				if pattern.lower() in line.lower():
					if(test_log["patterns"][pattern] == False): # first time seeing pattern
						test_log["summary"]["correct"] = test_log["summary"]["correct"] + 1
					test_log["patterns"][pattern] = True
					if(show_matches):
						print(color_line(line,pattern,YELLOW))
	test_log["summary"]["score"] = test_log["summary"]["correct"]/test_log["summary"]["total"]
	# pprint.pprint(test_log)
	return(test_log)

def run_student_tests(path,student,rubric,details,show_matches):
	all_test_logs = []
	for lesson in rubric:
		all_test_logs.append(run_tests(path,student,lesson["slug"],lesson["patterns"],show_matches))
	if(details):
		pprint.pprint(all_test_logs)
	average = 0
	for test_log in all_test_logs:
		average = average + test_log["summary"]["score"]
	average = average / len(all_test_logs)
	return(round(average*10,1)) # one decimal point, i.e. 9.7

##### archive #####

template_rubric = [
	{
		"slug": 'html',
		"patterns": ['pattern1', 'pattern2']
	},
]

# SEP10

sep10_bootstrap_grid_rubric = [
	{
		"slug": 'index.html',
		"patterns": ['container', 'fluid','row','col']
	},
]

sep10_rwd_principles_rubric = [
	{
		"slug": 'style.css',
		"patterns": ['media', 'v']
	},
]


# SEP11

sep11_dom_rubric = [
	{
		"slug": '01-basics/01-hw.html',
		"patterns": ['.querySelector', '.innerHTML']
	},
	{
		"slug": '02-details/02-hw.html',
		"patterns": ['.style', '.classList.add', '.classList.remove', '.classList.toggle']
	},
	{
		"slug": '03-creating/03-hw.html',
		"patterns": ['.createElement', 'body.appendChild', ').appendChild', '.insertBefore']
	},
	{
		"slug": '04-iterating/04-hw.html',
		"patterns": ['.forEach', '.querySelectorAll']
	},
	{
		"slug": '05-events/05-hw.html',
		"patterns": ['.addEventListener', 'click', 'keypress', 'mouse']
	},
	{
		"slug": '06-inputs/06-hw.html',
		"patterns": ['input', 'radio', 'select']
	}
]



##### PROGRAM #####

# SETTINGS

### SEP10 ###
cohort = 'wd-2024' # SEP10

repo = 'grid-practice-03-11-2022-08-21-17' # work
rubric = sep10_bootstrap_grid_rubric

# repo = 'rwd-principles-03-16-2022-10-40-37' # work
# rubric = sep10_rwd_principles_rubric

### SEP11 ###

# cohort = 'js-2023' # SEP11
# repo = 'dom-lessons-03-10-2022-08-27-36' # work
# rubric = sep11_dom_rubric

path = f'../../../Documents/github-classroom/{cohort}/{repo}' # NO NEED TO EDIT

# DO NOT EDIT
students = os.listdir(path)
students.sort()



# MAIN PROGRAM
def run():
	for student in students:
		print(student + ": " + str(run_student_tests(path,student,rubric,False,False))) # details, show_matches


##### PRINT #####

# CONFIRM STUDENTS
# print(students)

# PRINT ONE STUDENT
# student = 'fuadhoquef8414'
# print(student + ": " + str(run_student_tests(path,student,rubric,True,True))) # details, show_matches

run()