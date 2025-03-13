# python3 main.py
# open grades.csv in Excel > copy/paste to gSheet

import glob
import os
import pprint
import math
import re
import csv
import json

##### COLORS #####

PURPLE = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


##### RUBRICS #####

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




##### SETTINGS (cohort, repo, rubric) #####

### SEP10 ###
# cohort = 'wd-2027' # SEP10

# repo = 'rwd-principles'
# rubric = sep10_rwd_principles_rubric

# repo = 'bootstrap-grid-practice'
# rubric = sep10_bootstrap_grid_rubric


### SEP11 ###
cohort = 'js-2026' # SEP11
order_file = 'sep11info.json'

# repo = 'dom-lessons'
# rubric = sep11_dom_rubric

repo = 'p5js'
rubric = sep11_p5js_basics_rubric
# rubric = sep11_p5js_zoog_rubric
# rubric = sep11_p5js_movement_rubric
# rubric = sep11_p5js_interactivity_rubric
# rubric = sep11_p5js_application_rubric
# rubric = sep11_p5js_applicativity_rubric




##### PROGRAM #####

base_path = f'../../../../Documents/github-classroom/{cohort}/'
matching_folders = glob.glob(os.path.join(base_path, f"{repo}*"))

if matching_folders:
    BASE_DIR = matching_folders[0]  # Take the first match (there should be only one)
else:
    raise FileNotFoundError(f"No folder found starting with '{repo}' in {base_path}")

OUTPUT_FILE = "grades.csv"

# Load student order from JSON file
try:
    with open(order_file, 'r', encoding='utf-8') as f:
        student_order = json.load(f).get("students", [])
except (FileNotFoundError, json.JSONDecodeError):
    print(f"Warning: {order_file} not found or invalid. Defaulting to alphabetical order.")
    student_order = []

# Get list of students from directory
students = [s for s in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, s))]

# Reorder students based on the JSON file
if student_order:
    students = [s for s in student_order if s in students]  # Keep only students in both lists
else:
    students = sorted(students)  # Default to alphabetical order if JSON is missing

# Write results to a CSV file
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # Header row
    column_headers = ["Student"] + [assignment["slug"] for assignment in rubric] + ["Average (%)", "Out of 10"]
    writer.writerow(column_headers)

    for student in students:
        student_path = os.path.join(BASE_DIR, student)
        scores = [student]  # Start row with student name
        numeric_scores = []

        for assignment in rubric:
            file_path = os.path.join(student_path, assignment["slug"])

            if not os.path.exists(file_path):
                scores.append("0")  # File missing → score 0
                numeric_scores.append(0)
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            total_patterns = len(assignment["patterns"])
            match_count = sum(bool(re.search(pattern, content)) for pattern in assignment["patterns"])
            score = (match_count / total_patterns) * 10 if total_patterns else 0

            scores.append(f"{score:.2f}")
            numeric_scores.append(score)

        # Calculate the average and add extra columns
        if numeric_scores:
            avg_score = sum(numeric_scores) / len(numeric_scores)
            avg_percentage = f"{round(avg_score * 10)}%"
            
            # Round to nearest tenth and remove trailing .0 if it's a whole number
            avg_out_of_10 = round(avg_score, 1)
            avg_out_of_10 = int(avg_out_of_10) if avg_out_of_10.is_integer() else avg_out_of_10
        else:
            avg_percentage = "0%"
            avg_out_of_10 = 0

        scores.append(avg_percentage)
        scores.append(avg_out_of_10)

        # Write row to CSV
        writer.writerow(scores)

print(f"Grades saved to {OUTPUT_FILE}. Open it in Google Sheets.")