package rs.etf.dna.stellaris_wireless;

import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.PrintWriter;
import java.net.Socket;

public class MainActivity extends AppCompatActivity {
    protected String ipAddr;
    Button connectButton;
    NetworkTask networktask;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        connectButton = (Button)findViewById(R.id.button);
        final TextView ipField = (TextView)findViewById(R.id.editText);


        connectButton.setOnClickListener(new Button.OnClickListener(){
            public void onClick(View v){
                ipAddr = ipField.getText().toString();
                networktask.execute();
                connectButton.setEnabled(false);
                ipField.setEnabled(false);
            }
        });
        Button disconnectButton = (Button)findViewById(R.id.button2);
        disconnectButton.setOnClickListener(new Button.OnClickListener(){
            public void onClick(View v){
                try {
                    networktask.closeConn();
                    connectButton.setEnabled(true);
                    ipField.setEnabled(true);
                }catch(Exception e){
                    e.printStackTrace();
                }
            }
        });
        Button leftTurn = (Button) findViewById(R.id.button5);
        leftTurn.setOnTouchListener(new Button.OnTouchListener(){
            public boolean onTouch(View v, MotionEvent theMotion){
                switch(theMotion.getAction()){
                    case MotionEvent.ACTION_DOWN:
                        networktask.sendDataToNetwork('a');
                        break;
                    case MotionEvent.ACTION_UP:
                        networktask.sendDataToNetwork('x');
                        break;
                }
                return true;
            }
        });
        Button upTurn = (Button) findViewById(R.id.button3);
        upTurn.setOnTouchListener(new Button.OnTouchListener(){
            public boolean onTouch(View v, MotionEvent theMotion){
                switch(theMotion.getAction()){
                    case MotionEvent.ACTION_DOWN:
                        networktask.sendDataToNetwork('w');
                        break;
                    case MotionEvent.ACTION_UP:
                        networktask.sendDataToNetwork('x');
                        break;
                }
                return true;
            }
        });
        Button rightTurn = (Button) findViewById(R.id.button7);
        rightTurn.setOnTouchListener(new Button.OnTouchListener(){
            public boolean onTouch(View v, MotionEvent theMotion){
                switch(theMotion.getAction()){
                    case MotionEvent.ACTION_DOWN:
                        networktask.sendDataToNetwork('d');
                        break;
                    case MotionEvent.ACTION_UP:
                        networktask.sendDataToNetwork('x');
                        break;
                }
                return true;
            }
        });
        Button downTurn = (Button) findViewById(R.id.button4);
        downTurn.setOnTouchListener(new Button.OnTouchListener(){
            public boolean onTouch(View v, MotionEvent theMotion){
                switch(theMotion.getAction()){
                    case MotionEvent.ACTION_DOWN:
                        networktask.sendDataToNetwork('s');
                        break;
                    case MotionEvent.ACTION_UP:
                        networktask.sendDataToNetwork('x');
                        break;
                }
                return true;
            }
        });
        Button rotLeftTurn = (Button) findViewById(R.id.button6);
        rotLeftTurn.setOnTouchListener(new Button.OnTouchListener(){
            public boolean onTouch(View v, MotionEvent theMotion){
                switch(theMotion.getAction()){
                    case MotionEvent.ACTION_DOWN:
                        networktask.sendDataToNetwork('A');
                        break;
                    case MotionEvent.ACTION_UP:
                        networktask.sendDataToNetwork('x');
                        break;
                }
                return true;
            }
        });
        Button rotRightTurn = (Button) findViewById(R.id.button8);
        rotRightTurn.setOnTouchListener(new Button.OnTouchListener(){
            public boolean onTouch(View v, MotionEvent theMotion){
                switch(theMotion.getAction()){
                    case MotionEvent.ACTION_DOWN:
                        networktask.sendDataToNetwork('D');
                        break;
                    case MotionEvent.ACTION_UP:
                        networktask.sendDataToNetwork('x');
                        break;
                }
                return true;
            }
        });
        Button accelerate = (Button)findViewById(R.id.button9);
        accelerate.setOnClickListener(new Button.OnClickListener(){
            public void onClick(View v){
                networktask.sendDataToNetwork('+');
            }
        });
        Button decelerate = (Button)findViewById(R.id.button10);
        decelerate.setOnClickListener(new Button.OnClickListener(){
            public void onClick(View v){
                networktask.sendDataToNetwork('-');
            }
        });
        Button stop = (Button)findViewById(R.id.button11);
        stop.setOnClickListener(new Button.OnClickListener(){
            public void onClick(View v){
                networktask.sendDataToNetwork('x');
            }
        });
        networktask = new NetworkTask();
    }

    private class NetworkTask extends AsyncTask<Void, byte[], Boolean> {
        Socket nsocket; //Network Socket
        PrintWriter pw;
        @Override
        protected Boolean doInBackground(Void... param) { //This runs on a different thread
            boolean result = false;
            int port = 4001;
            try {
                Log.i("AsyncTask", "doInBackground: Creating socket");
                nsocket = new Socket(ipAddr, port);
                if (nsocket.isConnected()) {
                    pw = new PrintWriter(nsocket.getOutputStream(), true);
                    Log.i("AsyncTask", "doInBackground: Socket created, streams assigned");
                }
            } catch (Exception e) {
                e.printStackTrace();
                Log.i("AsyncTask", "doInBackground: Exception");
                result = true;
            } finally {
                Log.i("AsyncTask", "doInBackground: Finished");
            }
            return result;
        }
        boolean closeConn() {
            if(nsocket.isConnected()) {
                Log.i("AsyncTask", "CloseConn: Closing connection.");
                new Thread(new Runnable(){
                    public void run(){
                        try {
                            pw.close();
                            nsocket.close();

                        }catch(Exception e) {
                            Log.i("AsyncTask", "CloseConn failed.");
                        }
                    }
                }).start();

            }
            return true;
        }
        boolean sendDataToNetwork(final char c) {
                if (nsocket.isConnected())
                {
                    Log.i("AsyncTask", "SendDataToNetwork: Writing received message to socket");
                    new Thread(new Runnable()
                    {
                        public void run()
                        {
                            try
                            {
                                pw.write(c);
                                pw.flush();
                            }
                            catch (Exception e)
                            {
                                e.printStackTrace();
                                Log.i("AsyncTask", "SendDataToNetwork: Message send failed. Caught an exception");
                            }
                        }
                    }).start();

                    return true;
                }

                Log.i("AsyncTask", "SendDataToNetwork: Cannot send message. Socket is closed");
                return false;
            }
        }
}
