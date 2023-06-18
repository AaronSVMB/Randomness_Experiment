from otree.api import *
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'CPRAdditive'
    PLAYERS_PER_GROUP = 4  # CPR are usually larger groups, but this keeps it symmetric to our PGGs
    NUM_ROUNDS = 20
    ENDOWMENT = cu(10)  # Param Change
    alpha = 6  # Change params for this since group size is diff
    beta = 0.0125  # Param Change
    additive_shock_value = cu(5)  # decide on adequate shock value later


class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:
            Subsession.group_randomly(fixed_id_in_group=True)
        else:
            self.group_like_round(1)


class Group(BaseGroup):
    total_investment = models.CurrencyField()
    additive_shock = models.CurrencyField


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

    # In-person Passcode
    password_to_start = models.StringField()

    # Decision Variables
    investment = models.CurrencyField(
        min=0, max=C.ENDOWMENT, label="How much will you invest to Your Group's Joint Account?"
    )
    personal_account = models.CurrencyField()

    # For payoff Calculation and history table display
    common_pool_earnings = models.CurrencyField()

    # For the shock / adjustment
    additive_shock_realized = models.CurrencyField()

# Functions


def set_payoffs(group: Group):
    players = group.get_players()
    investments = [p.investment for p in players]
    group.total_investment = sum(investments)
    if random.random() <= 0.5:
        group.additive_shock = C.additive_shock_value
    else:
        group.additive_shock = -C.additive_shock_value
    for p in players:
        p.common_pool_earnings = (C.alpha - (C.beta * group.total_investment)) * p.investment
        p.personal_account = C.ENDOWMENT - p.investment
        p.additive_shock_realized = group.additive_shock
        p.payoff = p.personal_account + p.common_pool_earnings + group.additive_shock


# PAGES

class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class ComprehensionQuestions(Page):
    form_model = 'player'
    form_fields = ['comprehension_question_one', 'comprehension_question_two', 'comprehension_question_three']

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


class InPersonPassword(Page):
    form_model = 'player'
    form_fields = ['password_to_start']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    def error_message(player: Player, values):
        if values['password_to_start'] != 'experiment':
            return 'Check your spelling or ask the experimenter for assistance'


class PasswordWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Invest(Page):
    form_model = 'player'
    form_fields = ['investment']

    @staticmethod
    def vars_for_template(player: Player):
        # Get the player's history up to the current round
        previous_rounds = player.in_previous_rounds()

        # Extract investment and payoff for each round
        history = [
            {
                'round_number': p.round_number,
                'investment': p.investment,
                'personal_account': p.personal_account,
                'common_pool_earnings': p.common_pool_earnings,
                'payoff': p.payoff,
                'additive_shock_realized': p.additive_shock_realized
            }
            for p in previous_rounds
        ]
        return {'history': history}


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


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
                 Invest,
                 ResultsWaitPage,
                 Results,
                 CumulativeResults]
