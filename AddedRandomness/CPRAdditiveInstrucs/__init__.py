from otree.api import *


doc = """
Instructions and Comprehension Questions for the Common-Pool Resources ADDITIVE Treatment
"""


class C(BaseConstants):
    NAME_IN_URL = 'CPRAdditiveInstrucs'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NUM_PERIODS_IN_APP = 20  # For Instructions to display
    ENDOWMENT = cu(10)  # Param Change
    alpha = 6  # Change params for this since group size is diff
    beta = 0.0125  # Param Change
    additive_shock_value = cu(5)  # decide on adequate shock value later


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Comprehension Questions
    comprehension_question_one = models.IntegerField(label="If you invest X points into your Group's Joint Account, how"
                                                           " many points do you automatically invest in your "
                                                           "Personal Account?")
    comprehension_question_two = models.IntegerField(label="If you invest Y into your Group's Joint Account, what is "
                                                           "your profit from your Personal Account?")
    comprehension_question_three = models.IntegerField(label="If you invest Z into your Group's Joint account, and the "
                                                             "other three participants invest a total of W points into "
                                                             "the Group's Joint Account and the adjustment produces a"
                                                             " value of +5, what is your TOTAL profit?")


# PAGES


class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class ComprehensionQuestions(Page):
    form_model = 'player'
    form_fields = ['comprehension_question_one', 'comprehension_question_two', 'comprehension_question_three']
    timeout_seconds = 240

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player: Player, values):
        if values['comprehension_question_one'] != 2:
            return 'Reconsider your answer to question one'
        if values['comprehension_question_two'] != 2:
            return 'Reconsider your answer to question two'
        if values['comprehension_question_three'] != 2:
            return 'Reconsider your answer to question three'


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Instructions,
                 ComprehensionQuestions,
                 Results,
                 ResultsWaitPage]
