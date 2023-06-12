import Settings
from jnius import autoclass, PythonJavaClass, JavaClass, java_method
from android.runnable import run_on_ui_thread

class JavaBridge:
    PlayGamesSdk = autoclass("com.google.android.gms.games.PlayGamesSdk")
    PlayGames = autoclass("com.google.android.gms.games.PlayGames")
    Activity = autoclass("org.kivy.android.PythonActivity")
    OnCompleteListener_AuthenticationResult = autoclass("com.cldejessey.OnCompleteListener_AuthenticationResult")
    OnCompleteListener_String = autoclass("com.cldejessey.OnCompleteListener_String")
    OnCompleteListener_Player = autoclass("com.cldejessey.OnCompleteListener_Player")
    LeaderboardVariant = autoclass("com.google.android.gms.games.leaderboard.LeaderboardVariant")
    
class OnCompleteListener_String(PythonJavaClass):
    " AdMob banner ad class. "
    __javainterfaces__ = ("com.cldejessey.OnCompleteListener_StringInterface", )
    __javacontext__ = "app"
    def __init__(self, callback):
        self.callback = callback
        pass
    @java_method('(Lutil/lang/String;)V')
    def onComplete(self, result):
        print(result)
        self.callback(result)
        
class OnCompleteListener_Player(PythonJavaClass):
    " AdMob banner ad class. "
    __javainterfaces__ = ("com.cldejessey.OnCompleteListener_PlayerInterface", )
    __javacontext__ = "app"
    def __init__(self, callback):
        self.callback = callback
        pass
    @java_method('(Lcom/google/android/gms/games/Player;)V')
    def onComplete(self, result):
        print(result)
        self.callback(result)
    
class OnCompleteListener_AuthenticationResult(PythonJavaClass):
    " AdMob banner ad class. "
    __javainterfaces__ = ("com.cldejessey.OnCompleteListener_AuthenticationResultInterface", )
    __javacontext__ = "app"
    def __init__(self, on_signin_complete):
        self.on_signin_complete = on_signin_complete
        pass
    @java_method('(Lcom/google/android/gms/games/AuthenticationResult;)V')
    def onComplete(self, result):
        print(result.isAuthenticated())
        self.on_signin_complete(result.isAuthenticated())
        
class OnSuccessListener(PythonJavaClass):
    __javainterfaces__ = ("com.google.android.gms.tasks.OnSuccessListener", )
    __javacontext__ = "app"
    def __init__(self, callback):
        self.callback = callback
        pass
    @java_method('(Ljava/lang/Object;)V')
    def onSuccess(self, obj):
        self.callback(obj)

    
class PlayGamesServices():
    @run_on_ui_thread
    def __init__(self, leaderboard_id):
        self.activity = JavaBridge.Activity.mActivity
        JavaBridge.PlayGamesSdk.initialize(self.activity)
        self.gamesSignInClient = JavaBridge.PlayGames.getGamesSignInClient(self.activity);
        isAuthenticatedTask = OnCompleteListener_AuthenticationResult(self._on_signin_complete)
        self.gamesSignInClient.isAuthenticated().addOnCompleteListener(JavaBridge.OnCompleteListener_AuthenticationResult(isAuthenticatedTask))
        self.signed = False
        self.player = None
        self.leaderboard_id = leaderboard_id
        self.on_fetched_best = None
        
    @run_on_ui_thread
    def _on_signin_complete(self, result):
        if not result:
            self.signed = False
            print("PlayGamesServices : Failed GooglePlay signin")
            # add a button whom callback does self.gamesSignInClient.signIn()
        else:
            self.signed = True
            getPlayersClient = OnCompleteListener_Player(self._set_player)
            JavaBridge.PlayGames.getPlayersClient(self.activity).getCurrentPlayer().addOnCompleteListener(JavaBridge.OnCompleteListener_Player(getPlayersClient))
            print("PlayGamesServices : Successful GooglePlay signin")
            
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
        JavaBridge.PlayGames.getLeaderboardsClient(self.activity).submitScore(self.leaderboard_id, score);
        if self.player is not None:
            print(f"PlayGamesServices : {self.player.getDisplayName()} submitted a new high score : {score}")
        else:
            print("PlayGamesServices : No player info, can't submit highscore")
        
    @run_on_ui_thread
    def show_leaderboard(self):
        if not self.signed:
            print(f"PlayGamesServices : Try SignIn")
            self.gamesSignInClient.signIn()
        else:
            print(f"PlayGamesServices : Queuing Showing LeaderBoard")
            JavaBridge.PlayGames.getLeaderboardsClient(self.activity).getLeaderboardIntent(self.leaderboard_id).addOnSuccessListener(OnSuccessListener(self._on_show_leaderboard_success))

    @run_on_ui_thread
    def get_remote_best(self, callback):
        print(f"PlayGamesServices : Queuing Get Remote Best")
        self.on_fetched_best = callback
        leaderboards_client = JavaBridge.PlayGames.getLeaderboardsClient(self.activity).loadCurrentPlayerLeaderboardScore(self.leaderboard_id, JavaBridge.LeaderboardVariant.TIME_SPAN_ALL_TIME, JavaBridge.LeaderboardVariant.COLLECTION_PUBLIC)
        leaderboards_client.addOnSuccessListener(OnSuccessListener(self._on_get_remote_best_success))
