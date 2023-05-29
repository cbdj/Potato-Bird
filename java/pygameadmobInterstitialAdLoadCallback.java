package com.pygameadmob;
import com.pygameadmob.pygameadmobInterstitialAdLoadCallbackInterface;
import com.google.android.gms.ads.interstitial.InterstitialAdLoadCallback;
import com.google.android.gms.ads.LoadAdError;
import com.google.android.gms.ads.interstitial.InterstitialAd;

public class pygameadmobInterstitialAdLoadCallback extends InterstitialAdLoadCallback{
	pygameadmobInterstitialAdLoadCallbackInterface python_callbacks;
	public pygameadmobInterstitialAdLoadCallback(pygameadmobInterstitialAdLoadCallbackInterface my_interface){
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