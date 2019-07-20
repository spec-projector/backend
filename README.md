# spec-projector

# Gitlab OAuth

* Create application: https://gitlab.com/

User Settings -> Applications

1) Add Name
2) Add Redirect URI:

https://specprojector.com/api/complete/gitlab

https://specprojector.com/login

* Set project variables from created application:

`SOCIAL_AUTH_GITLAB_KEY` - "Application ID"

`SOCIAL_AUTH_GITLAB_SECRET` - "Secret"

`SOCIAL_AUTH_GITLAB_REDIRECT_URI` - 'https://specprojector.com/login'

* Login: https://specprojector.com/api/login/gitlab/