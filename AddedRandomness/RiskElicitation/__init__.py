from otree.api import *
import random
import numpy as np

doc = """
Holt Laury Risk Elicitation
"""


class C(BaseConstants):
    NAME_IN_URL = 'RiskElicitation'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    LOTTERY_A_LOW = cu(1)  # 1 dollar with current conversion
    LOTTERY_A_HIGH = cu(3)  # 3 dollars with current conversion
    LOTTERY_B_LOW = cu(.1)  # 10 cents with current conversion
    LOTTERY_B_HIGH = cu(5)  # 5 dollars with current conversion


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


# Functions

def make_lottery_option(label):
    return models.IntegerField(
        label=label,
        choices=[
            [1, 'A'],
            [2, 'B']
        ],
        widget=widgets.RadioSelectHorizontal
    )


class Player(BasePlayer):
    lottery_b_one = make_lottery_option("$0.1 with probability 9/10 or $5 with probability 1/10")
    lottery_b_two = make_lottery_option("$0.1 with probability 8/10 or $5 with probability 2/10")
    lottery_b_three = make_lottery_option("$0.1 with probability 7/10 or $5 with probability 3/10")
    lottery_b_four = make_lottery_option("$0.1 with probability 6/10 or $5 with probability 4/10")
    lottery_b_five = make_lottery_option("$0.1 with probability 5/10 or $5 with probability 5/10")
    lottery_b_six = make_lottery_option("$0.1 with probability 4/10 or $5 with probability 6/10")
    lottery_b_seven = make_lottery_option("$0.1 with probability 3/10 or $5 with probability 7/10")
    lottery_b_eight = make_lottery_option("$0.1 with probability 2/10 or $5 with probability 8/10")
    lottery_b_nine = make_lottery_option("$0.1 with probability 1/10 or $5 with probability 9/10")
    lottery_b_ten = make_lottery_option("$0.1 with probability 0/10 or $5 with probability 10/10")

    chosen_lottery = models.IntegerField()
    relevant_choice = models.IntegerField()
    relevant_choice_as_string = models.StringField()


# Functions for Payoff

def make_lottery_b_dictionary(player: Player):
    lottery_b_dictionary = {
        1: player.lottery_b_one,
        2: player.lottery_b_two,
        3: player.lottery_b_three,
        4: player.lottery_b_four,
        5: player.lottery_b_five,
        6: player.lottery_b_six,
        7: player.lottery_b_seven,
        8: player.lottery_b_eight,
        9: player.lottery_b_nine,
        10: player.lottery_b_ten
    }
    return lottery_b_dictionary


def calc_payoffs(subsession: Subsession):
    players = subsession.get_players()
    for p in players:
        lottery_b_dict = make_lottery_b_dictionary(p)
        lottery_ids = [i + 1 for i in range(len(lottery_b_dict))]
        salient_lottery = random.choice(lottery_ids)
        p.chosen_lottery = salient_lottery
        relevant_decision = lottery_b_dict[salient_lottery]
        p.relevant_choice = relevant_decision
        # store the choice as A or B to be displayed to subjects
        if relevant_decision == 1:
            p.relevant_choice_as_string = 'A'
        else:
            p.relevant_choice_as_string = 'B'
        # Calc payoff via random draw
        if relevant_decision == 1:
            if np.random.rand() < 1 / 2:
                p.payoff = C.LOTTERY_A_LOW
            else:
                p.payoff = C.LOTTERY_A_HIGH
        else:
            if np.random.rand() < (10 - salient_lottery)/10:
                p.payoff = C.LOTTERY_B_LOW
            else:
                p.payoff = C.LOTTERY_B_HIGH


# PAGES
class RiskPreference(Page):
    form_model = 'player'
    form_fields = ['lottery_b_one', 'lottery_b_two', 'lottery_b_three', 'lottery_b_four',
                   'lottery_b_five', 'lottery_b_six', 'lottery_b_seven', 'lottery_b_eight',
                   'lottery_b_nine', 'lottery_b_ten']


class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = calc_payoffs


class Results(Page):

    def vars_for_template(player: Player):
        return {
            'payoff_in_usd': float(player.payoff) / 1 # Divide by the conversion rate

        }


page_sequence = [RiskPreference,
                 ResultsWaitPage,
                 Results]
