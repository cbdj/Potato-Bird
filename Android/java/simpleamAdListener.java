package com.simpleam;
import com.simpleam.simpleamAdListenerInterface;
import com.google.android.gms.ads.AdListener;
import com.google.android.gms.ads.LoadAdError;

public class simpleamAdListener extends AdListener{
	simpleamAdListenerInterface python_callbacks;
	public simpleamAdListener(simpleamAdListenerInterface my_interface){
		python_callbacks = my_interface;
	}
    @Override
    public void onAdClicked(){
		python_callbacks.onAdClicked ();
        return;
	}
    @Override
    public void onAdClosed(){
		python_callbacks.onAdClosed();
        return;
	}
    @Override
    public void onAdFailedToLoad(LoadAdError adError){
		python_callbacks.onAdFailedToLoad(adError);
        return;
	}
	@Override
    public void onAdImpression(){
		python_callbacks.onAdImpression();
        return;
	}
	@Override
    public void onAdLoaded(){
		python_callbacks.onAdLoaded();
        return;
	}
	@Override
    public void onAdOpened(){
		python_callbacks.onAdOpened();
        return;
	}
	@Override
    public void onAdSwipeGestureClicked(){
		python_callbacks.onAdSwipeGestureClicked();
        return;
	}
}