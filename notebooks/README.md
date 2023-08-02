# 🐍 Practices

## How to update the notebooks

> Hint: 👉 Don't update the notebooks. Update the python scripts.

- Update or create a **python script in the `src` directory**: e.g `src/1_data_engineering.py`
- In the script, add markers containing `LINE TO BE REMOVED FOR STUDENTS`
- Then run the makefile:
    ```
    make
    ```

Then the students' version for the script and all the notebooks will be generated automatically **in the `build` directory**.

Example: Starting from this folder structure:
```
notebooks
├──  src
│   └── 1_data_engineering.py
└── build
```
It will generate this folder structure:
```
notebooks
├──  src
│   └── 1_data_engineering.py
└── build
    ├── 1_data_engineering.ipynb
    └── 1_data_engineering_students.ipynb
```
