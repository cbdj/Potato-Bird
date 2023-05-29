package com.pygameadmob;
import com.pygameadmob.pygameadmobRewardedAdLoadCallbackInterface;
import com.google.android.gms.ads.rewarded.RewardedAdLoadCallback;
import com.google.android.gms.ads.LoadAdError;
import com.google.android.gms.ads.rewarded.RewardedAd;

public class pygameadmobRewardedAdLoadCallback extends RewardedAdLoadCallback{
	pygameadmobRewardedAdLoadCallbackInterface python_callbacks;
	public pygameadmobRewardedAdLoadCallback(pygameadmobRewardedAdLoadCallbackInterface my_interface){
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