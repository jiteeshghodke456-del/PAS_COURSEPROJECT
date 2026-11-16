# Student Participation and Academic Achievement Prediction

PAS (MM0805 Probability & Statistics) Course Project – Group 3A6, A Division, Batch 3
Guide: Mr. Rajkumar V. Patil

| GR No | Roll No | Name |
|---|---|---|
| 1251080091 | 2080166 | Jiteesh Prashant Ghodke |
| 1251080081 | 2080159 | Kaustubh Rajkumar Gawali |
| 1251080122 | 2080152 | Himanshu Pushparaj Gaikwad |
| 1251080260 | 2080167 | Sparsh Sandip Zalwade |

## What is here

| Path | Contents |
|---|---|
| `index.html` | Website showing every code cell with its output |
| `project/CP_Group3A6_Student_Participation.ipynb` | Jupyter notebook (code + outputs) |
| `project/student-por.csv` | Original dataset (649 rows x 33 columns, `;` separated) |
| `project/student_cleaned.csv` | Cleaned dataset (634 rows x 12 columns) |
| `build_site.py` | Rebuilds `index.html` from the notebook |

## Dataset source

UCI Machine Learning Repository – Student Performance dataset, P. Cortez and A. Silva (2008).
https://archive.ics.uci.edu/dataset/320/student+performance

## Run the notebook

```
pip install -r requirements.txt
cd project
jupyter notebook CP_Group3A6_Student_Participation.ipynb
```
Then use Kernel → Restart & Run All.

## Rebuild the website after changing the notebook

Run the notebook first (so outputs are saved), then from the repo root:
```
pip install nbformat markdown pygments
python build_site.py
```

## Host on GitHub Pages

Push this folder to a GitHub repo → Settings → Pages → Source: "Deploy from a branch" → Branch: `main`, folder `/ (root)` → Save.
The site will be at `https://<your-username>.github.io/<repo-name>/`.
