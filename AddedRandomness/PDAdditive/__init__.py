import random

from otree.api import *


doc = """
Prisoner's Dilemma with Additive Shocks to the payoff
"""


class C(BaseConstants):
    NAME_IN_URL = 'PDAdditive'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    payoff_both_cooperate = cu(12)
    payoff_both_defect = cu(10)
    payoff_cooperate_defect_high = cu(16)
    payoff_cooperate_defect_low = cu(6)
    additive_shock_value = cu(5)



class Subsession(BaseSubsession):

    def creating_session(subsession):
        if subsession.round_number == 1:
            subsession.group_randomly(fixed_id_in_group=True)
        else:
            subsession.group_like_round(1)


class Group(BaseGroup):
    additive_shock_realized = models.CurrencyField()


class Player(BasePlayer):
    defect = models.BooleanField(
        label="Please choose if you want to cooperate or defect",
        choices=[
            [True, "Defect"],
            [False, "Cooperate"]
        ]
    )


# PAGES


class Instructions(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Decision(Page):
    form_model = 'player'
    form_fields = ['defect']


class ResultsWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        player_lists = group.get_players()
        player_1 = player_lists[0]
        player_2 = player_lists[1]
        if player_1.defect:
            if player_2.defect:
                player_1.payoff = C.payoff_both_defect
                player_2.payoff = C.payoff_both_defect
            else:
                player_1.payoff = C.payoff_cooperate_defect_high
                player_2.payoff = C.payoff_cooperate_defect_low
        else:
            if player_2.defect:
                player_1.payoff = C.payoff_cooperate_defect_low
                player_2.payoff = C.payoff_cooperate_defect_high
            else:
                player_1.payoff = C.payoff_both_cooperate
                player_2.payoff = C.payoff_both_cooperate

        # Additive Shock
        if random.random() <= 0.5:
            player_1.payoff -= C.additive_shock_value
            player_2.payoff -= C.additive_shock_value
        else:
            player_1.payoff += C.additive_shock_value
            player_2.payoff += C.additive_shock_value


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
                 Decision,
                 ResultsWaitPage,
                 Results,
                 CumulativeResults]
