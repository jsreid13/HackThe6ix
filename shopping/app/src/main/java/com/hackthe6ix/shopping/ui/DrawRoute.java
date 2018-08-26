package com.hackthe6ix.shopping.ui;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.hackthe6ix.shopping.MainActivity;
import com.hackthe6ix.shopping.R;

import org.w3c.dom.Text;

import java.util.Vector;

public class DrawRoute extends View {
    Paint myPaint;
    Paint circle;
    Vector<Coord> myVect = new Vector<Coord>();
    TextView itemView;
    int[] coordinates = {0, 0};
//            {0, 1},
//            [0, 2],
//            [0, 3],
//            [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11], [0, 12], [0, 13], [0, 14], [0, 15], [0, 16], [1, 16], [2, 16], [3, 16], [4, 16], [5, 16], [6, 16], [7, 16], [8, 16], [9, 16], [10, 16], [11, 16], [12, 16], [13, 16], [14, 16], [15, 16], [16, 16], [17, 16], [18, 16]]}


    public DrawRoute(Context context) {
        super(context);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
//        itemView = (TextView) findViewById(R.id.textItems);
        CreateShoppingListActivity myItems = new CreateShoppingListActivity();
//        itemView.setText(myItems.items);
        for (int i = 0; i < 20; i++) {
            // a random line
            myVect.add(i, new Coord(Float.valueOf(i) * 50, Float.valueOf(i) * 80 + 17));

        }
        myPaint = new Paint();
        circle = new Paint();
        circle.setColor(Color.BLACK);
        myPaint.setColor(Color.GREEN);
        circle.setStrokeWidth(10f);
        myPaint.setStrokeWidth(10f);
        canvas.drawCircle(400,1220, 12f, myPaint);
        //beer
        myPaint.setColor(Color.RED);
        canvas.drawLine(400, 1220, 480, 1110, myPaint);
        canvas.drawLine(480, 1110, 480, 600, myPaint);
        canvas.drawCircle(480, 600, 10f, circle);
        //chips
        canvas.drawLine(480, 580, 480, 450, myPaint);
        canvas.drawLine(480, 450, 530, 450, myPaint);
        canvas.drawLine(530, 450, 530, 750, myPaint);
        canvas.drawCircle(530, 750, 10f, circle);
        //cookies
        canvas.drawLine(530, 750, 590, 1000, myPaint);
        canvas.drawCircle(590, 1000, 10f, circle);
        //Jam
        canvas.drawLine(590,1000,590,1250, myPaint);
        canvas.drawLine(590,1250, 825, 1250, myPaint);
        canvas.drawLine(825, 1250, 825,700, myPaint);
        canvas.drawCircle(825,700, 10f, circle);

//        canvas.drawLine(0,0, 500, 500, myPaint);
//        canvas.drawLine(500, 500, 250, 650, myPaint);
//        for(int i = 0; i < myVect.size() -1; i++) {
//            canvas.drawLine(myVect.get(i).x ,myVect.get(i).y, myVect.get(i + 1).x, myVect.get(i + 1).y, myPaint);
//        }
    }
}

class Coord {
    public float x;
    public float y;

    public Coord(float x_in, float y_in) {
        x = x_in;
        y = y_in;
    }
}
