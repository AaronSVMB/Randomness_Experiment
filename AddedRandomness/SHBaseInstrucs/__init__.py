from otree.api import *


doc = """
Instrucs and CompQs for the Stag Hunt Base Game 
"""


class C(BaseConstants):
    NAME_IN_URL = 'SHBaseInstrucs'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NUM_PERIODS_IN_APP = 3
    payoff_both_stag = cu(10)  # pick parameters later
    payoff_both_hare = cu(5)
    payoff_stag_hare_high = cu(8)
    payoff_stag_hare_low = cu(1)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Comprehension Questions
    comprehension_question_one = models.IntegerField(
        choices=[
            [1, 'True'],
            [2, 'False'],
        ], label="True or False"
    )
    comprehension_question_two_a = models.IntegerField()
    comprehension_question_two_b = models.IntegerField()
    comprehension_question_three_a = models.IntegerField()
    comprehension_question_three_b = models.IntegerField()


# PAGES
class Instructions(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class ComprehensionQuestions(Page):
    form_model = 'player'
    form_fields = ['comprehension_question_one', 'comprehension_question_two_a',
                   'comprehension_question_two_b', 'comprehension_question_three_a',
                   'comprehension_question_three_b']
    timeout_seconds = 300

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player: Player, values):
        if values['comprehension_question_one'] != 1:
            return 'Reconsider your answer to question one'
        if values['comprehension_question_two_a'] != 10:
            return 'Reconsider your answer to question two b'
        if values['comprehension_question_two_b'] != 10:
            return 'Reconsider your answer to question two a'
        if values['comprehension_question_three_a'] != 1:
            return 'Reconsider your answer to question three a'
        if values['comprehension_question_three_b'] != 8:
            return 'Reconsider your answer to question three b'



class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Instructions,
                 ComprehensionQuestions,
                 Results,
                 ResultsWaitPage]
