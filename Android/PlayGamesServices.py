import Settings
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
        print(result)
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
        print(f"PlayGamesServices : onSuccess callback")
        self.callback(obj)

class PlayGamesServices():
    @run_on_ui_thread
    def __init__(self, leaderboard_id):
        self.activity = JavaBridge.Activity.mActivity
        JavaBridge.PlayGamesSdk.initialize(self.activity)
        JavaBridge.PlayGames.getGamesSignInClient(self.activity).isAuthenticated().addOnCompleteListener(JavaBridge.OnCompleteListener_AuthenticationResult(OnCompleteListener_AuthenticationResult(self._on_signin_complete)))
        self.signed = False
        self.player = None
        self.leaderboard_id = leaderboard_id
        self.on_fetched_best = None
        
    @run_on_ui_thread
    def _on_signin_complete(self, result):
        if result:
            self.signed = True
            JavaBridge.PlayGames.getPlayersClient(self.activity).getCurrentPlayer().addOnCompleteListener(JavaBridge.OnCompleteListener_Player(OnCompleteListener_Player(self._set_player)))
            print("PlayGamesServices : Successful GooglePlay signin")
        else:
            self.signed = False
            print("PlayGamesServices : Failed GooglePlay signin")
            
    @run_on_ui_thread
    def _on_show_leaderboard_success(self, intent):
        print(f"PlayGamesServices : Showing LeaderBoard")
        self.activity.startActivityForResult(intent, 9004);
        
    @run_on_ui_thread
    def _on_get_remote_best_success(self, leaderboardScoreAnnotatedData):
        print(f"PlayGamesServices : _on_get_remote_best_complete")
        scoreResult =  leaderboardScoreAnnotatedData.get()
        if scoreResult is not None:
            print(scoreResult.getDisplayRank())
            print(scoreResult.getDisplayScore())
            print(scoreResult.getScoreHolderDisplayName())
            remote_best = scoreResult.getRawScore()
            print(f"PlayGamesServices : Fetched remote best : {remote_best}")
            self.on_fetched_best(remote_best)
        else:
            print(f"PlayGamesServices : Fetched remote best error: scoreResult is None")
        leaderboardScoreAnnotatedData = None
     
    def _set_player(self, player):
        self.player = player
        print("PlayGamesServices : Successfully fetched player info")
        
    @run_on_ui_thread
    def submit_score(self, score):
        if self.player is not None:
            JavaBridge.PlayGames.getLeaderboardsClient(self.activity).submitScore(self.leaderboard_id, score);
            print(f"PlayGamesServices : {self.player.getDisplayName()} submitted a new high score : {score}")
        else:
            print("PlayGamesServices : No player info, can't submit highscore")
        
    @run_on_ui_thread
    def show_leaderboard(self):
        if not self.signed:
            print(f"PlayGamesServices : Try SignIn")
            JavaBridge.PlayGames.getGamesSignInClient(self.activity).signIn()
        else:
            print(f"PlayGamesServices : Queuing Showing LeaderBoard")
            JavaBridge.PlayGames.getLeaderboardsClient(self.activity).getLeaderboardIntent(self.leaderboard_id).addOnSuccessListener(OnSuccessListener(self._on_show_leaderboard_success))

    @run_on_ui_thread
    def get_remote_best(self, callback):
        print(f"PlayGamesServices : Queuing Get Remote Best")
        self.on_fetched_best = callback
        JavaBridge.PlayGames.getLeaderboardsClient(self.activity).loadCurrentPlayerLeaderboardScore(self.leaderboard_id, JavaBridge.LeaderboardVariant.TIME_SPAN_ALL_TIME, JavaBridge.LeaderboardVariant.COLLECTION_PUBLIC).addOnSuccessListener(OnSuccessListener(self._on_get_remote_best_success))
