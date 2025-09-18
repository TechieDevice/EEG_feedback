from texasholdem.game.game import TexasHoldEm
from texasholdem.gui.text_gui import TextGUI
from texasholdem.agents import random_agent, call_agent
from typing import Tuple

import random

from texasholdem.game.action_type import ActionType
from texasholdem.game.player_state import PlayerState
from texasholdem.game.hand_phase import HandPhase
from typing import Iterator, Callable, Dict, Tuple, Optional, Union, List, Iterable
from texasholdem.card.card import Card
from math import ceil
import argparse
from PyQt5 import QtCore, QtWidgets
#from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPainter, QBrush, QPen
from texasholdem.evaluator import evaluator
import numpy as np
#from PyQt5.QtCore import Qt


class Vis(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create a label to display the results
        self.result_label = QtWidgets.QLabel(self)
        self.result_label.setAlignment(QtCore.Qt.AlignBottom)
        self.result_label.setStyleSheet('font-size: 24px;')
        
        # Create a layout for the label
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.result_label)
        self.setLayout(layout)

        # Set the window properties
        self.setWindowTitle("Results")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTransparentForInput)

        # Set the size of the window
        self.move(0, 0)
        self.resize(400, 600)

    def update_result(self, result):
        self.result_label.setText(str(result))

        QtWidgets.QApplication.processEvents()
    
    def paintEvent(self, event):
        names = ['SF', '4H', 'FH', 'FL', 'ST', '3H', '22', '2H', '1H']
        painter = QPainter(self)
        painter.setPen(QPen(QtCore.Qt.black, 2))
        painter.setBrush(QBrush(QtCore.Qt.red))
        #sum1 = sum(values_1)
        width = 40
        #if sum1 == 0:
        #    sum1 = 0.000000001
        for i in range(9):
            count = values_1[i]
            #painter.drawRect(20 + i * width, 100 - round(count/sum1 * 500), 20, round(count/sum1 * 500))
            painter.drawRect(20 + i * width, 100 - round(count * 10), 20, round(count * 10))
            values_1_r = np.around(values_1, decimals=2) 
            painter.drawText(20 + i * width, 120, str(values_1_r[i]))
            painter.drawText(20 + i * width, 140, names[i])

            count = values_2[i]
            #painter.drawRect(20 + i * width, 100 - round(count/sum1 * 500), 20, round(count/sum1 * 500))
            painter.drawRect(20 + i * width, 300 - round(count * 3), 20, round(count * 3))
            values_2_r = np.around(values_2, decimals=2) 
            painter.drawText(20 + i * width, 320, str(values_2_r[i]))
            painter.drawText(20 + i * width, 340, names[i])

            count = values_3[i]
            #painter.drawRect(20 + i * width, 100 - round(count/sum1 * 500), 20, round(count/sum1 * 500))
            painter.drawRect(20 + i * width, 500 - round(count * 5), 20, round(count * 5))
            values_3_r = np.around(values_3, decimals=2) 
            painter.drawText(20 + i * width, 520, str(values_3_r[i]))
            painter.drawText(20 + i * width, 540, names[i])







def Prev_detect(game: TexasHoldEm):

    pr_raise = False
    pr_fold = True
    Next = True
    i = game.bb_loc+1
    while Next != False:
        if i>=game.max_players:
            i -= game.max_players
        if i == game.current_player:
            Next = False
        else:
            if game.players[i].state != PlayerState.OUT:
                pr_fold = False
                if game.players[i].state == PlayerState.TO_CALL:
                    pr_raise = True
        i += 1
    return(pr_fold, pr_raise)






def prefold_agent(game: TexasHoldEm, no_fold: bool = False) -> Tuple[ActionType, int]:
    """
    A uniformly random player

        - If someone raised, CALL, FOLD, or RAISE with uniform probability
        - Else, CHECK, (FOLD if no_fold=False), RAISE with uniform probability
        - If RAISE, the value will be uniformly random in [min_raise, # of chips]

    Arguments:
        game (TexasHoldEm): The TexasHoldEm game
        no_fold (bool): Removes the possibility of folding if no one raised, default False.
    Returns:
        Tuple[ActionType, int]: Returns a uniformly random action from the
            available moves.

    """
    bet_amount = game.player_bet_amount(game.current_player)
    chips = game.players[game.current_player].chips
    min_raise = game.value_to_total(game.min_raise(), game.current_player)
    max_raise = bet_amount + chips

    pr_fold, pr_raise = Prev_detect(game)


    
    #active_players = list(game.in_pot_iter(game.btn_loc + 1))
    #bb_loc = active_players.index(game.bb_loc)
    #current_player = active_players.index(game.current_player)

    position = game.current_player-game.bb_loc
    if position<1:
        position += game.max_players
    #print(active_players, '!!!', game.bb_loc, '!!!', game.current_player, '!!!', position)




    possible = list(ActionType)
    possible.remove(ActionType.ALL_IN)

    # A player did not raise
    if game.players[game.current_player].state == PlayerState.IN:
        possible.remove(ActionType.CALL)

    possible.remove(ActionType.FOLD)

    # A player raised
    if game.players[game.current_player].state == PlayerState.TO_CALL:
        possible.remove(ActionType.CHECK)

    # not enough chips to raise
    possible.remove(ActionType.RAISE)

    action_type, total = random.choice(possible), None
        
    #print(bb_loc, current_player, action_type, total, game.hands.get(game.current_player))
    #print(hand_val)
    return action_type, total






if __name__ == '__main__':
    
    app = QtWidgets.QApplication([])
    vis = Vis()
    def update(result):
        vis.update_result(result)

        
    parser = argparse.ArgumentParser(description='Known cards')
    parser.add_argument("--c", default = [], nargs='*')
    parser.add_argument("--n", default = 9, type = int)
    args = parser.parse_args()
    known_str = args.c
    if '00' in known_str:
        i = known_str.index('00')
        known_str = known_str[:i]
    #print(known_str)
    max_players = args.n
    game = TexasHoldEm(buyin=500, big_blind=0, small_blind=0, max_players=max_players)
    gui = TextGUI(game=game, no_wait = True, visible_players = [0], enable_animation = False)
    games = 0
    wins = 0  
    ctgames = 10000
    ar_wins = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ar_loses = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ar_wins_loses = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    

    while game.is_game_running():
        
        game.start_hand(known_str)

        #while game.is_hand_running():
        #    gui.run_step()

        while game.is_hand_running():
            game.take_action(*prefold_agent(game))
        
        my_id = (game.btn_loc+1)%max_players
        games += 1
        list_comb = list(map(evaluator.get_rank_class, game.hand_history.settle.player_ranks))
        if my_id in game.hand_history.settle.pot_winners[0][2]:
            #game.hand_history.settle.
            wins += 1
            ar_wins[list_comb[0]-1] += 1
            #print(min(list_comb))
            #print(my_id, game.btn_loc, game.hand_history.settle, list_comb)
            #print('!!!', my_id, game.hand_history.settle.pot_winners, wins/games*100)
        # else:
        #     #print(game._deck.cards)
        #     print(game.hands)
        #     print(game.hand_history.settle.pot_winners)
        #     print(game.hand_history.settle)
        else:
            ar_loses [list_comb[0]-1] += 1
            ar_wins_loses [min(list_comb)-1] += 1
        ar_wins_m = [100*x/games for x in ar_wins]
        ar_loses_m = [100*x/games for x in ar_loses]
        ar_wins_loses_m = [100*x/games for x in ar_wins_loses]
        #print(ar_wins_m, ar_loses_m, ar_wins_loses_m)
        values_1 = ar_wins_m
        values_2 = ar_loses_m
        values_3 = ar_wins_loses_m

        update(wins/games*100)
        
        #values = [30, 40, 50, 60, 60, 70, 70, 70, 80, 80, 90, 100]
        vis.show()
        QtWidgets.QApplication.processEvents()
        if games == ctgames:
            break
         
    #print(wins/games*100)
    QtCore.QTimer.singleShot(0, vis.close)   
    app.exec_()
        #my_id = (my_id + 1)%max_players
        #print(game.hand_history.settle.pot_winners[0][2])
        #if games%100 == 0:            
        #    path = game.export_history('./pgns')     # save history
        #gui.replay_history(path)                 # replay history