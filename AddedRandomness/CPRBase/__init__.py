from otree.api import *

doc = """
Standard Common Pool Resources Game played for multiple rounds. Comes from Ostrom, Gardner, and Walker (1993)
"""


class C(BaseConstants):
    NAME_IN_URL = 'CPRBase'
    PLAYERS_PER_GROUP = 4  # CPR are usually larger groups, but this keeps it symmetric to our PGGs
    NUM_ROUNDS = 20
    ENDOWMENT = cu(10)  # Param Change
    alpha = 6  # Change params for this since group size is diff
    beta = 0.0125  # Param Change


class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:
            Subsession.group_randomly(fixed_id_in_group=True)
        else:
            self.group_like_round(1)


class Group(BaseGroup):
    total_investment = models.CurrencyField()


class Player(BasePlayer):
    # Decision Variables
    investment = models.CurrencyField(
        min=0, max=C.ENDOWMENT, label="How much will you invest to Your Group's Joint Account?"
    )
    personal_account = models.CurrencyField()

    # For payoff Calculation and history table display
    common_pool_earnings = models.CurrencyField()

# Functions


def set_payoffs(group: Group):
    players = group.get_players()
    investments = [p.investment for p in players]
    group.total_investment = sum(investments)
    for p in players:
        p.common_pool_earnings = (C.alpha - (C.beta * group.total_investment)) * p.investment
        p.personal_account = C.ENDOWMENT - p.investment
        p.payoff = p.personal_account + p.common_pool_earnings


# PAGES
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
                'payoff': p.payoff
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


page_sequence = [Invest,
                 ResultsWaitPage,
                 Results,
                 CumulativeResults]
