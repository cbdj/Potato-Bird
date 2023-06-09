package com.simpleam;
import com.google.android.gms.ads.AdError;

public interface simpleamFullScreenContentCallbackInterface {
    public void onAdClicked ();
    public void onAdDismissedFullScreenContent();
    public void onAdFailedToShowFullScreenContent(AdError adError);
    public void onAdImpression ();
    public void onAdShowedFullScreenContent ();
}