package com.pygameadmob;
import com.pygameadmob.pygameadmobFullScreenContentCallbackInterface;
import com.google.android.gms.ads.FullScreenContentCallback;
import com.google.android.gms.ads.AdError;

public class pygameadmobFullScreenContentCallback extends FullScreenContentCallback{
	pygameadmobFullScreenContentCallbackInterface python_callbacks;
	public pygameadmobFullScreenContentCallback(pygameadmobFullScreenContentCallbackInterface my_interface){
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