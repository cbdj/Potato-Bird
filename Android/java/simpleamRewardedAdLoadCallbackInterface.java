package com.simpleam;
import com.google.android.gms.ads.LoadAdError;
import com.google.android.gms.ads.rewarded.RewardedAd;

public interface simpleamRewardedAdLoadCallbackInterface {

    public void onAdFailedToLoad(LoadAdError adError);
    public void onAdLoaded(RewardedAd adT);
}