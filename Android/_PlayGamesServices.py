from jnius import autoclass, PythonJavaClass, JavaClass, java_method
from android.runnable import run_on_ui_thread

class JavaBridge:
    PlayGamesSdk = autoclass("com.google.android.gms.games.PlayGamesSdk")
    PlayGames = autoclass("com.google.android.gms.games.PlayGames")
    Activity = autoclass("org.kivy.android.PythonActivity")
    OnCompleteListener_AuthenticationResult = autoclass("com.cldejessey.OnCompleteListener_AuthenticationResult")
    OnCompleteListener_Player = autoclass("com.cldejessey.OnCompleteListener_Player")
    LeaderboardVariant = autoclass("com.google.android.gms.games.leaderboard.LeaderboardVariant")
        
class OnCompleteListener_Player(PythonJavaClass):
    __javainterfaces__ = ("com.cldejessey.OnCompleteListener_PlayerInterface", )
    __javacontext__ = "app"
    def __init__(self, callback):
        self.callback = callback

    @java_method('(Lcom/google/android/gms/games/Player;)V')
    def onComplete(self, result):
        print(f"PlayGamesServices : onComplete Player callback")
        self.callback(result)
    
class OnCompleteListener_AuthenticationResult(PythonJavaClass):
    __javainterfaces__ = ("com.cldejessey.OnCompleteListener_AuthenticationResultInterface", )
    __javacontext__ = "app"
    def __init__(self, on_signin_complete):
        self.on_signin_complete = on_signin_complete

    @java_method('(Lcom/google/android/gms/games/AuthenticationResult;)V')
    def onComplete(self, result):
        print(f"PlayGamesServices : Authentication result : {result.isAuthenticated()}")
        self.on_signin_complete(result.isAuthenticated())
        
class OnSuccessListener(PythonJavaClass):
    __javainterfaces__ = ("com.google.android.gms.tasks.OnSuccessListener", )
    __javacontext__ = "app"
    def __init__(self, callback):
        self.callback = callback

    @java_method('(Ljava/lang/Object;)V')
    def onSuccess(self, obj):
        print("PlayGamesServices : onSuccess callback")
        self.callback(obj)
        
class OnFailureListener(PythonJavaClass):
    __javainterfaces__ = ("com.google.android.gms.tasks.OnFailureListener", )
    __javacontext__ = "app"
    def __init__(self, callback):
        self.callback = callback

    @java_method('(Ljava/lang/Exception;)V')
    def onFailure(self, e):
        print("PlayGamesServices : onFailure callback")
        self.callback(e)

class _PlayGamesServices():
    def __init__(self):
        self.activity = JavaBridge.Activity.mActivity
        self._initialized = False
        
        self.authenticated = False
        self.authenticating = False
        
        self.player = None
        self.getting_player = False
        
        self.sign_in_complete_listener = OnCompleteListener_AuthenticationResult(self._on_signin_complete)
        self.get_player_complete_listener = OnCompleteListener_Player(self._on_get_player)
        
        self._leaderboards_client = _LeaderboardClient(self)
        self._achievements_client = _AchievementsClient(self)
        
        self._synchronized = True
        
    def synchronize(self): 
        print(f"_PlayGamesServices : synchronize")
        if not self._initialized:
            self._synchronized = False
            self._initialize()
            return False
        if not self.authenticated:
            self._synchronized = False
            self._sign_in()
            return False
        if self.player is None:
            self._synchronized = False 
            self._get_player()
            return False
        if not self._synchronized:
            self._synchronized = True
            self._leaderboards_client.synchronize()
            self._achievements_client.synchronize()
        return True
        
    @property
    def leaderboards_client(self):
        return self._leaderboards_client
        
    @property
    def achievements_client(self):
        return self._achievements_client
                
    @run_on_ui_thread
    def _initialize(self):
        print(f"_PlayGamesServices : BEG _initialize")
        JavaBridge.PlayGamesSdk.initialize(self.activity)
        self._initialized = True
        self.synchronize()
        print(f"_PlayGamesServices : END _initialize")
        
    def _on_signin_complete(self, result):
        self.authenticating = False
        self.authenticated = result
        print("_PlayGamesServices : Authentication result : {result}")
        if result:
            self.synchronize()
    @run_on_ui_thread
    def _sign_in(self):   
        print(f"_PlayGamesServices : BEG _sign_in")
        if self.authenticating == False:
            self.authenticating = True
            JavaBridge.PlayGames.getGamesSignInClient(self.activity).isAuthenticated().addOnCompleteListener(JavaBridge.OnCompleteListener_AuthenticationResult(self.sign_in_complete_listener))
            JavaBridge.PlayGames.getGamesSignInClient(self.activity).signIn()
        else: 
            print("_PlayGamesServices : _sign_in : already queued")
        print(f"_PlayGamesServices : END _sign_in")
        
    def _on_get_player(self, player):
        print("_PlayGamesServices : Successfully fetched player info")
        self.getting_player = False
        self.player = player
        if self.player is not None:
            self.synchronize()
    @run_on_ui_thread
    def _get_player(self):
        print("_PlayGamesServices : BEG _get_player")
        if self.getting_player == False:
            self.getting_player = True
            JavaBridge.PlayGames.getPlayersClient(self.activity).getCurrentPlayer().addOnCompleteListener(JavaBridge.OnCompleteListener_Player(self.get_player_complete_listener))
        else: 
            print("_PlayGamesServices : _get_player : already queued")
        print("_PlayGamesServices : END _get_player")

class _LeaderboardClient():
    def __init__(self, pgs):
        self._pgs = pgs
        
        self.leaderboards = None
        self.getting_leaderboards = False
        self.show_leaderboard_candidates = {}
        self.show_leaderboards_candidate = False
        self.showing_leaderboard = False
        self.get_leaderboards_callback = None
        
        self.remote_bests = {}
        self.getting_remote_best = False
        self.getting_remote_best_current_id = None
        self.submit_candidates = {}
        self.get_remote_best_callbacks = {}
        self.on_fetched_best = None
        self.on_fetched_leaderboards = None
        
        self.get_leaderboards_success_listener = OnSuccessListener(self._on_get_leaderboards_success)
        self.get_leaderboards_failure_listener = OnFailureListener(self._on_get_leaderboards_failure)
        self.show_leaderboard_success_listener = OnSuccessListener(self._on_show_leaderboard_success)
        self.show_leaderboard_failure_listener = OnFailureListener(self._on_show_leaderboard_failure)
        self.get_remote_best_success_listener = OnSuccessListener(self._on_get_remote_best_success)
        self.get_remote_best_failure_listener = OnFailureListener(self._on_get_remote_best_failure)
        
    def synchronize(self):
        print(f"_LeaderboardClient : synchronize")
        pgs_synchronized = self._pgs.synchronize()
        if not self._pgs.authenticated:
            return
            
        if self.leaderboards is None:
            self._get_leaderboards()
            return
        if self.get_leaderboards_callback is not None:
            get_leaderboards_callback = self.get_leaderboards_callback
            self.get_leaderboards_callback = None
            get_leaderboards_callback(self.leaderboards)
        for id, value in self.show_leaderboard_candidates.items():
            if value:
                self.show_leaderboard_candidates[id] = False
                self._show_leaderboard(id)
                return
        if self.show_leaderboards_candidate :
            self.show_leaderboards_candidate = False
            self._show_leaderboard()
            return
        
        if not pgs_synchronized:
            return
        for id, score in self.submit_candidates.items():
            if score is not None:
                self.submit_candidates[id] = None
                self._submit_score(id, score)
                
        for id, best in self.remote_bests.items():
            if best is None:
                self._get_remote_best(id)
                return
        
        for id, callback in self.get_remote_best_callbacks.items():
            if callback is not None:
                callback(self.remote_bests[id])
            self.get_remote_best_callbacks[id] = None
                
    def _on_get_leaderboards_failure(self, e):
        print(f"_LeaderboardClient :_on_get_leaderboards_failure : {e.getMessage()}")
        self.getting_leaderboards = False
        self.leaderboards = None
    @run_on_ui_thread
    def _on_get_leaderboards_success(self, leaderboardBufferAnnotatedData):
        print(f"_LeaderboardClient :_on_get_leaderboards_success")
        self.getting_leaderboards = False
        buffer = leaderboardBufferAnnotatedData.get()
        count = buffer.getCount()
        print(f"_LeaderboardClient : {count} leaderboards")
        self.leaderboards = {}
        for i in range(count):
            leaderboard = buffer.get(i)
            print(f"_LeaderboardClient : {leaderboard.getDisplayName()} : {leaderboard.getLeaderboardId()}")
            self.leaderboards[leaderboard.getLeaderboardId()] = leaderboard
        buffer.release()
        self.synchronize()
    @run_on_ui_thread
    def _get_leaderboards(self):
        print(f"_LeaderboardClient : BEG _get_leaderboards")
        if self.getting_leaderboards == False:
            self.getting_leaderboards = True
            task = JavaBridge.PlayGames.getLeaderboardsClient(self._pgs.activity).loadLeaderboardMetadata(True)
            task.addOnSuccessListener(self.get_leaderboards_success_listener)
            task.addOnFailureListener(self.get_leaderboards_failure_listener)
        else:
            print("_LeaderboardClient : _get_leaderboards : already queued")
        print(f"_LeaderboardClient : END _get_leaderboards") 
    def get_leaderboards(self, callback):
        print(f"_LeaderboardClient : BEG get_leaderboards")
        self.get_leaderboards_callback = callback
        self.synchronize()
        print(f"_LeaderboardClient : END get_leaderboards")
        
    @run_on_ui_thread
    def _submit_score(self, id, score):
        print("_LeaderboardClient : BEG _submit_score")
        JavaBridge.PlayGames.getLeaderboardsClient(self._pgs.activity).submitScore(id, score);
        print(f"_LeaderboardClient : {self.player.getDisplayName()} submitted a new score : {id} : {score}")
        print("_LeaderboardClient : END _submit_score")

    def submit_score(self, id, score):
        print(f"_LeaderboardClient : BEG submit_score {id}")
        self.submit_candidates[id] = score
        self.synchronize()
        print(f"_LeaderboardClient : END submit_score {id}")
        
    def _on_show_leaderboard_failure(self, e):
        print(f"_LeaderboardClient :_on_show_leaderboard_failure : {e.getMessage()}")
        self.showing_leaderboard = False
    @run_on_ui_thread
    def _on_show_leaderboard_success(self, intent):
        print(f"_LeaderboardClient : Showing LeaderBoard")
        self._pgs.activity.startActivityForResult(intent, 9004);
        self.showing_leaderboard = False
        self.synchronize()
    @run_on_ui_thread
    def _show_leaderboard(self, id = None):
        print("_LeaderboardClient : BEG _show_leaderboard")
        if self.showing_leaderboard == False:
            self.showing_leaderboard = True
            if id is not None:
                task = JavaBridge.PlayGames.getLeaderboardsClient(self._pgs.activity).getLeaderboardIntent(id)
            else :
                task = JavaBridge.PlayGames.getLeaderboardsClient(self._pgs.activity).getAllLeaderboardsIntent()
            task.addOnSuccessListener(self.show_leaderboard_success_listener)
            task.addOnFailureListener(self.show_leaderboard_failure_listener)
        else:
            print("_LeaderboardClient : _show_leaderboard : already queued")
        print("_LeaderboardClient : END _show_leaderboard")
    def show_leaderboard(self, id):
        print("_LeaderboardClient : BEG show_leaderboard")
        self.show_leaderboard_candidates[id] = True
        self.synchronize()
        print("_LeaderboardClient : END show_leaderboard")
    def show_leaderboards(self):
        print("_LeaderboardClient : BEG show_leaderboards")
        self.show_leaderboards_candidate = True
        self.synchronize()
        print("_LeaderboardClient : END show_leaderboards")
            
    def _on_get_remote_best_failure(self, e):
        print(f"_LeaderboardClient :_on_get_remote_best_failure : {e.getMessage()}")
        self.getting_remote_best = False
        self.getting_remote_best_current_id = None
    @run_on_ui_thread
    def _on_get_remote_best_success(self, leaderboardScoreAnnotatedData):
        print(f"_LeaderboardClient : _on_get_remote_best_complete")
        scoreResult =  leaderboardScoreAnnotatedData.get()
        best = 0
        if scoreResult is not None:
            print(scoreResult.getDisplayRank())
            print(scoreResult.getDisplayScore())
            print(scoreResult.getScoreHolderDisplayName())
            best = scoreResult.getRawScore()
            print(f"_LeaderboardClient : Fetched remote best : {self.getting_remote_best_current_id} : {best}")
        else:
            print(f"_LeaderboardClient : Fetched remote best error: scoreResult is None")
        self.remote_bests[self.getting_remote_best_current_id] = best
        self.getting_remote_best = False
        self.getting_remote_best_current_id = None
        self.synchronize()
    @run_on_ui_thread
    def _get_remote_best(self, id):
        print("_LeaderboardClient : BEG _get_remote_best")
        if self.getting_remote_best == False:
            self.getting_remote_best = True
            self.getting_remote_best_current_id = id
            task = JavaBridge.PlayGames.getLeaderboardsClient(self._pgs.activity).loadCurrentPlayerLeaderboardScore(id, JavaBridge.LeaderboardVariant.TIME_SPAN_ALL_TIME, JavaBridge.LeaderboardVariant.COLLECTION_PUBLIC)
            task.addOnSuccessListener(self.get_remote_best_success_listener)
            task.addOnFailureListener(self.get_remote_best_failure_listener)
        else:
            print("_LeaderboardClient : _get_remote_best : already queued")
        print("_LeaderboardClient : END _get_remote_best")
        
    def get_remote_best(self, id, callback):
        print("_LeaderboardClient : BEG get_remote_best")
        self.remote_bests[id] = None
        self.get_remote_best_callbacks[id] = callback
        self.synchronize()
        print("_LeaderboardClient : END get_remote_best")
        
class _AchievementsClient():
    def __init__(self, pgs):
        self._pgs = pgs
        
        self.achievements = None
        self.getting_achievements = False
        self.get_achievements_callback = None
        self.showing_achievements = False
        self.show_achievements_candidate = False
        self.set_steps_candidates = {}
        self.unlock_candidates = {}
        self.reveal_candidates = {}
        self.increment_candidates = {}
        
        self.get_achievements_success_listener = OnSuccessListener(self._on_get_achievements_success)
        self.get_achievements_failure_listener = OnFailureListener(self._on_get_achievements_failure)
        self.show_leaderboard_success_listener = OnSuccessListener(self._on_show_achievements_success)
        self.show_leaderboard_failure_listener = OnFailureListener(self._on_show_achievements_failure)
        
    def synchronize(self):
        print(f"_AchievementsClient : synchronize")
        pgs_synchronized = self._pgs.synchronize()
        if not self._pgs.authenticated:
            return
            
        if self.show_achievements_candidate :
            self.show_achievements_candidate = False
            self._show_achievements()
            return
            
        if not pgs_synchronized:
            return
            
        if self.achievements is None:
            self._get_achievements()
            return
            
        if self.get_achievements_callback is not None:
            get_achievements_callback = self.get_achievements_callback
            self.get_achievements_callback = None
            get_achievements_callback(self.achievements)
            
        for id, increment in self.increment_candidates:
            if increment is not None:
                self.increment_candidates[id] = None
                self._increment(id, num_steps)
                
        for id, num_steps in self.set_steps_candidates:
            if num_steps is not None:
                self.set_steps_candidates[id] = None
                self._set_steps(id, num_steps)
                
        for id, unlock in self.unlock_candidates:
            if unlock:
                self.unlock_candidates[id] = False
                self._unlock(id)
                
        for id, reveal in self.reveal_candidates:
            if reveal:
                self.reveal_candidates[id] = False
                self._reveal(id)
    
    def _on_get_achievements_failure(self, e):
        print(f"_AchievementsClient :_on_get_achievements_failure : {e.getMessage()}")
        self.getting_achievements = False
        self.achievements = None
    @run_on_ui_thread
    def _on_get_achievements_success(self, achievementBufferAnnotatedData):
        print(f"_AchievementsClient :_on_get_achievements_success")
        self.getting_achievements = False
        buffer = achievementBufferAnnotatedData.get()
        count = buffer.getCount()
        print(f"_AchievementsClient : {count} achievements")
        self.achievements = {}
        for i in range(count):
            achievement = buffer.get(i)
            print(f"_AchievementsClient : {achievement.getName()} : {achievement.getAchievementId()}")
            self.achievements[achievement.getAchievementId()] = achievement
        buffer.release()
        self.synchronize()
    @run_on_ui_thread
    def _get_achievements(self):
        print(f"_AchievementsClient : BEG _get_achievements")
        if self.getting_achievements == False:
            self.getting_achievements = True
            task = JavaBridge.PlayGames.getAchievementsClient(self._pgs.activity).load(True)
            task.addOnSuccessListener(self.get_achievements_success_listener)
            task.addOnFailureListener(self.get_achievements_failure_listener)
        else:
            print("_AchievementsClient : _get_achievements : already queued")
        print(f"_AchievementsClient : END _get_achievements") 
    def get_achievements(self, callback):
        print(f"_AchievementsClient : BEG get_achievements")
        self.get_achievements_callback = callback
        self.synchronize()
        print(f"_AchievementsClient : END get_achievements")
      
    def _on_show_achievements_failure(self, e):
        print(f"_AchievementsClient :_on_show_leaderboard_failure : {e.getMessage()}")
        self.showing_achievements = False
    @run_on_ui_thread
    def _on_show_achievements_success(self, intent):
        print(f"_AchievementsClient : Showing Achievements")
        self._pgs.activity.startActivityForResult(intent, 9004);
        self.showing_achievements = False
        self.synchronize()
    @run_on_ui_thread
    def _show_achievements(self):
        print("_AchievementsClient : BEG _show_achievements")
        if self.showing_achievements == False:
            self.showing_achievements = True
            task = JavaBridge.PlayGames.getAchievementsClient(self._pgs.activity).getAchievementsIntent()
            task.addOnSuccessListener(self.show_leaderboard_success_listener)
            task.addOnFailureListener(self.show_leaderboard_failure_listener)
        else:
            print("_AchievementsClient : _show_achievements : already queued")
        print("_AchievementsClient : END _show_achievements")
    def show_achievements(self):
        print("_AchievementsClient : BEG show_achievements")
        self.show_achievements_candidate = True
        self.synchronize()
        print("_AchievementsClient : END show_achievements")  
        
    @run_on_ui_thread
    def _increment(self, id, num_steps):
        print(f"_AchievementsClient : BEG _increment")
        JavaBridge.PlayGames.getAchievementsClient(self._pgs.activity).increment(id, numSteps)
        print(f"_AchievementsClient : END _increment")
    def increment(self, id, num_steps):
        print(f"_AchievementsClient : BEG increment")
        self.increment_candidates[id] = num_steps
        self.synchronize()
        print(f"_AchievementsClient : END increment")
        
    @run_on_ui_thread
    def _set_steps(self, id, num_steps):
        print(f"_AchievementsClient : BEG _set_steps")
        JavaBridge.PlayGames.getAchievementsClient(self._pgs.activity).setSteps(id, numSteps)
        print(f"_AchievementsClient : END _set_steps")
    def set_steps(self, id, num_steps):
        print(f"_AchievementsClient : BEG set_steps")
        self.set_steps_candidates[id] = num_steps
        self.synchronize()
        print(f"_AchievementsClient : END set_steps")
        
    @run_on_ui_thread
    def _unlock(self, id):
        print(f"_AchievementsClient : BEG _unlock")
        JavaBridge.PlayGames.getAchievementsClient(self._pgs.activity).unlock(id)
        print(f"_AchievementsClient : END _unlock")
    def unlock(self, id):
        print(f"_AchievementsClient : BEG unlock")
        self.unlock_candidates[id] = True
        self.synchronize()
        print(f"_AchievementsClient : END unlock")
        
    @run_on_ui_thread
    def _reveal(self, id):
        print(f"_AchievementsClient : BEG _reveal")
        JavaBridge.PlayGames.getAchievementsClient(self._pgs.activity).reveal(id)
        print(f"_AchievementsClient : END _reveal")
    def reveal(self, id):
        print(f"_AchievementsClient : BEG reveal")
        self.reveal_candidates[id] = True
        self.synchronize()
        print(f"_AchievementsClient : END reveal")