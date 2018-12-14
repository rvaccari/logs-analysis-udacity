# Logs Analysis

This is my solution for the Logs Analysis project in Udacity Full Stack Nanodegree course.

## You will need:
- Python3
- Docker

## How to run the project.

1. Clone this repository
2. Enter the directory
3. Create a virtual env
4. Enable virtual env
5. Install the dependencies
5. Run docker-compose
6. Load data
7. Run analyzer.py

```
git clone
cd log_analyses
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
docker-compose up -d
psql -U vagrant -d news -1 -f newsdata.sql  -h 127.0.0.1 -p 5432
python analyzer.py
```

