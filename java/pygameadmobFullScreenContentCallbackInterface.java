package com.pygameadmob;
import com.google.android.gms.ads.AdError;

public interface pygameadmobFullScreenContentCallbackInterface {
    public void onAdClicked ();
    public void onAdDismissedFullScreenContent();
    public void onAdFailedToShowFullScreenContent(AdError adError);
    public void onAdImpression ();
    public void onAdShowedFullScreenContent ();
}