package com.simpleam;
import com.simpleam.simpleamInterstitialAdLoadCallbackInterface;
import com.google.android.gms.ads.interstitial.InterstitialAdLoadCallback;
import com.google.android.gms.ads.LoadAdError;
import com.google.android.gms.ads.interstitial.InterstitialAd;

public class simpleamInterstitialAdLoadCallback extends InterstitialAdLoadCallback{
	simpleamInterstitialAdLoadCallbackInterface python_callbacks;
	public simpleamInterstitialAdLoadCallback(simpleamInterstitialAdLoadCallbackInterface my_interface){
		python_callbacks = my_interface;
	}
    @Override
    public void onAdFailedToLoad(LoadAdError adError){
		python_callbacks.onAdFailedToLoad(adError);
        return;
	}
	
	@Override
    public void onAdLoaded(InterstitialAd adT){
		python_callbacks.onAdLoaded(adT);
        return;
	}
}