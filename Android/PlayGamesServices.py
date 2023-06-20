import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from _PlayGamesServices import _PlayGamesServices
'''
All methods of this class are asynchronous and should return immediately.
Callbacks will be fired on success
'''
class PlayGamesServices():
    def __init__(self):
        self._pgs = _PlayGamesServices()
    def get_leaderboards_names(self, callback):
        # callback will be called on success with a range of leaderboard names as parameter
        self._pgs.get_leaderboards_names(callback)
    def submit_score(self, score, leaderboard_name = None):
        # if leaderboard_name is None, submit to all leaderboards
        self._pgs.submit_score(score, leaderboard_name)
    def show_leaderboard(self, leaderboard_name):
        self._pgs.show_leaderboard(leaderboard_name)
    def show_leaderboards(self):
        self._pgs.show_leaderboards()
    def get_remote_best(self, leaderboard_name, callback):
        # callback will be called on success with best value as parameter
        self._pgs.get_remote_best(leaderboard_name, callback)