package com.simpleam;
import com.google.android.gms.ads.LoadAdError;
import com.google.android.gms.ads.interstitial.InterstitialAd;

public interface simpleamInterstitialAdLoadCallbackInterface {

    public void onAdFailedToLoad(LoadAdError adError);
    public void onAdLoaded(InterstitialAd adT);
}