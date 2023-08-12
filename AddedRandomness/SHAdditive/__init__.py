from otree.api import *
import random


doc = """
Stag Hunt Game with Additive Shocks 
"""


class C(BaseConstants):
    NAME_IN_URL = 'SHAdditive'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    payoff_both_stag = cu(10)  # pick parameters later
    payoff_both_hare = cu(5)
    payoff_stag_hare_high = cu(8)
    payoff_stag_hare_low = cu(1)
    additive_shock_value = cu(5)


class Subsession(BaseSubsession):

    def creating_session(subsession):
        if subsession.round_number == 1:
            subsession.group_randomly(fixed_id_in_group=True)
        else:
            subsession.group_like_round(1)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
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
    additive_shock_realized = models.CurrencyField()


# PAGES
class Decision(Page):
    form_model = 'player'
    form_fields = ['cooperate']


class ResultsWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        players_list = group.get_players()
        player_1 = players_list[0]
        player_2 = players_list[1]

        # Save the choice of their partner
        player_1.partner_choice = player_2.cooperate
        player_2.partner_choice = player_1.cooperate

        if player_1.cooperate:
            if player_2.cooperate:
                player_1.payoff = C.payoff_both_stag
                player_2.payoff = C.payoff_both_stag
            else:
                player_1.payoff = C.payoff_stag_hare_low
                player_2.payoff = C.payoff_stag_hare_high
        else:
            if player_2.cooperate:
                player_1.payoff = C.payoff_stag_hare_high
                player_2.payoff = C.payoff_stag_hare_low
            else:
                player_1.payoff = C.payoff_both_hare
                player_2.payoff = C.payoff_both_hare

        # Additive Shock
        if random.random() <= 0.5:
            player_1.payoff -= C.additive_shock_value
            player_1.additive_shock_realized = -5
            player_2.payoff -= C.additive_shock_value
            player_2.additive_shock_realized = -5
        else:
            player_1.payoff += C.additive_shock_value
            player_1.additive_shock_realized = 5
            player_2.payoff += C.additive_shock_value
            player_2.additive_shock_realized = 5


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


page_sequence = [Decision,
                 ResultsWaitPage,
                 Results,
                 CumulativeResults]
