package com.hackthe6ix.shopping;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;

import com.hackthe6ix.shopping.datatransfer.MapInit;
import com.hackthe6ix.shopping.ui.CreateShoppingListActivity;

public class MainActivity extends AppCompatActivity {
    ViewGroup group;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        group = (ViewGroup) getWindow().getDecorView();
        Draw draw = new Draw(this);
        group.addView(draw);

//        maybeEnableArButton();
//        MapInit map_grid = new MapInit();

    }

    public void createShoppingList(View view) {
        Intent intent = new Intent(this, CreateShoppingListActivity.class);
        startActivity(intent);
    }
}
