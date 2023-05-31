package com.pygameadmob;
import com.google.android.gms.ads.LoadAdError;

public interface pygameadmobAdListenerInterface {
    public void onAdClicked();
    public void onAdClosed();
    public void onAdFailedToLoad(LoadAdError adError);
    public void onAdImpression();
    public void onAdLoaded();
    public void onAdOpened();
    public void onAdSwipeGestureClicked();
}