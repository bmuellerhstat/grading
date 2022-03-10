import pprint

# settings 

cohort = 'js-2023'
assignment = 'dom-lessons-03-10-2022-08-27-36'
slug = '01-basics/01-hw.html'

# functions

path = f'../../../Documents/github-classroom/{cohort}/{assignment}'

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

# program

student = 'adinb5793'
slug = '01-basics/01-hw.html'
patterns_01 = ['querySelector', 'innerHTML']

run_tests(path,student,slug,patterns_01)



# backup

# # settings 

# cohort = 'js-2023'
# assignment = 'dom-lessons-03-10-2022-08-27-36'
# slug = '01-basics/01-hw.html'

# # functions

# path = f'../../../Documents/github-classroom/{cohort}/{assignment}'

# def run_tests(path,student,slug,patterns):
# 	# testLog = {
# 	#	'innerHTML': true,
# 	# 	'querySelector': false
# 	# }
# 	testLog = {}
# 	for pattern in patterns:
# 		testLog[pattern] = False

# 		with open(f'{path}/{student}/{slug}', 'rt') as f:
# 			lines = [line.rstrip('\n') for line in f]
# 			for line in lines:
# 				print(line)
# 				if pattern.lower() in line.lower():
# 					testLog[pattern] = True
# 					print('TRUE!!!')
# 	print(testLog)
# 	return(testLog)

# # program

# student = 'adinb5793'
# slug = '01-basics/01-hw.html'
# patterns_01 = ['querySelector', 'innerHTML']
# # patterns_01 = 'querySelector'

# run_tests(path,student,slug,patterns_01)

