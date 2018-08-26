package com.hackthe6ix.shopping.ui;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import com.hackthe6ix.shopping.R;

import java.util.Random;

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

        Random rand = new Random();
        int rand_int = rand.nextInt(25) + 1;
        String rand_item = CreateShoppingListActivity.item_list_vec.get(rand_int);
        String rand_item_2 = CreateShoppingListActivity.item_list_vec.get(rand_int+2);
        Button rec_item_1 = (Button) findViewById(R.id.recom_item_1);
        rec_item_1.setText(rand_item);
        Button rec_item_2 = (Button) findViewById(R.id.recom_item_2);
        rec_item_2.setText(rand_item_2);
    }
}