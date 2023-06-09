package com.cldejessey;
import com.google.android.gms.games.AuthenticationResult;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.cldejessey.OnCompleteListener_AuthenticationResultInterface;

public class OnCompleteListener_AuthenticationResult implements OnCompleteListener<AuthenticationResult> {
	OnCompleteListener_AuthenticationResultInterface python_callbacks;
	public OnCompleteListener_AuthenticationResult(OnCompleteListener_AuthenticationResultInterface my_interface){
		python_callbacks = my_interface;
	}
    public void onComplete(Task<AuthenticationResult> task){
        python_callbacks.onComplete(task.getResult());
    }
}
