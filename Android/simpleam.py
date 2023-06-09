from jnius import autoclass, PythonJavaClass, JavaClass, java_method
from android.runnable import run_on_ui_thread

TEST_BANNER_ID = "ca-app-pub-3940256099942544/6300978111"
TEST_INTERSTITIAL_ID = "ca-app-pub-3940256099942544/1033173712"
TEST_REWARDED_ID = "ca-app-pub-3940256099942544/5224354917"

class JavaBridge:
    View = autoclass("android.view.View")
    Activity = autoclass("org.kivy.android.PythonActivity")
    AdMobAdapter = autoclass("com.google.ads.mediation.admob.AdMobAdapter")
    AdRequestBuilder = autoclass("com.google.android.gms.ads.AdRequest$Builder")
    AdSize = autoclass("com.google.android.gms.ads.AdSize")
    AdView = autoclass("com.google.android.gms.ads.AdView")
    Bundle = autoclass("android.os.Bundle")
    Gravity = autoclass("android.view.Gravity")
    RewardedAd = autoclass("com.google.android.gms.ads.rewarded.RewardedAd")
    InterstitialAd = autoclass("com.google.android.gms.ads.interstitial.InterstitialAd")
    LayoutParams = autoclass("android.view.ViewGroup$LayoutParams")
    LinearLayout = autoclass("android.widget.LinearLayout")
    MobileAds = autoclass("com.google.android.gms.ads.MobileAds")
    # Since version 20.0 of play-services-ads some callbacks mecanisms are abstract class which pyjnius cannot manage
    # In that case we have to provide our own java class that extends admob api and can take a jnius-managed interface as constructor parameter
    AdListener = autoclass("com.simpleam.simpleamAdListener") # instead of "com.google.android.gms.ads.AdListener"
    InterstitialAdLoadCallback = autoclass("com.simpleam.simpleamInterstitialAdLoadCallback") # instead of "com.google.android.gms.ads.interstitial.InterstitialAdLoadCallback"
    RewardedAdLoadCallback = autoclass("com.simpleam.simpleamRewardedAdLoadCallback") # instead of "com.google.android.gms.ads.rewarded.RewardedAdLoadCallback"
    FullScreenContentCallback  = autoclass("com.simpleam.simpleamFullScreenContentCallback") # instead of "com.google.android.gms.ads.FullScreenContentCallback"
    
def simpleam_init():
    """ Initializes AdMob MobileAds class. Use this function at the start to use all functionality. 
        \nMake sure your APPLICATION_ID is set in your buildozer.spec like this:
        \nandroid.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713"""
    JavaBridge.MobileAds.initialize(JavaBridge.Activity.mActivity)

class AdObject:
    def __init__(self, ad_id):
        self.ad_id = ad_id
        self.context = JavaBridge.Activity.mActivity
        self.ad = None
        self._loaded = False
        self._loading = False

    @run_on_ui_thread
    def load_ad(self, filters: dict = {}) -> None:
        pass
    
    @run_on_ui_thread
    def destroy(self) -> None:
        self.ad.destroy()

    def is_loaded(self) -> bool:
        return self._loaded
        
    def is_loading(self) -> bool:
        return self._loading
        
    def get_builder(self, ad_filters: dict = {}) -> JavaBridge.AdRequestBuilder:
        "Creates an AdRequest contains targeting information used to fetch an ad"
        builder = JavaBridge.AdRequestBuilder()
        if ad_filters.get("children", None):
            builder.tagForChildDirectedTreatment(ad_filters["children"]) # Builds a child-friendly ad
        if ad_filters.get("family", None):
            extras = JavaBridge.Bundle()
            extras.putBoolean("is_designed_for_families", ad_filters["family"]) # Builds a family-friendly ad
            builder.addNetworkExtrasBundle(JavaBridge.AdMobAdapter, extras)
        return builder

class AdListener:
    def onAdClicked(self):
        print("simpleam: AdListener : onAdClicked")
    def onAdClosed(self):
        print("simpleam: AdListener : onAdClosed")
    def onAdFailedToLoad(self, adError):
        print(f"simpleam: AdListener : onAdFailedToLoad : {adError.toString()}")
    def onAdImpression(self):
        print("simpleam: AdListener : onAdImpression")
    def onAdLoaded(self):
        print("simpleam: AdListener : onAdLoaded")
    def onAdOpened(self):
        print("simpleam: AdListener : onAdOpened")
    def onAdSwipeGestureClicked(self):
        print("simpleam: AdListener : onAdSwipeGestureClicked")

class Banner(AdObject, PythonJavaClass):
    " AdMob banner ad class. "
    __javainterfaces__ = ("com.simpleam.simpleamAdListenerInterface", )
    __javacontext__ = "app"
    @run_on_ui_thread
    def __init__(self, ad_id: str = TEST_BANNER_ID, position = "BOTTOM", size = "SMART_BANNER"):
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
        self.ad = JavaBridge.AdView(JavaBridge.Activity.mActivity)
        self.ad.setAdUnitId(self.ad_id)
        self.ad.setAdSize(size if isinstance(size, tuple) else getattr(JavaBridge.AdSize, size, JavaBridge.AdSize.SMART_BANNER))
        self.ad.setVisibility(JavaBridge.View.GONE)
        self.adListener = AdListener()
        self.ad.setAdListener(JavaBridge.AdListener(self))
        adLayoutParams = JavaBridge.LayoutParams(JavaBridge.LayoutParams.MATCH_PARENT, JavaBridge.LayoutParams.WRAP_CONTENT)
        self.ad.setLayoutParams(adLayoutParams)
        layout = JavaBridge.LinearLayout(JavaBridge.Activity.mActivity)
        layout.setGravity(getattr(JavaBridge.Gravity, position, JavaBridge.Gravity.BOTTOM))
        layout.addView(self.ad)
        layoutParams = JavaBridge.LayoutParams(JavaBridge.LayoutParams.MATCH_PARENT, JavaBridge.LayoutParams.MATCH_PARENT)
        layout.setLayoutParams(layoutParams)
        self.context.addContentView(layout, layoutParams)
        self.visibility = False;

    @java_method("()V")
    def onAdClicked (self):
        self.adListener.onAdClicked()
    @java_method("()V")
    def onAdClosed(self):
        self._loaded = False
        self.adListener.onAdClosed()
    @java_method("(Lcom/google/android/gms/ads/LoadAdError;)V")
    def onAdFailedToLoad(self, adError):
        self._loaded = False
        self._loading = False
        self.adListener.onAdFailedToLoad(adError)
    @java_method("()V")
    def onAdImpression(self):
        self.adListener.onAdImpression()
    @java_method("()V")
    def onAdLoaded(self):
        self._loaded = True
        self._loading = False
        self.adListener.onAdLoaded()
    @java_method("()V")
    def onAdOpened(self):
        self.adListener.onAdOpened()
    @java_method("()V")
    def onAdSwipeGestureClicked(self):
        self.adListener.onAdSwipeGestureClicked()
      
    @run_on_ui_thread
    def load_ad(self, filters: dict = {}) -> None:
        self._loaded = False
        self.ad.loadAd(self.get_builder(filters).build())
        self._loading = True
        
    @run_on_ui_thread
    def _get_visibility(self) -> None:
        self.visibility = self.ad.getVisibility() == JavaBridge.View.VISIBLE
        
    def get_visibility(self) -> bool:
        self._get_visibility()
        return self.visibility
        
    @run_on_ui_thread
    def _set_visibility(self, visibility: bool = True) -> None:
        self.ad.setVisibility(JavaBridge.View.VISIBLE if visibility else JavaBridge.View.GONE)
        
    def set_visibility(self, visibility: bool = True) -> None:
        self._set_visibility(visibility)
        self.visibility = True
        
    def setAdListener(self, adListener : AdListener):
        self.adListener = AdListener

class Interstitial(AdObject, PythonJavaClass):
    " AdMob interstitial ad class. "
    __javainterfaces__  = ("com.simpleam.simpleamInterstitialAdLoadCallbackInterface", )
    __javacontext__ = "app"
    def __init__(self, ad_id: str = TEST_INTERSTITIAL_ID):
        """ Interstitial has 2 variations which depend on AdMob ID.
    	    \nTEST image interstitial: `ca-app-pub-3940256099942544/1033173712`
    	    \nTEST video interstitial: `ca-app-pub-3940256099942544/8691691433`.
    	    \nIf no argument was supplied, interstitial would be ALWAYS image."""
        super().__init__(ad_id)

    @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
    def onAdFailedToLoad(self, loadAdError):
        self._loading = False
        self._loaded = False
        print('simpleam: Failed to load interstitial ad')
        print(loadAdError.toString())

    @java_method("(Lcom/google/android/gms/ads/interstitial/InterstitialAd;)V")
    def onAdLoaded(self, ad):
        self._loading = False
        self.ad = ad
        self._loaded = True
        
    @run_on_ui_thread
    def load_ad(self, filters: dict = {}) -> None:
        self._loaded = False
        JavaBridge.InterstitialAd.load(self.context, self.ad_id, self.get_builder(filters).build(),JavaBridge.InterstitialAdLoadCallback(self))
        self._loading = True
        
    @run_on_ui_thread
    def show(self) -> None:
        if self.is_loaded():
            self.ad.show(self.context)

class FullScreenContentCallbacks:
    def onAdClicked (self):
        print("simpleam: FullScreenContentCallbacks : onAdClicked")
    def onAdDismissedFullScreenContent(self):
        print("simpleam: FullScreenContentCallbacks : onAdDismissedFullScreenContent")
    def onAdFailedToShowFullScreenContent(self, adError):
        print(f"simpleam: FullScreenContentCallbacks : onAdFailedToShowFullScreenContent : {adError.toString()}")
    def onAdImpression(self):
        print("simpleam: FullScreenContentCallbacks : onAdImpression")
    def onAdShowedFullScreenContent(self):
        print("simpleam: FullScreenContentCallbacks : onAdShowedFullScreenContent")

class PaidEventCallbacks:
    def onPaidEvent(self, value):
        print(f"simpleam: PaidEventCallbacks : onPaidEvent : code : {value.getCurrencyCode()}, precision : {value.getPrecisionType()}, value: {value.getValueMicros()}")      
        
class OnUserEarnedRewardCallbacks:
    def onUserEarnedReward(self, reward):
        print(f"simpleam: OnUserEarnedRewardCallbacks : onUserEarnedReward : amount : {reward.getAmount()}, type  : {reward.getType()}")      


class Rewarded(AdObject, PythonJavaClass):
    " AdMob rewarded ad class. "
    __javainterfaces__ = (
        "com.google.android.gms.ads.OnPaidEventListener",
        "com.google.android.gms.ads.OnUserEarnedRewardListener",
        "com.simpleam.simpleamFullScreenContentCallbackInterface",
        "com.simpleam.simpleamRewardedAdLoadCallbackInterface", 
    )
    __javacontext__ = "app"
    def __init__(self, ad_id: str = TEST_REWARDED_ID):
        """Rewarded ads need multiple callbacks/listener : FullScreenContentCallbacks, PaidEventCallbacks, OnUserEarnedRewardCallbacks"
           \nLook at https://developers.google.com/android/reference/com/google/android/gms/ads/rewarded/RewardedAd for more information
           \nYou can provide your own implementations using set_FullScreenContentCallbacks, set_OnUserEarnedRewardListener, set_OnPaidEventListener
        """
        super().__init__(ad_id)
        self._full_screen_content_callback = FullScreenContentCallbacks()
        self._user_earned_reward_listener = OnUserEarnedRewardCallbacks()
        self._paid_event_listener = PaidEventCallbacks()   

    @java_method("(Lcom/google/android/gms/ads/AdValue;)V")
    def onPaidEvent(self, value):
        self._paid_event_listener.onPaidEvent(value)

    @java_method("(Lcom/google/android/gms/ads/rewarded/RewardItem;)V")
    def onUserEarnedReward(self, reward):
        self._user_earned_reward_listener.onUserEarnedReward(reward)

    @java_method("()V")
    def onAdClicked (self):
        self._full_screen_content_callback.onAdClicked()
    @java_method("()V")
    def onAdDismissedFullScreenContent(self):
        self._full_screen_content_callback.onAdDismissedFullScreenContent()
    @java_method("(Lcom/google/android/gms/ads/AdError;)V")
    def onAdFailedToShowFullScreenContent(self, adError):
        self._full_screen_content_callback.onAdFailedToShowFullScreenContent(adError)
    @java_method("()V")
    def onAdImpression(self):
        self._full_screen_content_callback.onAdImpression()
    @java_method("()V")
    def onAdShowedFullScreenContent(self):
        self._full_screen_content_callback.onAdShowedFullScreenContent()

    @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
    def onAdFailedToLoad(self, loadAdError):
        self.loading = False
        self.loaded = False
        print(loadAdError.toString())
 
    @java_method("(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V")
    def onAdLoaded(self, ad):
        self._loading = False
        self.ad = ad
        self.ad.setFullScreenContentCallback(JavaBridge.FullScreenContentCallback(self))
        self.ad.setOnPaidEventListener(self)
        self._loaded = True
                
    def set_FullScreenContentCallbacks(self, callbacks: FullScreenContentCallbacks):
        self._full_screen_content_callback = callbacks
        
    def set_OnUserEarnedRewardListener(self, callback: OnUserEarnedRewardCallbacks):
        self._user_earned_reward_listener = callback
        
    def set_OnPaidEventListener(self, callback: PaidEventCallbacks):
        self._paid_event_listener = callback
        
    @run_on_ui_thread
    def load_ad(self, filters: dict = {}) -> None:
        self._loaded = False
        JavaBridge.RewardedAd.load(self.context, self.ad_id, self.get_builder(filters).build(),JavaBridge.RewardedAdLoadCallback(self))
        self._loading = True
        
    @run_on_ui_thread
    def show(self) -> None:
        if self.is_loaded():
            self.ad.show(self.context, self)
        

