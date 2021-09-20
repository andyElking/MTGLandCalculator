import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

import math
kivy.require("1.9.0")

def binomial(n, k):
    if 0 <= k <= n:
        num = math.factorial(n)
        denom = math.factorial(k) * math.factorial(n - k)
        return num / denom
    else:
        return 0


def hypergeom(sample_success, sample, pop, pop_success):
    hypa = binomial(pop_success, sample_success)
    hypb = binomial((pop - pop_success), (sample - sample_success))
    hypc = binomial(pop, sample)
    if hypc > 0:
        return (hypa * hypb) / hypc
    else:
        return 0


def probability(N_dr, L_opmin, L_opmax, L_min, L_max, L_d):
    """if not(N_dr.isnumeric() and L_opmin.isnumeric() and L_opmax.isnumeric() and L_min.isnumeric()
        and L_max.isnumeric() and L_d.isnumeric()):
        return "error"
    else: """
    opening_nomullignas = []
    opening_withmullignas = []
    sum_nomulligans = 0
    sum_withmulligans = 0
    mulligan_coeff = 0

    for i in range(L_opmin, min(L_opmax + 1, 8)):  # first make a list of tuples of the form:
        # (number_of_lands_in_opening_hand, probability_of_drawing_such_a_hand)
        a = hypergeom(i, 7, 60, L_d)
        opening_nomullignas.append((i, a))
        mulligan_coeff = mulligan_coeff + a  # this will be used later for calculating the probability of
        # taking the mulligan and is used as a coefficient before the mulligan sum
    for (x, y) in opening_nomullignas:  # use the list of tuples to calculate the first part of equation 5
        partial_nomulligans = 0
        for j in range(L_min - x, L_max - x + 1):
            partial_nomulligans = partial_nomulligans + hypergeom(j, N_dr, 53, L_d - x)
        sum_nomulligans = sum_nomulligans + partial_nomulligans * y

    mulligan_coeff = 1 - mulligan_coeff  # probability of mulliganing
    for i in range(L_opmin, min(L_opmax + 1, 7)):  # doing the same thing as before, but drawing 6 instead of 7 cards
        a = hypergeom(i, 6, 60, L_d)
        opening_withmullignas.append((i, a))

    for (x, y) in opening_withmullignas:
        partial_withmulligans = 0
        for j in range(L_min - x, L_max - x + 1):
            partial_withmulligans = partial_withmulligans + hypergeom(j, N_dr, 54, L_d - x)
        sum_withmulligans = sum_withmulligans + partial_withmulligans * y
    total_withmulligans = mulligan_coeff * sum_withmulligans

    return total_withmulligans + sum_nomulligans


class PCalcBoxLayout(BoxLayout):
    def calculate(self):
        grid = self.ids.theThing
        x = self.ids
        grid2 = self.ids.theotherThing
        grid2.size_hint_y = 1.0
        grid2.clear_widgets()
        a_is_properly_filled_in = False
        b_is_properly_filled_in = False
        c_is_properly_filled_in = False

        if x.L_dmed.text.isnumeric():
            if (x.aN_dr.text.isnumeric() and x.aL_opmin.text.isnumeric() and x.aL_opmax.text.isnumeric()
                    and x.aL_min.text.isnumeric() and x.aL_max.text.isnumeric() and x.L_dmed.text.isnumeric()):
                a_is_properly_filled_in = True

            if (x.bN_dr.text.isnumeric() and x.bL_opmin.text.isnumeric() and x.bL_opmax.text.isnumeric()
                    and x.bL_min.text.isnumeric() and x.bL_max.text.isnumeric() and x.L_dmed.text.isnumeric()):
                b_is_properly_filled_in = True

            if (x.cN_dr.text.isnumeric() and x.cL_opmin.text.isnumeric() and x.cL_opmax.text.isnumeric()
                    and x.cL_min.text.isnumeric() and x.cL_max.text.isnumeric() and x.L_dmed.text.isnumeric()):
                c_is_properly_filled_in = True

            for iL_d in range(int(x.L_dmed.text) - 3, int(x.L_dmed.text) + 4):
                if a_is_properly_filled_in:
                    resulta = probability(int(x.aN_dr.text), int(x.aL_opmin.text), int(x.aL_opmax.text),
                                          int(x.aL_min.text),
                                          int(x.aL_max.text), iL_d)
                else:
                    resulta = 1

                if b_is_properly_filled_in:
                    resultb = probability(int(x.bN_dr.text), int(x.bL_opmin.text), int(x.bL_opmax.text),
                                          int(x.bL_min.text),
                                          int(x.bL_max.text), iL_d)
                else:
                    resultb = 1

                if c_is_properly_filled_in:
                    resultc = probability(int(x.cN_dr.text), int(x.cL_opmin.text), int(x.cL_opmax.text),
                                          int(x.cL_min.text),
                                          int(x.cL_max.text), iL_d)
                else:
                    resultc = 1

                grid2.add_widget(Label(text=str(iL_d)))
                grid2.add_widget(Label(text=str(resulta)))
                grid2.add_widget(Label(text=str(resultb)))
                grid2.add_widget(Label(text=str(resultc)))
                grid2.add_widget(Label(text=str(resulta * resultb * resultc)))

        else:
            grid2.add_widget(Label(text="Input the number of lands in the deck"))


class ProbcalcApp(App):
    def build(self):
        return PCalcBoxLayout()


tralala = ProbcalcApp()
tralala.run()
