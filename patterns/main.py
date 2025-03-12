# python3 main.py
# open grades.csv in Excel > copy/paste to gSheet

import glob
import os
import pprint
import math
import re
import csv

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

repo = 'dom-lessons'
rubric = sep11_dom_rubric

# repo = 'p5js'
# rubric = sep11_p5js_basics_rubric
# rubric = sep11_p5js_zoog_rubric
# rubric = sep11_p5js_movement_rubric
# rubric = sep11_p5js_interactivity_rubric
# rubric = sep11_p5js_application_rubric
# rubric = sep11_p5js_applicativity_rubric




##### PROGRAM #####

base_path = f'../../../../Documents/github-classroom/{cohort}/'
matching_folders = glob.glob(os.path.join(base_path, f"{repo}*"))  # Find folders starting with `repo`
if matching_folders:
    BASE_DIR = matching_folders[0]  # Take the first match (there should be only one)
else:
    raise FileNotFoundError(f"No folder found starting with '{repo}' in {base_path}")

OUTPUT_FILE = "grades.csv"

# Get student folders, sorted alphabetically
students = sorted([s for s in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, s))])

# Write results to a CSV file
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write header row
    writer.writerow(["Student"] + [assignment["slug"] for assignment in rubric])

    for student in students:
        student_path = os.path.join(BASE_DIR, student)
        scores = [student]  # Start row with student name

        for assignment in rubric:
            file_path = os.path.join(student_path, assignment["slug"])

            if not os.path.exists(file_path):
                scores.append("0")  # If file is missing, score 0
                continue

            # Read file contents
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Count pattern matches
            total_patterns = len(assignment["patterns"])
            match_count = sum(bool(re.search(pattern, content)) for pattern in assignment["patterns"])

            # Calculate score out of 10
            score = (match_count / total_patterns) * 10 if total_patterns else 0
            scores.append(f"{score:.2f}")

        # Write row to CSV file
        writer.writerow(scores)

print(f"Grades saved to {OUTPUT_FILE}. Open it in Google Sheets.")