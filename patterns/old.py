# `>>> isinstance([0, 10, 20, 30], list) # True`
# `>>> isinstance(50, list) # False`
# `if type(a_list) == list:`


import os
import pprint
import math
from re import search

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

	try:
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
					# if pattern.lower() in line.lower():
					if search(pattern.lower(), line.lower()):
						if(test_log["patterns"][pattern] == False): # first time seeing pattern
							test_log["summary"]["correct"] = test_log["summary"]["correct"] + 1
						test_log["patterns"][pattern] = True
						if(show_matches):
							print(color_line(line,pattern,YELLOW))
	except:
		# print("File: " + student + "/" + test_log["file"] + " not found.")
		pass
	test_log["summary"]["score"] = test_log["summary"]["correct"]/test_log["summary"]["total"]
	# pprint.pprint(test_log)
	return(test_log)

def run_student_tests(path,student,rubric,details,show_matches,student_breakdown):
	all_test_logs = []
	for lesson in rubric:
		all_test_logs.append(run_tests(path,student,lesson["slug"],lesson["patterns"],show_matches))
	if(details):
		pprint.pprint(all_test_logs)
	if(student_breakdown):
		# print("")
		for test_log in all_test_logs:
			# pprint.pprint(all_test_logs)
			score = test_log["summary"]["score"] # out of 1.0
			score = round(score,3)
			score = score*10
			if float(score).is_integer(): # i.e. turn 10.0 into 10
				score = int(score)
			print(student + ": " + test_log["file"] + " " + str(score) + "/10")
	average = 0
	for test_log in all_test_logs:
		average = average + test_log["summary"]["score"]
	average = average / len(all_test_logs)
	average = average*10
	average = round(average,2)
	if float(average).is_integer(): # i.e. turn 10.0 into 10
		average = int(average)
	return(average)

##### archive #####

template_rubric = [
	{
		"slug": 'html',
		"patterns": ['pattern1', 'pattern2']
	},
]

# SEP10

sep10_rwd_principles_rubric = [
	{
		"slug": 'style.css',
		"patterns": ['media', 'v']
	},
]

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
		"patterns": ['querySelector', 'innerHTML.*\+=', 'innerHTML.*=']
	},
	{
		"slug": '02-details/02-hw.html',
		"patterns": ['\.style', '.classList.add', '.classList.remove', '.classList.toggle']
	},
	{
		"slug": '03-creating/03-hw.html',
		"patterns": ['createElement', 'appendChild', 'insertBefore']
	},
	{
		"slug": '04-iterating/04-hw.html',
		"patterns": ['forEach', 'querySelectorAll']
	},
	{
		"slug": '05-events/05-hw.html',
		"patterns": ['addEventListener', 'click', 'keypress', 'mouse']
	},
	{
		"slug": '06-inputs/06-hw.html',
		"patterns": ['input', 'radio', 'select']
	}
]

sep11_p5js_basics_rubric = [
	{
		"slug": '01-basics/shapes-hw.html',
		"patterns": ['rect', 'ellipse', 'line']
	},
	{
		"slug": '01-basics/text-hw.html',
		"patterns": ['text']
	},
	{
		"slug": '01-basics/color-hw.html',
		"patterns": ['(fill|stroke)']
	}
]

sep11_p5js_zoog_rubric = [
	{
		"slug": '01-basics/zoog.html',
		"patterns": ['\/\/(?! JS)', 'background', 'point', 'line', 'rect', 
					 'ellipse', 'text', 'fill', 'stroke', 'strokeWeight']
	}
]

sep11_p5js_movement_rubric = [
	{
		"slug": '02-movement/variables-hw.html',
		"patterns": ['(?<!ntent..|device\-)width','height'] # fixed width: both 7 letters (ignore meta tag)
	},
	{
		"slug": '02-movement/mousexy-hw.html',
		"patterns": ['mouseX','mouseY']
	},
	{
		"slug": '02-movement/events-hw.html',
		"patterns": ['(function mouse|function key)'] # OR
	},
	{
		"slug": '02-movement/random-hw.html',
		"patterns": ['random']
	}
]

sep11_p5js_interactivity_rubric = [
	{
		"slug": '02-movement/interactivity.html',
		"patterns": ['var', '(?<!ntent..|device\-)width', 'height', 'mouseX', 'mouseY', 
					 'constrain', 'function mouse', 'function key', 'random', 'h1']
	}
]

sep11_p5js_application_rubric = [
	{
		"slug": '03-application/conditionals-hw.html',
		"patterns": ['if','key']
	},
	{
		"slug": '03-application/functions-hw.html',
		"patterns": ['function']
	},
	{
		"slug": '03-application/loops-hw.html',
		"patterns": ['(for|while)']
	},
	{
		"slug": '03-application/arrays-hw.html',
		"patterns": ['\[']
	},
]

sep11_p5js_applicativity_rubric = [
	{
		"slug": '03-application/applicativity.html',
		"patterns": ['if', 'for', '\[', 'h1', '\//']
	}
]




##### PROGRAM #####

# SETTINGS

### SEP10 ###
cohort = 'wd-2026' # SEP10

# repo = 'rwd-principles-03-14-2024-03-37-05'
# rubric = sep10_rwd_principles_rubric

# repo = 'bootstrap-grid-practice-03-14-2024-03-11-48'
# rubric = sep10_bootstrap_grid_rubric

### SEP11 ###

cohort = 'js-2025' # SEP11

# repo = 'dom-lessons-03-14-2024-03-10-35'
# rubric = sep11_dom_rubric

repo = 'p5js-03-14-2024-03-11-11'
# rubric = sep11_p5js_basics_rubric
rubric = sep11_p5js_zoog_rubric
# rubric = sep11_p5js_movement_rubric
# rubric = sep11_p5js_interactivity_rubric
# rubric = sep11_p5js_application_rubric
# rubric = sep11_p5js_applicativity_rubric

path = f'../../../Documents/github-classroom/{cohort}/{repo}' # NO NEED TO EDIT

# DO NOT EDIT
students = os.listdir(path)
students.sort()



# MAIN PROGRAM
def run():
	num_students = 0
	score_total = 0
	for student in students:
		
		# final score only
		student_score = run_student_tests(path,student,rubric,False,False,False) # details, show_matches, student_breakdown
		print(student + ": " + str(student_score)) 
		
		# breakdown
		# print(student + ": AVERAGE " + str(run_student_tests(path,student,rubric,False,False,True)) + "/10") # details, show_matches, student_breakdown

		# average
		num_students = num_students + 1
		score_total = score_total + student_score
		
	
	print("AVERAGE: " + str(round(score_total/num_students,2)))


##### PRINT #####

# CONFIRM STUDENTS
# print(students)

# PRINT ONE STUDENT
# student = 'austinl1905'
# print(student + ": " + str(run_student_tests(path,student,rubric,True,False,False))) # details, show_matches,student_breakdown

# python3 patterns.py
run()