package com.simpleam;
import com.simpleam.simpleamRewardedAdLoadCallbackInterface;
import com.google.android.gms.ads.rewarded.RewardedAdLoadCallback;
import com.google.android.gms.ads.LoadAdError;
import com.google.android.gms.ads.rewarded.RewardedAd;

public class simpleamRewardedAdLoadCallback extends RewardedAdLoadCallback{
	simpleamRewardedAdLoadCallbackInterface python_callbacks;
	public simpleamRewardedAdLoadCallback(simpleamRewardedAdLoadCallbackInterface my_interface){
		python_callbacks = my_interface;
	}
    @Override
    public void onAdFailedToLoad(LoadAdError adError){
		python_callbacks.onAdFailedToLoad(adError);
        return;
	}
	
	@Override
    public void onAdLoaded(RewardedAd adT){
		python_callbacks.onAdLoaded(adT);
        return;
	}
}