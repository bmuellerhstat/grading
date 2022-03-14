import os
import pprint

##### functions #####

def run_tests(path,student,slug,patterns):
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

		with open(f'{path}/{student}/{slug}', 'rt') as f:
			lines = [line.rstrip('\n') for line in f]
			for line in lines:
				# print(line)
				if pattern.lower() in line.lower():
					if(test_log["patterns"][pattern] == False): # first time seeing pattern
						test_log["summary"]["correct"] = test_log["summary"]["correct"] + 1
					test_log["patterns"][pattern] = True
	test_log["summary"]["score"] = test_log["summary"]["correct"]/test_log["summary"]["total"]
	# pprint.pprint(test_log)
	return(test_log)

def run_student_tests(path,student,rubric,details):
	all_test_logs = []
	for lesson in rubric:
		all_test_logs.append(run_tests(path,student,lesson["slug"],lesson["patterns"]))
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

# cohort = 'wd-2024' # SEP10
# repo = 'grid-practice-03-13-2022-09-40-08'
# rubric = sep10_bootstrap_grid_rubric

cohort = 'js-2023' # SEP11
repo = 'dom-lessons-03-10-2022-08-27-36'
rubric = sep11_dom_rubric

path = f'../../../Documents/github-classroom/{cohort}/{repo}' # NO NEED TO EDIT

# DO NOT EDIT
students = os.listdir(path)
students.sort()



# MAIN PROGRAM
def run():
	for student in students:
		print(student + ": " + str(run_student_tests(path,student,rubric,False)))


##### PRINT #####

# CONFIRM STUDENTS
# print(students)

# PRINT ONE STUDENT
student = 'fuadhoquef8414'
print(student + ": " + str(run_student_tests(path,student,rubric,True)))

# run()