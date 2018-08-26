package com.hackthe6ix.shopping;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;

public class MainActivity extends AppCompatActivity {
    ViewGroup group;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        group = (ViewGroup) getWindow().getDecorView();
        Draw draw = new Draw(this);
        group.addView(draw);

    }
}
