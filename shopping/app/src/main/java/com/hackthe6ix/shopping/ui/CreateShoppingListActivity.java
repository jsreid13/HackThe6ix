package com.hackthe6ix.shopping.ui;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.hackthe6ix.shopping.MainActivity;
import com.hackthe6ix.shopping.R;
import com.hackthe6ix.shopping.utils.JsonGen;

import java.util.Arrays;
import java.util.Vector;

public class CreateShoppingListActivity extends AppCompatActivity {
    public String shopping_list = "Shopping List:";
    public Vector<String> shopping_list_vec = new Vector<String>();
    public TextView s_l;
    public static Vector<String> item_list_vec = new Vector<String>();
    public String items = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_itemsearch);
        String[] item_list_arr = {
                "deli meats",
                "beer",
                "wine",
                "soda",
                "chips",
                "cookies",
                "crackers",
                "bottled juice",
                "canned juice",
                "asceptics",
                "isotonics",
                "candy",
                "popcorn",
                "snack nuts",
                "snacks",
                "bread",
                "tortillas",
                "pastries",
                "condiments",
                "pickles",
                "vinegar",
                "salad dressing",
                "peanut butter",
                "jam",
                "jelly",
                "canned meat",
                "rice",
                "dried beans",
                "goya",
                "jalapenoes",
                "picante",
                "pasta",
                "pasta sauce",
                "canned tomatoes",
                "canned pasta",
                "gravy mix",
                "canned beans",
                "dried fruit",
                "canned fruit",
                "deli",
                "bakery",
                "flowers",
                "market",
                "seafood",
                "apple"
        };
        item_list_vec.addAll(Arrays.asList(item_list_arr));
    }

    public void addShoppingList(View view) {
        EditText barContent = (EditText) findViewById(R.id.itemSearchBar);
        String new_item = barContent.getText().toString().toLowerCase();
        barContent.getText().clear();
        if (item_list_vec.contains(new_item)) {
            shopping_list_vec.add(new_item);
            shopping_list = shopping_list + "\n" + new_item;
            s_l = (TextView) findViewById(R.id.shoppingList);
            s_l.setText(shopping_list);
            items = items + shopping_list;
        }
        else {
            Toast.makeText(getApplicationContext(), "Item entered not available!", Toast.LENGTH_LONG).show();
        }
        Toast.makeText(this, items, Toast.LENGTH_LONG);
    }

    public void submitShoppingList(View view) {
        Intent intent = new Intent(this, DisplayRouteActivity.class);
        try {
            Thread.sleep(1000);
            startActivity(intent);
        }catch (Exception e){

        }
//        JsonGen new_submit = new JsonGen(shopping_list_vec);
//        boolean success = new_submit.generateJsonFromVector();
//        if (success) {
//            shopping_list_vec.clear();
//            shopping_list = "Shopping List submitted";
//            s_l = (TextView) findViewById(R.id.shoppingList);
//            s_l.setText(shopping_list);
//            Toast.makeText(getApplicationContext(), "Shopping List submission succeed!", Toast.LENGTH_LONG).show();
//            Intent intent = new Intent(this, DisplayRouteActivity.class);
//            startActivity(intent);
//        }
//        else {
//            Toast.makeText(getApplicationContext(), "Shopping List submission failed!", Toast.LENGTH_LONG).show();
//        }
    }
}
