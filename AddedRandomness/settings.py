from os import environ

SESSION_CONFIGS = [
    # dict(
    #     name='public_goods',
    #     app_sequence=['public_goods'],
    #     num_demo_participants=3,
    # ),
    dict(
        name='PDBase',
        display_name='PD',
        app_sequence=['PDBase'],
        num_demo_participants=2
    ),
    dict(
        name='PDAdditive',
        display_name='PDAdditive',
        app_sequence=['PDAdditive'],
        num_demo_participants=2
    ),
    dict(
        name='RiskElicitation',
        display_name='RiskElicitation',
        app_sequence=['RiskElicitation'],
        num_demo_participants=1

    ),
    dict(
        name='Questionnaire',
        display_name='Questionnaire',
        app_sequence=['Questionnaire'],
        num_demo_participants=1
    ),
    dict(
        name='SHBase',
        display_name='Stag Hunt Base',
        app_sequence=['SHBase'],
        num_demo_participants=2
    ),
    dict(
        name='SHAdditive',
        display_name='Stag Hunt Additive',
        app_sequence=['SHAdditive'],
        num_demo_participants=2
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=7.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '1061348711524'
