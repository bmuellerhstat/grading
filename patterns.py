import pprint

# functions

def run_tests(path,student,slug,patterns):
	# testLog = {
	#	'innerHTML': true,
	# 	'querySelector': false
	# }
	testLog = {
		"patterns": {},
		"summary": {
			"correct":0,
			"total":0
		}
	}
	for pattern in patterns:
		testLog["summary"]["total"] = testLog["summary"]["total"] + 1
		testLog["patterns"][pattern] = False

		with open(f'{path}/{student}/{slug}', 'rt') as f:
			lines = [line.rstrip('\n') for line in f]
			for line in lines:
				# print(line)
				if pattern.lower() in line.lower():
					if(testLog["patterns"][pattern] == False): # first time seeing pattern
						testLog["summary"]["correct"] = testLog["summary"]["correct"] + 1
					testLog["patterns"][pattern] = True
					# print('TRUE!!!')

	pprint.pprint(testLog)
	return(testLog)

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
	for lesson in rubric:
		run_tests(path,student,lesson["slug"],lesson["patterns"])

run_student_tests(path,student,rubric)