import os
import pprint

# functions

def run_tests(path,student,slug,patterns):
	# test_log = {
	#	'innerHTML': true,
	# 	'querySelector': false
	# }
	test_log = {
		"patterns": {},
		"summary": {
			"correct":0,
			"total":0
		}
	}
	for pattern in patterns:
		test_log["summary"]["total"] = test_log["summary"]["total"] + 1
		test_log["patterns"][pattern] = False

		with open(f'{path}/{student}/{slug}', 'rt') as f:
			lines = [line.rstrip('\n') for line in f]
			for line in lines:
				# print(line)
				if pattern.lower() in line.lower():
					if(test_log["patterns"][pattern] == False): # first time seeing pattern
						test_log["summary"]["correct"] = test_log["summary"]["correct"] + 1
					test_log["patterns"][pattern] = True
					# print('TRUE!!!')
	test_log["summary"]["score"] = test_log["summary"]["correct"]/test_log["summary"]["total"]
	# pprint.pprint(test_log)
	return(test_log)

# settings 
cohort = 'js-2023'
repo = 'dom-lessons-03-10-2022-08-27-36'
path = f'../../../Documents/github-classroom/{cohort}/{repo}'
student = 'adinb5793'
# slug = '01-basics/01-hw.html'
rubric = [
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

# run_tests(path,student,slug,patterns_01)
def run_student_tests(path,student,rubric):
	all_test_logs = []
	for lesson in rubric:
		all_test_logs.append(run_tests(path,student,lesson["slug"],lesson["patterns"]))
	# pprint.pprint(alltest_logs)
	average = 0
	for test_log in all_test_logs:
		average = average + test_log["summary"]["score"]
	average = average / len(all_test_logs)
	return(average*10)

# print(student + ": " + str(run_student_tests(path,student,rubric)))

students = os.listdir(path)
students.sort()
# print(students)

for student in students:
	print(student + ": " + str(run_student_tests(path,student,rubric)))