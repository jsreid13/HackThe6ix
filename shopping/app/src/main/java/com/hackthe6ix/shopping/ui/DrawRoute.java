package com.hackthe6ix.shopping.ui;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.view.View;

import java.util.Vector;

public class DrawRoute extends View {
    Paint myPaint;
    Vector<Coord> myVect = new Vector<Coord>();

    public DrawRoute(Context context){
      super(context);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        for(int i = 0; i < 20; i++) {
            // a random line
            myVect.add(i, new Coord(Float.valueOf(i) * 50, Float.valueOf(i) * 80 + 17));

        }
        myPaint = new Paint();
        myPaint.setColor(Color.RED);
        myPaint.setStrokeWidth(10f);
        canvas.drawLine(0,0, 500, 500, myPaint);
        canvas.drawLine(500, 500, 250, 650, myPaint);
        for(int i = 0; i < myVect.size() -1; i++) {
            canvas.drawLine(myVect.get(i).x ,myVect.get(i).y, myVect.get(i + 1).x, myVect.get(i + 1).y, myPaint);
        }
    }
}

class Coord
{
    public float x;
    public float y;
    public Coord(float x_in, float y_in) {
        x = x_in;
        y = y_in;
    }
}
