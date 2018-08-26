package com.hackthe6ix.shopping.ui;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.ViewGroup;
import android.widget.TextView;

import com.hackthe6ix.shopping.R;

public class DisplayRouteActivity extends AppCompatActivity {
    public ViewGroup v_group;
    TextView itemView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_drawroute);

        v_group = (ViewGroup) getWindow().getDecorView();
        DrawRoute draw = new DrawRoute(this);
        v_group.addView(draw);
    }
}