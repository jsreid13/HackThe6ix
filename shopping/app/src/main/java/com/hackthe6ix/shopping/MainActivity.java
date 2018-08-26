package com.hackthe6ix.shopping;

import android.app.Activity;
import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.VectorDrawable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Display;
import android.widget.ImageView;

public class MainActivity extends Activity {
    Draw draw;
    ImageView myImg;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        draw = new Draw(this);

        draw.setBackgroundColor(Color.TRANSPARENT);
        setContentView(draw);
        loadImage();



    }

    void loadImage(){
        Resources res = getResources();
        Drawable drawable = res.getDrawable(R.drawable.ic_map);
        VectorDrawable vectorDrawable =  (VectorDrawable) drawable;
    }

}
