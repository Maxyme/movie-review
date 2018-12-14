### movie-review
A simple way to share movie recommendations with friends and family

### checking the webapp:
https://movie-review-staging.herokuapp.com/
https://movie-review-pro.herokuapp.com/

## setting up a dev environment:
- `pipenv install --dev`
- `pipenv install --test`

## running the backend
- run `dotenv run quart run` and in a separate terminal `dotenv run python worker.py`.
- the environment variables from .env will be sourced automatically by flask-cli and dotenv.
- Hypercorn can also be used: `dotenv run hypercorn -b 127.0.0.1:${PORT} "app:create_app()"`

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
- flask cli will automatically read the .flaskenv file if python-dotnet is installed and add source it.
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
- adding a redis instance on heroku
`heroku addons:create redistogo:nano --app movie-review-staging`
- run the migrations on heroku:  
`heroku run python manage.py db upgrade --app movie-review-staging`
- run locally with environment file (loads the heroku.sh file)
`heroku local -e .env`
- setting environment variables on heroky, with heroku toolbelt cli: 
`heroku config:set DEBUG=True --remote staging`  
`heroku config:set DEBUG=False --remote pro`  

