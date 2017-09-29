heroku login
git init
heroku git:remote -a fiuberappserver
heroku container:login
heroku container:push web