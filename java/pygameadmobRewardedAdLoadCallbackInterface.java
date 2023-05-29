package com.pygameadmob;
import com.google.android.gms.ads.LoadAdError;
import com.google.android.gms.ads.rewarded.RewardedAd;

public interface pygameadmobRewardedAdLoadCallbackInterface {

    public void onAdFailedToLoad(LoadAdError adError);
    public void onAdLoaded(RewardedAd adT);
}