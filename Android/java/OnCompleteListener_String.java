package com.cldejessey;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.cldejessey.OnCompleteListener_StringInterface;

public class OnCompleteListener_String implements OnCompleteListener<String> {
	OnCompleteListener_StringInterface python_callbacks;
	public OnCompleteListener_String(OnCompleteListener_StringInterface my_interface){
		python_callbacks = my_interface;
	}
    public void onComplete(Task<String> task){
        python_callbacks.onComplete(task.getResult());
    }
}
