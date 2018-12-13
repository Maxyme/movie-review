### movie-review
A simple way to share movie recommendations with friends and family

### checking the webapp:
https://movie-review-staging.herokuapp.com/
https://movie-review-pro.herokuapp.com/

## running the backend
`flask run` and in a separate terminal `python worker.py`

### setting the correct config
`export APP_SETTINGS="config.DevelopmentConfig"`  
`APP_SETTINGS="config.DevelopmentConfig" python app.py`

- on heroku, with heroku toolbelt cli:  
`heroku config:set APP_SETTINGS=config.StagingConfig --remote staging`  
`heroku config:set APP_SETTINGS=config.ProductionConfig --remote pro`  

### setting up heroku (do twice for staging)
`heroku create movie-review-pro`  
`git remote add pro git@heroku.com:movie-review-pro.git`

### deploying to heroku
- staging: `git push staging master`  
- production: `git push pro master`

### run on heroku server
`heroku run python app.py --app movie-review-staging`

### setting up the local postgres db and local redis
`docker-compose up -d`

### making migrations
- flask cli will automatically read the .flaskenv file if python-dotnet is installed and add source it.
`flask db init`

### make the migrations and migrate into the db
`flask db migrate`
`flask db upgrade`

### heroku
- checking the config (env variables):  
`heroku config --app movie-review-staging`
- adding a postgres db:  
`heroku addons:create heroku-postgresql:hobby-dev --app movie-review-staging`
- adding a redis instance on heroku
`heroku addons:create redistogo:nano --app movie-review-staging`
- run the migrations on heroku:  
`heroku run python manage.py db upgrade --app movie-review-staging`
- run locally with environment file (loads the heroku.sh file)
`heroku local -e development.env`

