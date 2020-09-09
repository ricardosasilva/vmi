"""
Django settings for vmi (Verify My Identity) project.
Copyright Videntity Systems Inc.


For more information on this file, see
https://docs.djangoproject.com/en/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import datetime
import dj_database_url
from django.contrib.messages import constants as messages
from getenv import env
from .utils import bool_env
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    'SECRET_KEY', '@+tmixefm9-bu1eknb4k^5dj(f2z0^97c$zan9akdr^4s8cc55')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool_env(env('DEBUG', True))

if DEBUG:
    # Never run a production system in DEBUG or with insecure transport turned
    # off (i.e. http instead of https)
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrapform',
    'social_django',
    'phonenumber_field',
    'oauth2_provider',
    'rest_framework',
    'django_filters',
    'apps.oidc',
    'apps.home',
    'apps.reports',
    'apps.accounts',
    'apps.ial',
    'apps.fido',
    'apps.dynamicreg',
    'apps.mfa.backends.sms',
    'apps.api',
    'apps.testclient',
    # 'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'apps.mfa.middleware.DeviceVerificationMiddleware',
    'apps.mfa.middleware.AssertDeviceVerificationMiddleware',
    'apps.oidc.error_handlers.AuthenticationRequiredExceptionMiddleware',
    'apps.oidc.error_handlers.OIDCNoPromptMiddleware',
]


AUTHENTICATION_BACKENDS = (
    # 'social_core.backends.google_openidconnect.GoogleOpenIdConnect',
    'django.contrib.auth.backends.ModelBackend',
    'apps.accounts.authentication_backends.EmailBackend',
    'apps.accounts.authentication_backends.SubjectBackend',
    # apps.accounts.ldap_auth_backends.LDAPBackend',
)


SOCIAL_AUTH_GOOGLE_URL = env(
    "SOCIAL_AUTH_GOOGLE_URL", 'https://accounts.google.com')
SOCIAL_AUTH_GOOGLE_OIDC_ENDPOINT = env(
    "SOCIAL_AUTH_GOOGLE_OIDC_ENDPOINT", 'https://accounts.google.com')

SOCIAL_AUTH_GOOGLE_OPENIDCONNECT_KEY = env(
    'SOCIAL_AUTH_GOOGLE_OPENIDCONNECT_KEY', '')
SOCIAL_AUTH_GOOGLE_OPENIDCONNECT_SECRET = env(
    'SOCIAL_AUTH_GOOGLE_OPENIDCONNECT_SECRET', '')
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'


VERIFICATION_BACKENDS = [
    'apps.fido.auth.backends.FIDO2Backend',
    'apps.mfa.backends.sms.backend.SMSBackend',
]

SMS_CODE_CHARSET = "1234567890"

ROOT_URLCONF = 'vmi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_settings_export.settings_export',
            ],
        },
    },
]


WSGI_APPLICATION = 'vmi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASES_CUSTOM',
                    'sqlite:///{}/db/db.sqlite3'.format(BASE_DIR))),
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AWS_STORAGE_BUCKET_NAME = env(
    "AWS_STORAGE_BUCKET_NAME", "development-vmi-media-storage")
AWS_AUTO_CREATE_BUCKET = True
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False
DEFAULT_FILE_STORAGE = env("DEFAULT_FILE_STORAGE",
                           'django.core.files.storage.FileSystemStorage')
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# MEDIA_URL = 'http://localhost:8000/media/'
MEDIA_URL = '/media/'

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'sitestatic'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static-assets"),
]

ATOMIC_REQUESTS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

# OAUTH SETTINGS
OAUTH2_PROVIDER = {
    'SCOPES': {'openid': 'open id connect access'},
    'DEFAULT_SCOPES': ['openid'],

    'OAUTH2_VALIDATOR_CLASS': 'vmi.oauth2_validators.SingleAccessTokenValidator',
    'OAUTH2_SERVER_CLASS': 'apps.oidc.server.Server',
    'REQUEST_APPROVAL_PROMPT': 'auto',
    'ACCESS_TOKEN_EXPIRE_SECONDS':  int(env('ACCESS_TOKEN_EXPIRE_SECONDS', 315360000))
}
OAUTH2_PROVIDER_GRANT_MODEL = 'oidc.Grant'
OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL = 'oauth2_provider.AccessToken'
OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'

OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL = 'oauth2_provider.RefreshToken'
OAUTH2_PROVIDER_ALLOWED_GRANT_TYPES = (
    "authorization_code",
    # "password",
    # "client_credentials",
    "refresh_token",
)
OAUTH2_PROVIDER_ALLOWED_RESPONSE_TYPES = (
    # "token",
    "code",
)
OIDC_PROVIDER = {
    # 'OIDC_ISSUER': 'http://localhost:8000',
    'OIDC_BASE_CLAIM_PROVIDER_CLASS': 'apps.oidc.claims.ClaimProvider',
    'OIDC_CLAIM_PROVIDERS': [
        # Mandatory
        'apps.oidc.claims.UserClaimProvider',

        # Optional
        # The UserProfileClaimProvider currently gets all claims non repeating
        # claims.
        'apps.accounts.claims.UserProfileClaimProvider',

        # Include address
        'apps.accounts.claims.AddressClaimProvider',

        # Include document (identifiers) claim
        'apps.accounts.claims.IdentifierClaimProvider',
        # Include this Member is in a part for Organizations 0..n
        'apps.accounts.claims.MemberToOrganizationClaimProvider',
        # Include this Agent is part of 0..n Organizations
        'apps.accounts.claims.AgentToOrganizationClaimProvider',

        # Identity Assurance for OIDC
        'apps.accounts.claims.VerifiedPersonDataClaimProvider',
        # 'apps.accounts.claims.SubjectClaimProvider',
        # 'apps.accounts.claims.EmailVerifiedClaimProvider',
        # 'apps.accounts.claims.PhoneNumberClaimProvider',
        # 'apps.accounts.claims.IdentityAssuranceLevelClaimProvider',
        # 'apps.accounts.claims.AuthenticatorAssuranceLevelClaimProvider',
        # 'apps.accounts.claims.VectorsOfTrustClaimProvider',
        'apps.fido.claims.AuthenticatorAssuranceProvider',
        'apps.mfa.backends.sms.claims.AuthenticatorAssuranceProvider',
    ],
}

# Adding to allow other modes of SMS text delivery in the future.
SMS_STRATEGY = env('SMS_STRATEGY', 'AWS-SNS')  # AWS-SNS or TWILIO

# If Using TWILIO, set these credentials

TWILIO_ACCOUNT_SID = env('TWILIO_ACCOUNT_SID',
                         'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
TWILIO_TOKEN = env('TWILIO_TOKEN', 'your_auth_token')
# Use your twilio number.
TWILIO_FROM_NUMBER = env('TWILIO_FROM_NUMBER', "+15555555555")


# Add a prefix to the luhn checkdigit calculation.
# This can help identify genuine subject ids and indicate provenance.
SUBJECT_LUHN_PREFIX = env('SUBJECT_LUHN_PREFIX', '')
APPLICATION_TITLE = env('APPLICATION_TITLE', "Verify My Identity")
KILLER_APP_TITLE = env('KILLER_APP_TITLE', 'Your Application Here')
KILLER_APP_URI = env('KILLER_APP_URI', 'http://localhost:8002')

TOP_LEFT_TITLE = env('TOP_LEFT_TITLE', 'verify my identity')
PARTNER_REF = env('PARTNER_REF', '')  # a subtitle

ORGANIZATION_TITLE = env(
    'DJANGO_ORGANIZATION_TITLE',
    'Videntity')
ORGANIZATION_URI = env('DJANGO_ORGANIZATION_URI',
                       'https://videntity.com')
POLICY_URI = env('DJANGO_POLICY_URI',
                 'https://static.verifymyidentity.com/privacy-policy-1.0.html')
POLICY_TITLE = env('DJANGO_POLICY_TITLE', 'Privacy Policy')
TOS_URI = env('DJANGO_TOS_URI',
              'https://static.verifymyidentity.com/terms-of-service-1.0.html')
AGENT_TOS_URI = env('DJANGO_AGENT_TOS_URI',
                    'https://static.verifymyidentity.com/agent-terms-of-service-1.0.html')

TOS_TITLE = env('DJANGO_TOS_TITLE', 'Terms of Service')

# If True, display the training attestation on agent signup.
REQUIRE_TRAINING_FOR_AGENT_SIGNUP = bool_env(
    env('REQUIRE_TRAINING_FOR_AGENT_SIGNUP', False))
TRAINING_URI = env('TRAINING_URI',
                   'https://static.verifymyidentity.com/training-1.0.html')
TOS_TITLE = env('DJANGO_TOS_TITLE', 'Terms of Service')
USER_DOCS_URI = "https://github.com/videntity/vmi"
USER_DOCS_TITLE = "User Documentation"
USER_DOCS = "User Docs"

# LINKS TO DOCS
DEVELOPER_DOCS_URI = "https://github.com/videntity/vmi"
DEVELOPER_DOCS = "Developer Docs"
DEFAULT_DISCLOSURE_TEXT = """
    Verify My Identity  provides standards-based identity verification,
    digital credentials, and single sign-on services for people and
    organizations. Unauthorized or improper use of this system or
    its data may result in disciplinary action, as well as civil
    and criminal penalties. This system may be monitored, recorded,
    and subject to audit.
    """

DISCLOSURE_TEXT = env('DJANGO_PRIVACY_POLICY_URI', DEFAULT_DISCLOSURE_TEXT)

HOSTNAME_URL = env('HOSTNAME_URL', 'http://localhost:8000')

ORG_SIGNUP_CONTACT = env('ORG_SIGNUP_CONTACT',
                         'https://videntity.com/contact-us/')

# Allow Members to create accounts
ALLOW_MEMBER_SIGNUP = bool_env(env('ALLOW_MEMBER_SIGNUP', False))

CONTACT_EMAIL = env('DJANGO_CONTACT_EMAIL', 'sales@videntity.com')

SETTINGS_EXPORT = [
    'DEBUG',
    'CONTACT_EMAIL',
    'ALLOWED_HOSTS',
    'APPLICATION_TITLE',
    'STATIC_URL',
    'STATIC_ROOT',
    'DEVELOPER_DOCS_URI',
    'ORGANIZATION_TITLE',
    'POLICY_URI',
    'POLICY_TITLE',
    'DISCLOSURE_TEXT',
    'TOS_URI',
    'TOS_TITLE',
    'USER_DOCS_URI',
    'USER_DOCS',
    'DEVELOPER_DOCS',
    'USER_DOCS_TITLE',
    'HOSTNAME_URL',
    'TOP_LEFT_TITLE',
    'KILLER_APP_URI',
    'KILLER_APP_TITLE',
    'ORG_SIGNUP_CONTACT',
    'ALLOW_MEMBER_SIGNUP',
    'PARTNER_REF',
    'PUBLIC_HOME_TEMPLATE',
]


# Emails ----------------------------------------------------------
# Verify My Identity REQUIRES A WORKING OUTBOUND EMAIL AND SMS SERVICE TO
# FUNCTION!
DEFAULT_FROM_EMAIL = env('FROM_EMAIL', 'no-reply@example.com')
DEFAULT_ADMIN_EMAIL = env('ADMIN_EMAIL',
                          'no-reply@example.com')

# Select the right Email delivery system that works for you.
# Django's default is 'django.core.mail.backends.smtp.EmailBackend'. This will work with most
# email systems including Sendgrid. Sendgrid is the new default and will work with Azure.
# Set email settings according to your own configuration in your .env file.
# Use SMTP Backend for SendGrid, Sendmail or other SMTP.  SMTP may also be used for AWS SES.
# You can use 'django.core.mail.backends.console.EmailBackend' to send
# emails to stdout instead of sending them. This is good for a local dev setup.
# If using the AWS Simple Email Service (SES) you may also use,
# 'django_ses.SESBackend'. You only need the settings for for AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY ,
# and AWS_DEFAULT_REGION set for this to work. Those should also be set in
# as environment variables.
EMAIL_SUBJECT_PREFIX = env('EMAIL_SUBJECT_PREFIX', '[VerifyMyIdentity] ')
EMAIL_BACKEND = env(
    'EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
SENDGRID_API_KEY = env('SENDGRID_API_KEY', 'Set this in your envvar')
# Use localhost for local dev. No needed for AWS SES
EMAIL_HOST = env('EMAIL_HOST', 'smtp.sendgrid.net')
# this is exactly the value 'apikey' (for Sendgrid.)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', 'apikey')
EMAIL_HOST_PASSWORD = env('SENDGRID_API_KEY', SENDGRID_API_KEY)
EMAIL_PORT = int(env('EMAIL_PORT', 587))
EMAIL_USE_TLS = True

# These emails settings are not used but provided as an envvars for
# compatibility/completeness.
EMAIL_PASSWORD = env('EMAIL_PASSWORD', '')
EMAIL_USE_LOCALTIME = bool_env(env('EMAIL_USE_LOCALTIME', False))
EMAIL_USE_TLS = bool_env(env('EMAIL_USE_TLS', False))
EMAIL_USE_SSL = bool_env(env('EMAIL_USE_SSL', False))
EMAIL_SSL_CERTFILE = env('EMAIL_SSL_CERTFILE', None)
EMAIL_SSL_KEYFILE = env('EMAIL_SSL_KEYFILE', None)


SIGNUP_TIMEOUT_DAYS = 3
ORGANIZATION_NAME = env('ORGANIZATION_NAME', "Verify My Identity")

# 4 MB Default
MAX_PROFILE_PICTURE_SIZE = env(
    'MAX_PROFILE_PICTURE_SIZE', str(4 * 1024 * 1024))

# Define individual identifier types
INDIVIDUAL_ID_TYPE_CHOICES = env('INDIVIDUAL_ID_TYPE_CHOICES', (
    ('PATIENT_ID_FHIR', 'Patient ID in FHIR'),
    ('MPI', 'Master Patient Index (Not FHIR Patient ID)'),
    ('SSN', 'Social Security Number'),
    ('MEDICAID_ID', 'Medicaid ID Number'),
    ('MEDICARE_HICN', 'Medicare HICN (Legacy)'),
    ('MEDICARE_ID', 'Medicare ID Number'),
    ('INSURANCE_ID', 'Insurance ID Number'),
    ('IHE_ID', 'Health Information Exchange ID'),
    ('NPI', 'National Provider Identifier'),
    ('UHI', 'Universal Health Identifier'),))


# Define organization identifier types
ORGANIZATION_ID_TYPE_CHOICES = env('ORGANIZATION_ID_TYPE_CHOICES', (
    ('FEIN', 'Federal Employer ID Number (Tax ID)'),
    ('NPI', 'National Provider Identifier'),
    ('OEID', 'Other Entity Identifier'),
    ('PECOS', 'PECOS Medicare ID'),))

DEFAULT_COUNTRY_CODE_FOR_INDIVIDUAL_IDENTIFIERS = env(
    'DEFAULT_COUNTRY_CODE_FOR_IDENTIFIERS', "US")

PHONENUMBER_DEFAULT_REGION = env('PHONENUMBER_DEFAULT_REGION', "US")

# Terms of service version
CURRENT_TOS_VERSION = env('CURRENT_TOS_VERSION', "1")

# Privacy Policy version
CURRENT_PP_VERSION = env('CURRENT_PP_VERSION', "1")

# Expire session on browser close.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Expire session. Default is 10 minutes: 10 * 60 seconds
SESSION_COOKIE_AGE = int(env('SESSION_COOKIE_AGE', int(30 * 60)))


# Whitelabeling.The next settings allow for homepage and login screen
# customization.

# Pick a login template and title.
LOGIN_TEMPLATE_PICKER = {"default": 'login.html',
                         'share-my-health': 'login.html',
                         # Add others here to create a custom login template.
                         }

# Whitelabel: Pick a public template. Customize to your needs.
PUBLIC_HOME_TEMPLATE = env('PUBLIC_HOME_TEMPLATE', "index.html")

# What a user sees when logged in.
AUTHENTICATED_HOME_TEMPLATE = env(
    'AUTHENTICATED_HOME_TEMPLATE', "authenticated-home.html")

# List of IAL2 classifications. You can define your own.  Anything that is not empty
# (e.g.  not "") will be an IAL2.""
IAL2_EVIDENCE_CLASSIFICATIONS = (
    # Generic
    ('ONE-SUPERIOR-OR-STRONG-PLUS',
     'One Superior or one Strong+ piece of identity evidence'),
    ('ONE-STRONG-TWO-FAIR', 'One Strong and Two Fair pieces of identity evidence'),
    ('TWO-STRONG', 'Two Pieces of Strong identity evidence'),

    # More specific
    ('ONE-SUPERIOR-OR-STRONG-PLUS-1', "Driver's License"),
    ('ONE-SUPERIOR-OR-STRONG-PLUS-2', "Identification Card"),
    ('ONE-SUPERIOR-OR-STRONG-PLUS-3', 'Veteran ID Card'),
    ('ONE-SUPERIOR-OR-STRONG-PLUS-4', 'Passport'),
    ('ONE-SUPERIOR-OR-STRONG-PLUS-5', 'RealID'),
    ('TWO-STRONG-1', 'Original Birth Certificate and a Social Security Card'),
    ('TRUSTED-REFEREE-VOUCH', 'I am a Trusted Referee Vouching for this person'),
)


# For creating agent users who have out of band _D verification on file.
AUTO_IAL_2_DEFAULT_CLASSIFICATION = 'ONE-SUPERIOR-OR-STRONG-PLUS',
AUTO_IAL_2_DEFAULT_SUBCLASSIFICATION = env(
    'AUTO_IAL_2_DEFAULT_SUBCLASSIFICATION', "OFFLINE")
AUTO_IAL_2_DESCRIPTION = env(
    'AUTO_IAL_2_DESCRIPTION', "Verified offline. Documents on file.")

LOGIN_RATELIMIT = env('LOGIN_RATELIMIT', '100/h')

# These are used to encrypt the passphrase. Change these for production
PASSPHRASE_SALT = env('PASSPHRASE_SALT', "FA6F747468657265616C706570706573")
PASSPHRASE_ITERATIONS = int(env('PASSPHRASE_ITERATIONS', "200"))


# These are added for portability to other cloud platforms.
# Note that instead these values can be passed as an IAM role.
# See
# https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', "set-your-own-id")
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', "set-your-own-key")
AWS_DEFAULT_REGION = env('AWS_DEFAULT_REGION', 'us-east-1')

# Set to True when using in a reverse proxy such as Gunicorn and Nginx
SOCIAL_AUTH_REDIRECT_IS_HTTPS = bool_env(
    env('SOCIAL_AUTH_REDIRECT_IS_HTTPS', False))

# Blank means skip EC2.
EC2PARAMSTORE_4_ENVIRONMENT_VARIABLES = env(
    'EC2PARAMSTORE_4_ENVIRONMENT_VARIABLES', "EC2_PARAMSTORE")

# Set an acceptable age range for birthdays, registering,

now = datetime.datetime.now()
MINIMUM_AGE = int(env('MINIMUM_AGE', '18'))
MINIMUM_BIRTH_YEAR = now.year - MINIMUM_AGE

BIRTHDATE_YEARS = [x for x in range(1900, MINIMUM_BIRTH_YEAR)]

ID_DOCUMENT_ISSUANCE_YEARS = [x for x in range(now.year - 20, now.year)]

# Set possible expiration for identity documents e.g. driver's license).
EXPIRY_DATE_ACCEPTABLE_YEARS = [x for x in range(now.year, 2050)]

# VECTORS_OF_TRUST_TRUSTMARK_URLfor value of `vtm` claim.
VECTORS_OF_TRUST_TRUSTMARK_URL = env('VECTORS_OF_TRUST_TRUSTMARK_URL',
                                     'https://github.com/TransparentHealth/800-63-3-trustmark/')

# ALLOW_MULTIPLE_USERS_PER_EMAIL should never be activated on a production
# system. It exists for debugging and testing.
ALLOW_MULTIPLE_USERS_PER_EMAIL = bool_env(
    env('ALLOW_MULTIPLE_USERS_PER_EMAIL', False))


# Use these settings to allow/disallow different ID verification modes.
ALLOW_PHYSICAL_INPERSON_PROOFING = bool_env(
    env('ALLOW_PHYSICAL_INPERSON_PROOFING', True))  # pipp
ALLOW_SUPERVISED_REMOTE_INPERSON_PROOFING = bool_env(
    env('ALLOW_PHYSICAL_INPERSON_PROOFING', True))  # sripp
ALLOW_ONLINE_VERIFICATION_OF_AN_ELECTRONIC_ID_CARD = bool_env(
    env('ALLOW_ONLINE_VERIFICATION_OF_AN_ELECTRONIC_ID_CARD', False))  # eid
DEFAULT_PROOFING_METHOD = env(
    'DEFAULT_PROOFING_METHOD', 'pipp')  # pipp, sripp, or eid
