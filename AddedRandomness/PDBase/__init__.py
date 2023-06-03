from otree.api import *


doc = """
Prisoner's Dilemma base game version
"""


class C(BaseConstants):
    NAME_IN_URL = 'PDBase'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    payoff_both_cooperate = cu(12)
    payoff_both_defect = cu(10)
    payoff_cooperate_defect_high = cu(16)
    payoff_cooperate_defect_low = cu(6)


class Subsession(BaseSubsession):

    def creating_session(subsession):
        if subsession.round_number == 1:
            subsession.group_randomly(fixed_id_in_group=True)
        else:
            subsession.group_like_round(1)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Password to Start
    password = models.StringField()

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

    cooperate = models.BooleanField(
        label="Please select your move: Left or Right",
        choices=[
            [True, "Left"],
            [False, "Right"]
        ]
    )
    partner_choice = models.BooleanField(
        choices=[
            [True, "Left"],
            [False, "Right"],
        ]
    )


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

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player: Player, values):
        if values['comprehension_question_one'] != 1:
            return 'Reconsider your answer to question one'
        if values['comprehension_question_two_a'] != 12:
            return 'Reconsider your answer to question two b'
        if values['comprehension_question_two_b'] != 12:
            return 'Reconsider your answer to question two a'
        if values['comprehension_question_three_a'] != 6:
            return 'Reconsider your answer to question three a'
        if values['comprehension_question_three_b'] != 16:
            return 'Reconsider your answer to question three b'


class InPersonPassword(Page):
    form_model = 'player'
    form_fields = ['password']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player: Player, values):
        if values['password'] != 'GoodLuck':
            return 'Please check your spelling or ask the experimenter for assistance'


class PasswordWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Decision(Page):
    form_model = 'player'
    form_fields = ['cooperate']


class ResultsWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        player_lists = group.get_players()
        player_1 = player_lists[0]
        player_2 = player_lists[1]

        # Save the choice of their partner
        player_1.partner_choice = player_2.cooperate
        player_2.partner_choice = player_1.cooperate

        if player_1.cooperate:
            if player_2.cooperate:
                player_1.payoff = C.payoff_both_cooperate
                player_2.payoff = C.payoff_both_cooperate
            else:
                player_1.payoff = C.payoff_cooperate_defect_low
                player_2.payoff = C.payoff_cooperate_defect_high
        else:
            if player_2.cooperate:
                player_1.payoff = C.payoff_cooperate_defect_high
                player_2.payoff = C.payoff_cooperate_defect_low
            else:
                player_1.payoff = C.payoff_both_defect
                player_2.payoff = C.payoff_both_defect


class Results(Page):
    def vars_for_template(player: Player):
        if player.cooperate:
            if player.partner_choice:
                return {
                    'choice': 'Left',
                    'partners_choice': 'Left'
                }
            else:
                return {
                    'choice': 'Left',
                    'partners_choice': 'Right'
                }
        else:
            if player.partner_choice:
                return {
                    'choice': 'Right',
                    'partners_choice': 'Left'
                }
            else:
                return {
                    'choice': 'Right',
                    'partners_choice': 'Right'
                }


class CumulativeResults(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        cumulative_payoff = sum([p.payoff for p in player.in_all_rounds() if p.payoff])

        return {'cumulative_payoff': cumulative_payoff}


page_sequence = [Instructions,
                 ComprehensionQuestions,
                 InPersonPassword,
                 PasswordWaitPage,
                 Decision,
                 ResultsWaitPage,
                 Results,
                 CumulativeResults]
