import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from _PlayGamesServices import _PlayGamesServices
'''
All methods of these class are asynchronous and should return immediately.
Callbacks will be fired on success
'''
class PlayGamesServices():
    def __init__(self):
        self._pgs = _PlayGamesServices()
        self._leaderboards_client = _LeaderboardsClient(self._pgs.leaderboards_client)
        self._achievements_client = _AchievementsClient(self._pgs.achievements_client)
    
    @property
    def leaderboards_client(self):
        return self._leaderboards_client
        
    @property
    def achievements_client(self):
        return self._achievements_client
        
class _LeaderboardsClient():
    '''
    https://developers.google.com/android/reference/com/google/android/gms/games/LeaderboardsClient
    '''
    def __init__(self, client ):
        self._client = client
    def get_leaderboards(self, success_callback):
        # success_callback will be called on success with a dict of 
        # {leaderboard_id : https://developers.google.com/android/reference/com/google/android/gms/games/leaderboard/Leaderboard }
        # as parameter
        self._client.get_leaderboards(success_callback)
    def submit_score(self, id, score):
        # if id is None, submit to all leaderboards
        self._client.submit_score(id, score)
    def show_leaderboard(self, id):
        self._client.show_leaderboard(id)
    def show_leaderboards(self):
        self._client.show_leaderboards()
    def get_remote_best(self, id, success_callback):
        # success_callback will be called on success with best value as parameter
        self._client.get_remote_best(id, success_callback)
        
        
class _AchievementsClient():
    '''
    https://developers.google.com/android/reference/com/google/android/gms/games/AchievementsClient
    '''
    def __init__(self, client ):
        self._client = client
    def get_achievements(self, success_callback):
        # success_callback will be called on success with a dict of 
        # { achievement_id : https://developers.google.com/android/reference/com/google/android/gms/games/achievement/Achievement }
        # as parameter
        self._client.get_achievements(success_callback)
    def show_achievements(self):
        self._client.show_achievements()
    def increment(id, numSteps):
        self._client.increment(id, numSteps)
    def set_steps(id, numSteps):
        self._client.set_steps(id, numSteps)
    def unlock(id):
        self._client.unlock(id)
    def reveal(id):
        self._client.reveal(id)