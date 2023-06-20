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
        
        self.leaderboards = None
        self.getting_leaderboards = False
        self.show_leaderboard_candidates = {}
        self.show_leaderboards_candidate = False
        self.showing_leaderboard = False
        self.get_leaderboards_names_callback = None
        
        self.player = None
        self.getting_player = False
        
        self.remote_bests = {}
        self.getting_remote_best = False
        self.getting_remote_best_current_name = None
        self.submit_candidates = {}
        self.get_remote_best_callbacks = {}
        
        
        self.on_fetched_best = None
        self.on_fetched_leaderboards = None
        
        self.get_leaderboards_success_listener = OnSuccessListener(self._on_get_leaderboards_success)
        self.show_leaderboard_success_listener = OnSuccessListener(self._on_show_leaderboard_success)
        self.get_remote_best_success_listener = OnSuccessListener(self._on_get_remote_best_success)
        self.get_leaderboards_failure_listener = OnFailureListener(self._on_get_leaderboards_failure)
        self.show_leaderboard_failure_listener = OnFailureListener(self._on_show_leaderboard_failure)
        self.get_remote_best_failure_listener = OnFailureListener(self._on_get_remote_best_failure)
        self.sign_in_complete_listener = OnCompleteListener_AuthenticationResult(self._on_signin_complete)
        self.get_player_complete_listener = OnCompleteListener_Player(self._on_get_player)
        
        print(f"PlayGamesServices : initialize PlayGamesSdk")
        
    def synchronize(self): 
        print(f"PlayGamesServices : synchronizing...")
        if self._initialized == False:
            self._initialize()
            return
        if self.authenticated == False:
            self._sign_in()
            return
        if self.leaderboards is None:
            self._get_leaderboards()
            return
        get_leaderboards_names_callback = self.get_leaderboards_names_callback
        self.get_leaderboards_names_callback = None
        if get_leaderboards_names_callback is not None:
            get_leaderboards_names_callback(list(self.leaderboards.keys()))
        for name in self.leaderboards.keys():
            if name not in self.show_leaderboard_candidates.keys():
                self.show_leaderboard_candidates[name] = False
        for name, value in self.show_leaderboard_candidates.items():
            if value:
                self._show_leaderboard(name)
                self.show_leaderboard_candidates[name] = False
                return
        if self.show_leaderboards_candidate :
            self._show_leaderboard()
            self.show_leaderboards_candidate = False
            return
                
        if self.player is None:
            self._get_player()
            return
            
        for name in self.leaderboards.keys():
            if name not in self.remote_bests.keys():
                self.remote_bests[name] = None
        for name, best in self.remote_bests.items():
            if best is None:
                self.getting_remote_best_current_name = name
                self._get_remote_best(name)
                return
        for name, callback in self.get_remote_best_callbacks.items():
            if callback is not None:
                callback()
            self.get_remote_best_callbacks[name] = None
                
        self.getting_remote_best_current_name = None
        for name in self.leaderboards.keys():
            if name not in self.submit_candidates.keys():
                self.submit_candidates[name] = None
        for name, score in self.submit_candidates.items():
            if score is not None:
                self._submit_score(name, score)
                self.submit_candidates[name] = None
                
    @run_on_ui_thread
    def _initialize(self):
        print(f"PlayGamesServices : BEG _initialize")
        JavaBridge.PlayGamesSdk.initialize(self.activity)
        self._initialized = True
        self.synchronize()
        print(f"PlayGamesServices : END _initialize")
        
    def _on_signin_complete(self, result):
        self.authenticating = False
        self.authenticated = result
        print("PlayGamesServices : Authentication result : {result}")
        if result:
            self.synchronize()
    @run_on_ui_thread
    def _sign_in(self):   
        print(f"PlayGamesServices : BEG _sign_in")
        if self.authenticating == False:
            self.authenticating = True
            JavaBridge.PlayGames.getGamesSignInClient(self.activity).isAuthenticated().addOnCompleteListener(JavaBridge.OnCompleteListener_AuthenticationResult(self.sign_in_complete_listener))
            JavaBridge.PlayGames.getGamesSignInClient(self.activity).signIn()
        else: 
            print("PlayGamesServices : _sign_in : already queued")
        print(f"PlayGamesServices : END _sign_in")
        
    def _on_get_player(self, player):
        print("PlayGamesServices : Successfully fetched player info")
        self.getting_player = False
        self.player = player
        if self.player is not None:
            self.synchronize()
    @run_on_ui_thread
    def _get_player(self):
        print("PlayGamesServices : BEG _get_player")
        if self.getting_player == False:
            self.getting_player = True
            JavaBridge.PlayGames.getPlayersClient(self.activity).getCurrentPlayer().addOnCompleteListener(JavaBridge.OnCompleteListener_Player(self.get_player_complete_listener))
        else: 
            print("PlayGamesServices : _get_player : already queued")
        print("PlayGamesServices : END _get_player")
        
    def _on_get_leaderboards_failure(self, e):
        print(f"PlayGamesServices :_on_get_leaderboards_failure : {e.getMessage()}")
        self.getting_leaderboards = False
        self.leaderboards = None
    @run_on_ui_thread
    def _on_get_leaderboards_success(self, leaderboardBufferAnnotatedData):
        print(f"PlayGamesServices :_on_get_leaderboards_success")
        self.getting_leaderboards = False
        buffer = leaderboardBufferAnnotatedData.get()
        count = buffer.getCount()
        print(f"PlayGamesServices : {count} leaderboards")
        self.leaderboards = {}
        for i in range(count):
            leaderboard = buffer.get(i)
            print(f"PlayGamesServices : {leaderboard.getDisplayName()} : {leaderboard.getLeaderboardId()}")
            self.leaderboards[leaderboard.getDisplayName()] = leaderboard.getLeaderboardId()
        buffer.release()
        self.synchronize()
    @run_on_ui_thread
    def _get_leaderboards(self):
        print(f"PlayGamesServices : BEG _get_leaderboards")
        if self.getting_leaderboards == False:
            self.getting_leaderboards = True
            task = JavaBridge.PlayGames.getLeaderboardsClient(self.activity).loadLeaderboardMetadata(True)
            task.addOnSuccessListener(self.get_leaderboards_success_listener)
            task.addOnFailureListener(self.get_leaderboards_failure_listener)
        else:
            print("PlayGamesServices : _get_leaderboards : already queued")
        print(f"PlayGamesServices : END _get_leaderboards") 
    def get_leaderboards_names(self, callback):
        print(f"PlayGamesServices : BEG get_leaderboards_names")
        self.get_leaderboards_names_callback = callback
        self.synchronize()
        print(f"PlayGamesServices : END get_leaderboards_names")
        
    @run_on_ui_thread
    def _submit_score(self, leaderboard_name, score):
        print("PlayGamesServices : BEG _submit_score")
        JavaBridge.PlayGames.getLeaderboardsClient(self.activity).submitScore(self.leaderboards[leaderboard_name], score);
        print(f"PlayGamesServices : {self.player.getDisplayName()} submitted a new high score : {score}")
        print("PlayGamesServices : END _submit_score")

    def submit_score(self, score, leaderboard_name = None):
        print("PlayGamesServices : BEG submit_score {leaderboard_name}")
        if leaderboard_name is not None:
            self.submit_candidates[leaderboard_name] = score
        else:
            for key in self.submit_candidates.keys():
                self.submit_candidates[key] = score
        self.synchronize()
        print("PlayGamesServices : END submit_score {leaderboard_name}")
        
    def _on_show_leaderboard_failure(self, e):
        print(f"PlayGamesServices :_on_show_leaderboard_failure : {e.getMessage()}")
        self.showing_leaderboard = False
    @run_on_ui_thread
    def _on_show_leaderboard_success(self, intent):
        print(f"PlayGamesServices : Showing LeaderBoard")
        self.activity.startActivityForResult(intent, 9004);
        self.showing_leaderboard = False
        self.synchronize()
    @run_on_ui_thread
    def _show_leaderboard(self, leaderboard_name = None):
        print("PlayGamesServices : BEG _show_leaderboard")
        if self.showing_leaderboard == False:
            self.showing_leaderboard = True
            if leaderboard_name is not None:
                task = JavaBridge.PlayGames.getLeaderboardsClient(self.activity).getLeaderboardIntent(self.leaderboards[leaderboard_name])
            else :
                task = JavaBridge.PlayGames.getLeaderboardsClient(self.activity).getAllLeaderboardsIntent()
            task.addOnSuccessListener(self.show_leaderboard_success_listener)
            task.addOnFailureListener(self.show_leaderboard_failure_listener)
        else:
            print("PlayGamesServices : _show_leaderboard : already queued")
        print("PlayGamesServices : END _show_leaderboard")
    def show_leaderboard(self, leaderboard_name):
        print("PlayGamesServices : BEG show_leaderboard")
        self.show_leaderboard_candidates[leaderboard_name] = True
        self.synchronize()
        print("PlayGamesServices : END show_leaderboard")
    def show_leaderboards(self):
        print("PlayGamesServices : BEG show_leaderboards")
        self.show_leaderboards_candidate = True
        self.synchronize()
        print("PlayGamesServices : END show_leaderboards")
            
    def _on_get_remote_best_failure(self, e):
        print(f"PlayGamesServices :_on_get_remote_best_failure : {e.getMessage()}")
        self.getting_remote_best = False
        self.getting_remote_best_current_name = None
    @run_on_ui_thread
    def _on_get_remote_best_success(self, leaderboardScoreAnnotatedData):
        print(f"PlayGamesServices : _on_get_remote_best_complete")
        scoreResult =  leaderboardScoreAnnotatedData.get()
        best = 0
        if scoreResult is not None:
            print(scoreResult.getDisplayRank())
            print(scoreResult.getDisplayScore())
            print(scoreResult.getScoreHolderDisplayName())
            best = scoreResult.getRawScore()
            print(f"PlayGamesServices : Fetched remote best : {self.getting_remote_best_current_name} : {best}")
        else:
            print(f"PlayGamesServices : Fetched remote best error: scoreResult is None")
        self.remote_bests[self.getting_remote_best_current_name] = best
        self.getting_remote_best = False
        self.getting_remote_best_current_name = None
        self.synchronize()
    @run_on_ui_thread
    def _get_remote_best(self, leaderboard_name):
        print("PlayGamesServices : BEG _get_remote_best")
        if self.getting_remote_best == False:
            self.getting_remote_best = True
            task = JavaBridge.PlayGames.getLeaderboardsClient(self.activity).loadCurrentPlayerLeaderboardScore(self.leaderboards[leaderboard_name], JavaBridge.LeaderboardVariant.TIME_SPAN_ALL_TIME, JavaBridge.LeaderboardVariant.COLLECTION_PUBLIC)
            task.addOnSuccessListener(self.get_remote_best_success_listener)
            task.addOnFailureListener(self.get_remote_best_failure_listener)
        else:
            print("PlayGamesServices : _get_remote_best : already queued")
        print("PlayGamesServices : END _get_remote_best")
        
    def get_remote_best(self, leaderboard_name, callback):
        print("PlayGamesServices : BEG get_remote_best")
        self.remote_bests[leaderboard_name] = None
        self.get_remote_best_callbacks[leaderboard_name] = callback
        self.synchronize()
        print("PlayGamesServices : END get_remote_best")