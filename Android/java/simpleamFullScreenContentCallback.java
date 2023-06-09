package com.simpleam;
import com.simpleam.simpleamFullScreenContentCallbackInterface;
import com.google.android.gms.ads.FullScreenContentCallback;
import com.google.android.gms.ads.AdError;

public class simpleamFullScreenContentCallback extends FullScreenContentCallback{
	simpleamFullScreenContentCallbackInterface python_callbacks;
	public simpleamFullScreenContentCallback(simpleamFullScreenContentCallbackInterface my_interface){
		python_callbacks = my_interface;
	}
    @Override
    public void onAdClicked (){
		python_callbacks.onAdClicked();
        return;
	}
	@Override
    public void onAdDismissedFullScreenContent(){
		python_callbacks.onAdDismissedFullScreenContent();
        return;
	}
	@Override
    public void onAdFailedToShowFullScreenContent(AdError adError){
		python_callbacks.onAdFailedToShowFullScreenContent(adError);
        return;
	}
	@Override
    public void onAdImpression (){
		python_callbacks.onAdImpression ();
        return;
	}
	@Override
    public void onAdShowedFullScreenContent (){
		python_callbacks.onAdShowedFullScreenContent();
        return;
	}
}