try:
    from jnius import autoclass, PythonJavaClass, JavaClass, java_method
    from android.runnable import run_on_ui_thread #type: ignore
    from time import sleep
except:
    print("SIMPLEAM: Failed to load android and java modules.")
    raise ImportError

class JC:
    "Java & AdMob classes enumerator"
    View = autoclass("android.view.View")
    Activity = autoclass("org.kivy.android.PythonActivity")
    AdMobAdapter = autoclass("com.google.ads.mediation.admob.AdMobAdapter")
    AdRequestBuilder = autoclass("com.google.android.gms.ads.AdRequest$Builder")
    AdSize = autoclass("com.google.android.gms.ads.AdSize")
    AdView = autoclass("com.google.android.gms.ads.AdView")
    Bundle = autoclass("android.os.Bundle")
    Gravity = autoclass("android.view.Gravity")
    InterstitialAd = autoclass("com.google.android.gms.ads.interstitial.InterstitialAd")
    LayoutParams = autoclass("android.view.ViewGroup$LayoutParams")
    LinearLayout = autoclass("android.widget.LinearLayout")
    MobileAds = autoclass("com.google.android.gms.ads.MobileAds")
    # Some firebase callbacks mecanisms are abstract class which one cannot manage with pyjnius
    # In that case we have to provide our own java class that extends firebase api and can take an pythonizable interface as constructor parameter
    InterstitialAdLoadCallback = autoclass("com.pygameadmob.pygameadmobInterstitialAdLoadCallback") # instead of "com.google.android.gms.ads.interstitial.InterstitialAdLoadCallback"

def simpleam_init(app_id: str = None):
    """ Initializes AdMob MobileAds class. Use this function at the start to use all functionality. 
        \nTakes AdMob app id as an argument. Test app Ids is used if no argument was supplied"""
    app_id = app_id if app_id else "ca-app-pub-3940256099942544~3347511713"
    JC.MobileAds.initialize(JC.Activity.mActivity)

class AdObject:
    def __init__(self, ad_id):
        self.adUnitId = ad_id
        self.context = JC.Activity.mActivity
        self.admob_obj = None
        self.loaded = False
        self.loading = False

    @run_on_ui_thread
    def load_ad(self, filters: dict = {}) -> None:
        self.loaded = False
        self.loading = True
        self.admob_obj.loadAd(self.get_builder(filters).build())
        self.loaded = True
        
    def is_loaded(self) -> bool:
        return self.loaded
        
    def is_loading(self) -> bool:
        return self.loading
    
    @run_on_ui_thread
    def destroy(self) -> None:
        self.admob_obj.destroy()

    def get_builder(self, ad_filters: dict = {}) -> JC.AdRequestBuilder:
        " Builds ad depending on you're filters. "
        builder = JC.AdRequestBuilder()
        if ad_filters.get("children", None):
            builder.tagForChildDirectedTreatment(ad_filters["children"]) # Builds a child-friendly ad
        if ad_filters.get("family", None):
            extras = JC.Bundle()
            extras.putBoolean("is_designed_for_families", ad_filters["family"]) # Builds a family-friendly ad
            builder.addNetworkExtrasBundle(JC.AdMobAdapter, extras)
        return builder

class Banner(AdObject):
    " AdMob banner ad class. "
    @run_on_ui_thread
    def __init__(self, ad_id: str = "ca-app-pub-3940256099942544/6300978111", 
    			 position = "BOTTOM", size = "SMART_BANNER"):
        """ Banner has ability to create custom size. You can pass different arguments as position and size.
    		\nIf you want to use custom size - pass tuple as an argument with 2 integers.
            \n(Take in mind, some sizes might NOT work)
    		\nIf you want to use AdMob constant for position or size, you have to pass a string argument.
    		\nFor example: `simpleam.Banner("ad_id", position = "LEFT", size = "SMART_BANNER")`,
    		\nor: `simpleam.Banner("ad_id", position = "CENTER", size = (400, 200))`.
            \nBanner can take only custom size argument. Position always takes a constant.

    		\n**All banner size constants:**
    		\n- BANNER - 320x50;
    		\n- LARGE_BANNER - 320x100;
    		\n- MEDIUM_RECTANGLE - 300x250;
    		\n- FULL_BANNER - 468x60;
    		\n- LEADERBOARD - 728X90;
    		\n- SMART_BANNER - (Scales depending on the device screen);

    		\n**Standart banner position constants:**
    		\n- TOP; 
            \n- BOTTOM; 
            \n- LEFT; 
            \n- RIGHT;
            \n- CENTER.
            \n(For more check https://developer.android.com/reference/android/view/Gravity)"""
        super().__init__(ad_id)
        self.visible = False
        banner_position = getattr(JC.Gravity, position, JC.Gravity.BOTTOM)
        banner_size = size if isinstance(size, tuple) else getattr(JC.AdSize, size, JC.AdSize.SMART_BANNER)

        self.admob_obj = JC.AdView(JC.Activity.mActivity)
        self.admob_obj.setAdUnitId(self.AD_ID)
        self.admob_obj.setAdSize(banner_size)
        self.admob_obj.setVisibility(JC.View.GONE)
        adLayoutParams = JC.LayoutParams(JC.LayoutParams.MATCH_PARENT, JC.LayoutParams.WRAP_CONTENT)
        self.admob_obj.setLayoutParams(adLayoutParams)
        layout = JC.LinearLayout(JC.Activity.mActivity)
        layout.setGravity(banner_position)
        layout.addView(self.admob_obj)
        layoutParams = JC.LayoutParams(JC.LayoutParams.MATCH_PARENT, JC.LayoutParams.MATCH_PARENT)
        layout.setLayoutParams(layoutParams)
        JC.Activity.addContentView(layout, layoutParams)

    @run_on_ui_thread
    def set_visibility(self, visibility: bool = True) -> None:
        self.visible = visibility
        self.admob_obj.setVisibility(JC.View.VISIBLE if visibility else JC.View.GONE)

class Interstitial(AdObject):
    " AdMob interstitial ad class. "
    @run_on_ui_thread
    def __init__(self, ad_id: str = "ca-app-pub-3940256099942544/8691691433"):
        """ Interstitial has 2 variations which depend on AdMob ID.
    	    \nTEST image interstitial: `ca-app-pub-3940256099942544/1033173712`
    	    \nTEST video interstitial: `ca-app-pub-3940256099942544/8691691433`.
    	    \nIf no argument was supplied, interstitial would be ALWAYS image."""
        super().__init__(ad_id)
        self.callback = self.InterstitialAdLoadCallback(self.loaded_ad_callback, self.ad_failed_callback)
 
    class InterstitialAdLoadCallback(PythonJavaClass):
        "Callback to be invoked when an ad finishes loading."
        __javainterfaces__  = ("com.pygameadmob.pygameadmobInterstitialAdLoadCallbackInterface", )
        __javacontext__ = "app"

        def __init__(self, ad_loaded_callback, ad_failed_callback):
            self.ad_loaded_callback = ad_loaded_callback
            self.ad_failed_callback = ad_failed_callback

        @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
        def onAdFailedToLoad(self, loadAdError):
            self.ad_failed_callback(loadAdError)

        @java_method("(Lcom/google/android/gms/ads/interstitial/InterstitialAd;)V")
        def onAdLoaded(self, ad):
            self.ad_loaded_callback(ad)
        
    def loaded_ad_callback(self, ad):
        self.loading = False
        self.loaded = True
        self.admob_obj = ad
        
    def ad_failed_callback(self, error):
        self.loading = False
        self.loaded = False
        print('pygameadmob: Failed to load interstitial ad')
        print(error.toString())
        
    @run_on_ui_thread
    def load_ad(self, filters: dict = {}) -> None:
        self.loaded = False
        JC.InterstitialAd.load(self.context, self.adUnitId, self.get_builder(filters).build(),JC.InterstitialAdLoadCallback(self.callback))
        
    @run_on_ui_thread
    def show(self) -> None:
        if self.is_loaded():
            self.admob_obj.show(self.context)

class Rewarded(AdObject):
    " AdMob rewarded ad class. "
    @run_on_ui_thread
    def __init__(self, ad_id: str = "ca-app-pub-3940256099942544/5224354917"):
        """Rewarded ads need rewarded video listener.
           Video listener is used for checking events like `on_rewarded_succes` or `on_rewarded_loaded`
           \nIt should look like `RewardedCallbacks` class.
           \nYou have to set up it like this: `rewarded.set_listener(my_callback_listener)
        """
        super().__init__(ad_id)
        self.viewed_ad = False
        self.admob_obj = JC.MobileAds.getRewardedVideoAdInstance(JC.Activity.mActivity)
    
    @run_on_ui_thread
    def set_listener(self, callback_listener):
        self.rewarded_listener = RVListener(callback_listener, self)
        self.admob_obj.setRewardedVideoAdListener(self.rewarded_listener)

    @run_on_ui_thread
    def load_ad(self, filters: dict = {}) -> None:
        self.loaded = False
        self.admob_obj.loadAd(self.AD_ID, self.get_builder(filters).build())

    @run_on_ui_thread
    def _is_loaded(self) -> None:
        self.loaded = self.admob_obj.isLoaded()

    @run_on_ui_thread
    def _show(self) -> None:
        self.admob_obj.show()
        
    def is_loaded(self) -> bool:
        self._is_loaded()
        return self.loaded
    
    def show(self) -> None:
    	if self.is_loaded():
            while not self.viewed_ad:
                self._show()
                sleep(0.15)

class RVListener(PythonJavaClass):
    "AdMob revarded video listener class."
    __javainterfaces__ = ("com.google.android.gms.ads.reward.RewardedVideoAdListener", )
    __javacontext__ = "app"

    def __init__(self, reward_listener, rewarded_object):
        self._rewarded = rewarded_object
        self._listener = reward_listener

    @java_method("()V")
    def onRewardedVideoAdLoaded(self):
        self._rewarded.viewed_ad = False
        self._listener.on_rewarded_loaded()

    @java_method("()V")
    def onRewardedVideoAdOpened(self):
        self._listener.on_rewarded_opened()

    @java_method("()V")
    def onRewardedVideoStarted(self):
        self._listener.on_rewarded_load_fail

    @java_method("()V")
    def onRewardedVideoAdClosed(self):
        self._rewarded.viewed_ad = True
        self._listener.on_rewarded_closed()

    @java_method("(Lcom/google/android/gms/ads/reward/RewardItem;)V")
    def onRewarded(self, reward):
        self._listener.on_rewarded_success(reward)

    @java_method("()V")
    def onRewardedVideoAdLeftApplication(self):
        self._rewarded.viewed_ad = True
        self._listener.on_rewarded_left()

    @java_method("(I)V")
    def onRewardedVideoAdFailedToLoad(self, num):
        self._rewarded.viewed_ad = False
        self._listener.on_rewarded_load_fail(num)

class RewardedCallbacks:
    def on_rewarded_loaded(self):
        print("SIMPLEAM: Ad is loaded!")

    def on_rewarded_opened(self):
        print("SIMPLEAM: Ad is opened!")

    def on_rewarded_started(self):
        print("SIMPLEAM: Ad is started!")

    def on_rewarded_closed(self):
        print("SIMPLEAM: Ad closed!")

    def on_rewarded_success(self, reward):
        print(f"SIMPLEAM: Ad succesfully ended!")

    def on_rewarded_left(self):
        print("SIMPLEAM: Ad left application!")

    def on_rewarded_load_fail(self, num):
        print("SIMPLEAM: Ad failed to load!")
        


