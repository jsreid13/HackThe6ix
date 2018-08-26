package com.hackthe6ix.shopping;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import com.hackthe6ix.shopping.ui.CreateShoppingListActivity;

public class MainActivity extends AppCompatActivity {

    TextView myTextbox;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        myTextbox = (TextView)findViewById(R.id.mytext);
        myTextbox.setText("");

    }

    public void createShoppingList(View view) {
        Intent intent = new Intent(this, CreateShoppingListActivity.class);
        startActivity(intent);
    }
}
