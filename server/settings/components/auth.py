AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'login'

AUTHENTICATION_BACKENDS = [
    'apps.core.gitlab.oauth2.CustomGitLabOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_USER_MODEL = 'users.User'
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_GITLAB_KEY = 'd6c59be32a74d6ad714ce67c941e0887a968f5dfd55bca31b16a82b7f0901571'
SOCIAL_AUTH_GITLAB_SECRET = 'c5acd4f1ce9ae4bc48d5d9010b195744ffecae69d7cc8d60837fcd20a014fe27'
SOCIAL_AUTH_GITLAB_REDIRECT_URI = 'http://127.0.0.1:8000/api/login/'