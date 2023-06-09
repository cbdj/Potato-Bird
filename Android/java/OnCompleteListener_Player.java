package com.cldejessey;
import com.google.android.gms.games.Player;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.cldejessey.OnCompleteListener_PlayerInterface;

public class OnCompleteListener_Player implements OnCompleteListener<Player> {
	OnCompleteListener_PlayerInterface python_callbacks;
	public OnCompleteListener_Player(OnCompleteListener_PlayerInterface my_interface){
		python_callbacks = my_interface;
	}
    public void onComplete(Task<Player> task){
        python_callbacks.onComplete(task.getResult());
    }
}
