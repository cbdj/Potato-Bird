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
    def __init__(self):
        self.activity = JavaBridge.Activity.mActivity
        JavaBridge.PlayGamesSdk.initialize(self.activity)
        self.gamesSignInClient = JavaBridge.PlayGames.getGamesSignInClient(self.activity);
        isAuthenticatedTask = OnCompleteListener_AuthenticationResult(self._on_signin_complete)
        self.gamesSignInClient.isAuthenticated().addOnCompleteListener(JavaBridge.OnCompleteListener_AuthenticationResult(isAuthenticatedTask))
        self.signed = False
        self.player = None
        
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
    def _on_show_leaderboard_complete(self, intent):
        print(f"PlayGamesServices : Beforre Showing LeaderBoard")
        self.activity.startActivityForResult(intent, 9004);
        print(f"PlayGamesServices : Showing LeaderBoard")
     
    def _set_player(self, player):
        self.player = player
        print("PlayGamesServices : Successfully fetched player info")
        
    @run_on_ui_thread
    def submit_score(self, score):
        JavaBridge.PlayGames.getLeaderboardsClient(self.activity).submitScore(Settings.LEADERBOARD_ID, score);
        print(f"PlayGamesServices : {self.player.getDisplayName()} submitted a new high score : {score}")
        
    @run_on_ui_thread
    def show_leaderboard(self):
        print(f"PlayGamesServices : Queuing Showing LeaderBoard")
        JavaBridge.PlayGames.getLeaderboardsClient(self.activity).getLeaderboardIntent(Settings.LEADERBOARD_ID).addOnSuccessListener(OnSuccessListener(self._on_show_leaderboard_complete) )
