package com.hackthe6ix.shopping.datatransfer;

import java.util.Vector;

public class MapInit
{
    public Vector<Grid> map_grid_info;

    public void MapInit() {
        map_grid_info = new Vector<Grid>(1155);  // 33 rows, 35 cols
        for (int i = 0; i < 33; i++) {
            for (int j = 0; j < 35; j++) {
                map_grid_info.add(new Grid(i, j));
            }
        }
        
        changeGridToShelf(2, 6, 5, 5);
        changeGridToShelf(9, 15, 5, 5);
        changeGridToShelf(17, 24, 5, 5);
        changeGridToShelf(26, 26, 0, 5);
        changeGridToShelf(3, 4, 10, 10);
        changeGridToShelf(7, 8, 10, 10);
        changeGridToShelf(11, 14, 10, 10);
        changeGridToShelf(16, 18, 9, 11);
        changeGridToShelf(21, 22, 9, 11);
        changeGridToShelf(4, 5, 15, 27);
        changeGridToShelf(3, 4, 32, 33);

        changeGridToShelf(8, 31, 15, 15);
        changeGridToShelf(8, 31, 18, 19);
        changeGridToShelf(8, 31, 22, 22);
        changeGridToShelf(8, 31, 25, 26);
        changeGridToShelf(8, 31, 29, 30);
        changeGridToShelf(8, 31, 32, 33);

        changeGridToItem(7, 6, "Bakery");
        changeGridToItem(14, 15, "Wine");
        changeGridToItem(28, 25, "Candy");
        changeGridToItem(13, 29, "Peanut Butter");
        changeGridToItem(4, 32, "Canned Tomatoes");
        changeGridToItem(22, 32, "Seafood");

        // call the API to upload the gridmap
        
    }

    public void changeGridToShelf(int x_start, int x_end, int y_start, int y_end) {
        for (int i = x_start; i <= x_end; i++) {
            for (int j = y_start; j <= y_end; j++) {
                map_grid_info.get(35*i + j).type = GridType.SHELF;
            }
        }
    }

    public void changeGridToItem(int x, int y, String name) {
        map_grid_info.get(35*x + y).type = GridType.ITEM;
        map_grid_info.get(35*x + y).item_name = name;
    }
}

class Grid
{
    public int row;
    public int col;
    GridType type;
    public String item_name;
    public Grid(int row_in, int col_in) {
        row = row_in;
        col = col_in;
        type = GridType.PASSAGE;
        item_name = "";
    }
}
