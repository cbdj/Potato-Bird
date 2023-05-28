package com.pygameadmob;
import com.google.android.gms.ads.LoadAdError;
import com.google.android.gms.ads.interstitial.InterstitialAd;

public interface pygameadmobInterstitialAdLoadCallbackInterface {

    public void onAdFailedToLoad(LoadAdError adError);
    public void onAdLoaded(InterstitialAd adT);
}