final float TILE_WIDTH = 50; // width of one tile

class Tile
{
  
  float tile_height; // height of one tile (randomly selected)
  float[] c; // color of each tile
  
  // constructor
  Tile(float[] clr)
  {
    tile_height = random(9.7,10); // height of the tile would be between 0 to 0.3 (this variable is second z position other than farZ)
    c = clr; // color of the tile
  }
  
  // draw each tile with given color
  void draw()
  {
     pushMatrix();
     fill(color(c[0], c[1], c[2]));
     drawCube();
     popMatrix();
  }
  
  void setColor(float[] clr)
  {
    c = clr;
  }
  
   //<>//
  
  void drawCube() {
    
    noStroke();
    beginShape(QUADS);
    
    // Z = -1 // original color
    vertex(TILE_WIDTH, 0, tile_height);
    vertex(0, 0, tile_height);
    vertex(0, TILE_WIDTH, tile_height);
    vertex(TILE_WIDTH, TILE_WIDTH, tile_height);
    
    // Z = 1 // original color
    vertex(0, 0, farZ);
    vertex(0, TILE_WIDTH, farZ);
    vertex(TILE_WIDTH, TILE_WIDTH, farZ);
    vertex(TILE_WIDTH,0, farZ);
  
    
    // light shady color for other faces of tile (feature for Question 2)
    fill(color(c[0]*0.75 , c[1]*0.75, c[2]*0.75));
    
    // Y = 1
    vertex(0, TILE_WIDTH, farZ);
    vertex(TILE_WIDTH, TILE_WIDTH, farZ);
    vertex(TILE_WIDTH, TILE_WIDTH, tile_height);
    vertex(0, TILE_WIDTH, tile_height);
    
    // X = 1
    vertex(TILE_WIDTH, 0, farZ);
    vertex(TILE_WIDTH, 0, tile_height);
    vertex(TILE_WIDTH, TILE_WIDTH, tile_height);
    vertex(TILE_WIDTH, TILE_WIDTH, farZ);
  
    // X = -1
    vertex(0, 0, tile_height);
    vertex(0, 0, farZ);
    vertex(0, TILE_WIDTH, farZ);
    vertex(0, TILE_WIDTH,tile_height);
  
    // Y = -1
    vertex(TILE_WIDTH, 0, farZ);
    vertex(0, 0, farZ);
    vertex(0, 0, tile_height);
    vertex(TILE_WIDTH, 0, tile_height);
    
    endShape();
  }
  
}
