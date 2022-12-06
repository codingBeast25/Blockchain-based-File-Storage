final color BLACK = color(0);
final color GREEN = color(0, 255, 0);
final color YELLOW  = color(255, 255, 0);
final color BLUE = color(0, 0, 255);

PGraphics pg;

void setup() {
  size(100, 100);
  pg = createGraphics(100, 100);
}

void draw() {
  pg.beginDraw();
  pg.background(0, 0); // fully transparent background, the point of doing this

  // put the origin at the center of the screen and direct the y axis upward
  pg.pushMatrix();
  pg.translate(width/2, height/2);
  pg.scale(1, -1);
  drawShapes();
  pg.popMatrix();

  pg.endDraw();
  image(pg, 0, 0);
  pg.save("Transparent.png");
  noLoop();
}

// a selection of shapes to demonstrate the syntax
// pg.beginShape(), pg.vertex(), pg.endShape() will also work

void drawShapes() {
  pg.stroke(BLACK);
  pg.fill(YELLOW);
  pg.rect(0, 0, width/3, height/3);
  pg.fill(GREEN);
  pg.triangle(-width/3, height/3, -width/3, -height/3, width/3, -height/3);
  pg.fill(BLUE);
  pg.ellipse(0, 0, width/4, width/4);
}
