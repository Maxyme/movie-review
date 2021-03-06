### movie-review

A simple way to share movie recommendations with friends and family

### checking the webapp:

https://movie-review-staging.herokuapp.com/
https://movie-review-pro.herokuapp.com/

## setting up a dev environment:

- install dev packages: `pipenv install --dev`
- install test packages: `pipenv install --test`

## running the backend

- run: `pipenv shell`
- run: `pipenv run "quart run --host 127.0.0.1 --port 5000"`.
- the environment variables from .env will be sourced automatically with pipenv.
- Hypercorn can also be used: `pipenv run hypercorn -b 127.0.0.1:5000 app:app`

### setting up heroku (do twice for staging)

`heroku create movie-review-pro`  
`git remote add pro git@heroku.com:movie-review-pro.git`

### deploying to heroku

- staging: `git push staging master`  
- production: `git push pro master`

### run on heroku server
`heroku run python app.py --app movie-review-staging`

### Starting the local postgres db

`docker-compose up -d`

### Migrations and database

- flask cli will automatically read the .env file with pipenv run.
`flask db init`
- making the migrations and upgrading the db
`flask db migrate`
`flask db upgrade`

### Spacy:

- installing a package:
`python -m spacy download en`

### Heroku (tips)

- checking the config (env variables):  
`heroku config --app movie-review-staging`
- adding a postgres db:  
`heroku addons:create heroku-postgresql:hobby-dev --app movie-review-staging`
- adding a redis instance:
`heroku addons:create redistogo:nano --app movie-review-staging`
- run the migrations on heroku:  
`heroku run "cd app && flask db upgrade" --app movie-review-staging`
- run locally with environment file (loads the heroku.sh file)
`heroku local -e .env`
- setting environment variables on heroky, with heroku toolbelt cli: 
`heroku config:set DEBUG=True --remote staging`  
`heroku config:set DEBUG=False --remote pro`  
- check the number of free hours for the app:
`heroku ps -a movie-review-staging`
- start psql:
`heroku pg:psql --app movie-review-staging`
- get db info:
`heroku pg:info --app movie-review-staging`
