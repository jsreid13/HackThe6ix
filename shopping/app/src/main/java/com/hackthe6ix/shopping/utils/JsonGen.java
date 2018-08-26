package com.hackthe6ix.shopping.utils;

import android.content.Context;

import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Vector;

import java.io.FileWriter;
import java.io.IOException;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

public class JsonGen
{
    Vector<String> submit_shopping_list = new Vector<String>();
    public JsonGen(Vector<String> shopping_list) {
        submit_shopping_list = shopping_list;
    }

    public boolean generateJsonFromVector() {
        JSONObject obj = new JSONObject();
//        obj.put("Name", "Shopping list items");

        JSONArray shopping_list_json = new JSONArray();
        for (int i = 0; i < submit_shopping_list.size(); i++)
            shopping_list_json.add(submit_shopping_list.get(i));
        obj.put("Shopping List", shopping_list_json);

//        String filePath = ctx.getFilesDir().getPath().toString() + "/fileName.json";
        String filePath = "sdcard/fileName.json";
        try (FileWriter file = new FileWriter(filePath)) {
            file.write(obj.toJSONString());
            System.out.println("Successfully Copied JSON Object to File...");
            System.out.println("\nJSON Object: " + obj);
            // call API to submit the json file

            return true;
        }
        catch (java.io.IOException e) {
            System.err.println("IOException: " + e.getMessage());
            return false;
        }
    }

    public boolean uploadJsonFile() {
        try {
            URL url = new URL("http://");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        }
        catch (Exception e) {
            e.printStackTrace();
        }
        return true;
    }
}