package com.hackthe6ix.shopping;

import android.content.Context;
import android.content.res.Configuration;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.AppCompatImageView;
import android.util.AttributeSet;
import android.util.DisplayMetrics;
import android.view.View;
import android.view.WindowManager;
import android.widget.ImageView;
import android.widget.Toast;

public class Draw extends View {

    Paint paint = new Paint();
    Toast toast;
    private Context context = getContext();
    CharSequence text = "Drew Line";
    Configuration config = getResources().getConfiguration();
    int screenWidthDp = config.screenWidthDp;
    int screenHeightDp = config.screenHeightDp;
    int smallestScreenWidthDp = config.smallestScreenWidthDp;

    int height;
    int width;

    private void init() {
        paint.setColor(Color.BLACK);
    }

    public Draw(Context context) {
        super(context);
        init();
    }

    public Draw(Context context, AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    public Draw(Context context, AttributeSet attrs, int defStyle) {
        super(context, attrs, defStyle);
        init();
    }


    public void onDraw(Canvas canvas) {
        paint.setStrokeWidth(10f);
        for(int i = 0; i < 200; i++){
            canvas.drawLine(i, i, i+1 , i + 1, paint);
        }
//        canvas.drawLine(0, 0, 1080, 1920, paint);
//        canvas.drawLine(0, 0, 0, 200, paint);


        Toast toast = Toast.makeText(context, ("height: " + screenHeightDp  + " width: "+ screenWidthDp), Toast.LENGTH_LONG);
        toast.show();
    }


}
