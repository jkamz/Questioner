<div align="center">

<img width=200 src="https://jkamz.github.io/Questioner/UI/static/images/logo.png">

# Questioner API

[![Build Status](https://travis-ci.org/jkamz/Questioner.svg?branch=develop)](https://travis-ci.org/jkamz/Questioner) [![Coverage Status](https://coveralls.io/repos/github/jkamz/Questioner/badge.svg?branch=develop)](https://coveralls.io/github/jkamz/Questioner?branch=develop)   [![Maintainability](https://api.codeclimate.com/v1/badges/ccc01049d9b2db4cf789/maintainability)](https://codeclimate.com/github/jkamz/Questioner/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/ccc01049d9b2db4cf789/test_coverage)](https://codeclimate.com/github/jkamz/Questioner/test_coverage)

</div>

## Summary
Questioner helps a meetup organizer prioritize questions to be answered during the meetup. After an admin has created a meetup, users can post questions relevant to that meetup. Users are then allowed to upvote or downvote a question thereby allowing the organizer to prioritize the questions based on the votes.

The project is managed using [Pivotal Tracker](https://www.pivotaltracker.com) and is available [here](https://www.pivotaltracker.com/n/projects/2235485)

## Site links
### Heroku

`https://questionerandela.herokuapp.com`

## Endpoints

Required Method       | EndPoint       | Functionality |
------------- | ------------- | ---------------
POST  | /api/v1/create_meetup  | Post a new meetup record   |
GET  | /api/v1/meetups/<int:meetup_id>  | Get a specific meetup   |
GET  | /api/v1/meetups/   | Get all meetup records   |
POST  | /api/v1/meetup/<int:meetup_id>/question | Create a question for a specific meetup.   |
GET  | /api/v1/meetup/<int:meetup_id>/<int:question_id> | Get a specific question for a specific meetup.   |
GET  | /api/v1/meetup/<int:meetup_id>/questions> | Get all questions for a specific meetup.   |
PUT | /api/v1/questions/<int:question_id>/upvote | Adds votes by one |
PUT | /api/v1/questions/<int:question_id>/downvote | Decreases votes by one  |
POST | /api/v1/meetups/<int:meetup_id>/rsvps | Create a RSVP for a specific meetup



## Getting Started

To test the API on your local machine, start by cloning the Repository and navigating to the root folder

`git clone https://github.com/jkamz/Questioner`
`cd Questioner` to navigate to the root folder
`git checkout develop` to navigate to the develop branch

### Prerequisites
- python 3.6
- pip - python package manager
- Postman - for testing the end points
- Git - for version control

### Installation
Run the commands

    • `python3 -m venv venv` to install virtual environment
    • `source venv/bin/activate` to activate the virtual environment
    • `pip install -r requirements.txt` to install all the requirements
    • `export APP_SETTINGS='development'` to setup the environment
    • `flask run` to launch the API

### Running Tests
Run

`pytest --cov-report term --cov=app/tests/v1`

#### Postman

Run `flask run`
Test the defined endpoints in postman

## Acknowledgments
- slack nbo-36
- nbo-36 team 12 members

## Author

[John Kamau](https://github.com/jkamz)

