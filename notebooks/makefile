
1_data_engineering_students.py: 1_data_engineering.py
	sed 's/^\(\ *\).*LINE TO BE REMOVED FOR STUDENTS.*$$/\1*** FILL THE MISSING LINE ***/g' \
		1_data_engineering.py > 1_data_engineering_students.py

2_exploratory_data_analysis_students.py: 2_exploratory_data_analysis.py
	sed 's/^\(\ *\).*LINE TO BE REMOVED FOR STUDENTS.*$$/\1*** FILL THE MISSING LINE ***/g' \
		2_exploratory_data_analysis.py > 2_exploratory_data_analysis_students.py

1_data_engineering.ipynb: 1_data_engineering.py
	jupytext --to ipynb 1_data_engineering.py

1_data_engineering_students.ipynb: 1_data_engineering_students.py
	jupytext --to ipynb 1_data_engineering_students.py

2_exploratory_data_analysis.ipynb: 2_exploratory_data_analysis.py
	jupytext --to ipynb 2_exploratory_data_analysis.py

2_exploratory_data_analysis_students.ipynb: 2_exploratory_data_analysis_students.py
	jupytext --to ipynb 2_exploratory_data_analysis_students.py

students_scripts: 1_data_engineering_students.py 2_exploratory_data_analysis_students.py

all: 1_data_engineering_students.ipynb 2_exploratory_data_analysis_students.ipynb 1_data_engineering.ipynb 2_exploratory_data_analysis.ipynb
