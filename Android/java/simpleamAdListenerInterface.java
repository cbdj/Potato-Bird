package com.simpleam;
import com.google.android.gms.ads.LoadAdError;

public interface simpleamAdListenerInterface {
    public void onAdClicked();
    public void onAdClosed();
    public void onAdFailedToLoad(LoadAdError adError);
    public void onAdImpression();
    public void onAdLoaded();
    public void onAdOpened();
    public void onAdSwipeGestureClicked();
}