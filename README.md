# Yescapa Backend Challenge
This test is part of our hiring process at Yescapa for backend positions.

**Looking for a job? Contact us at jobs@yescapa.com**

## Get started

Create a Python 3.8 virtualenv
`python3.8 -m venv ./virtualenv`

Install dependencies
```
source ./virtualenv/bin/activate`
pip install -r requirements.txt
```

Migrate the database
`python manage.py migrate`

Run the server
`python manage.py runserver`

Optionally:

- Run lint & format `black . ; flake8 backendcampers`
- Run type checker `mypy .`
- Run tests `coverage run manage.py test -v 2`

## Challenge
During this challenge, you will create a search engine to find the best campers to rent for your next roadtrip.
Across the 3 levels, the difficulty is raising and the engine can handle more precise searches.

## Guidelines
- Clone this repo
- Solve the levels in ascending order

For each level, write code that creates a new `results.json` file from the json data in the `data` directory.
An `expected_results.json` file is available to give you a reference on what result is expected.

## Evaluation
Our criteria:
- Correctness. The program should generate the correct output.
- Clarity. Is the code well-organized and clear?
- Robustness. Is the code easy maintenable and scalable?

## Sending your results
Once you are done, please send your results to the person you are talking to.

You can send your GitHub/Gitlab project link or zip your directory and send it via email.
If you do not use Github, don't forget to attach your .git folder.

Good luck!
