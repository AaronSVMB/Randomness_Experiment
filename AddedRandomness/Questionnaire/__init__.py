from otree.api import *


doc = """
Questionnaire for the end of the randomness / high variance experimental session
"""


class C(BaseConstants):
    NAME_IN_URL = 'Questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    password_to_start = models.StringField()

    gender = models.IntegerField(
        choices=[
            [1, 'Female'],
            [2, 'Male'],
            [3, "Prefer not to Answer"]
        ],
        label='What is your gender?'
    )

    age = models.IntegerField(label='How old are you?')

    major = models.StringField(label='What is your major?')

    # Decision-making style
    facts_and_logic = models.IntegerField(label='When making important decisions I focus on facts and logic',
                                          choices=[
                                            [1, "Always"],
                                            [2, "Never"]
                                        ], widget=widgets.RadioSelectHorizontal
                                          )
    feelings_and_intuition = models.IntegerField(choices=[
        [1, "Always"],
        [2, "Never"]
    ],
        label='When making important decisions I trust my feelings and intuition',
        widget=widgets.RadioSelectHorizontal)
    religious_and_spiritual = models.IntegerField(choices=[
        [1, "Always"],
        [2, "Never"]
    ],
        label='when making important decisions I consult with religious or spiritual leaders',
        widget=widgets.RadioSelectHorizontal)

    # How strongly do you agree or disagree with the following statements

    spirits = models.IntegerField(
        choices=[
            [1, 'Strongly Disagree'],
            [2, 'Disagree'],
            [3, 'Neutral'],
            [4, 'Agree'],
            [5, 'Strongly Agree'],
        ],
        widget=widgets.RadioSelectHorizontal,
        label='Some places really are haunted by spirits'
    )
    healing = models.IntegerField(
        choices=[
            [1, 'Strongly Disagree'],
            [2, 'Disagree'],
            [3, 'Neutral'],
            [4, 'Agree'],
            [5, 'Strongly Agree'],
        ],
        widget=widgets.RadioSelectHorizontal,
        label='Some people can use the power of their minds to heal other people'
    )
    fortunetelling = models.IntegerField(
        choices=[
            [1, 'Strongly Disagree'],
            [2, 'Disagree'],
            [3, 'Neutral'],
            [4, 'Agree'],
            [5, 'Strongly Agree'],
        ],
        widget=widgets.RadioSelectHorizontal,
        label='some people can use the power of their minds to "see" into the future'
    )
    spiritual_person = models.IntegerField(choices=[
            [1, 'Very Spiritual'],
            [2, 'Somewhat Spiritual'],
            [3, 'Not at all spiritual'],
        ],
        widget=widgets.RadioSelectHorizontal,
        label='Would you describe yourself as a "spiritual" person?')
    religious_person = models.IntegerField(choices=[
        [1, 'Very Religious'],
        [2, 'Somewhat Religious'],
        [3, 'Not at all Religious'],
    ],
        widget=widgets.RadioSelectHorizontal,
        label='Would you describe yourself as a "religious" person?')

    religious_affiliation = models.IntegerField(choices=[
        [1, "Christian"],
        [2, "Jewish"],
        [3, "Muslim"],
        [4, "Buddhist"],
        [5, "Hindu"],
        [6, "Other"],
        [7, "No religion"]
    ],
        widget=widgets.RadioSelectHorizontal,
        label='Which of the following best describes your current religion?')

    attend_services = models.IntegerField(choices=[
        [1, "Almost every week"],
        [2, "About two or three times per month"],
        [3, "About once each month"],
        [4, "Several times each year"],
        [5, "Once or twice each year"],
        [6, "Never or almost never"],
    ],
        label='In the past year, about how often have you attended religious services?')

    attend_services_young = models.IntegerField(choices=[
        [1, "Almost every week"],
        [2, "About two or three times per month"],
        [3, "About once each month"],
        [4, "Several times each year"],
        [5, "Once or twice each year"],
        [6, "Never or almost never"],
    ],
        label='When you were growing up, around age 11 or 12, how often did you attend religious services?')

    clarity = models.IntegerField(choices=[
        [1, "Strongly Disagree"],
        [2, "Disagree"],
        [3, "Agree"],
        [4, "Strongly Agree"]
    ])

    suggestions = models.LongStringField(label='Thank you for completing this experiment. We value your feedback, so please'
                                               ' use the following text box for comments or suggestions. ')







# PAGES
class ThankYou(Page):
    form_model = 'player'
    form_fields = ['password_to_start']

    def error_message(player: Player, values):
        if values['password_to_start'] != 'Questionnaire':
            return 'Check your spelling or ask the experimenter for help'


class Survey(Page):
    form_model = 'player'
    form_fields = ['gender', 'age', 'major',
                   'facts_and_logic', 'feelings_and_intuition', 'religious_and_spiritual',
                   'spirits', 'healing', 'fortunetelling', 'spiritual_person',
                   'religious_person', 'religious_affiliation', 'attend_services',
                   'attend_services_young', 'clarity', 'suggestions']


class ResultsWaitPage(WaitPage):
    pass


class EndPage(Page):
    pass


page_sequence = [ThankYou,
                 Survey,
                 EndPage]
