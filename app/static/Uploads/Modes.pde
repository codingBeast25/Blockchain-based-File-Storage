final char KEY_VIEW = 'r'; // switch between orthographic and perspective views
final char KEY_PAUSE = 'p';

// player character
final char KEY_LEFT = 'a';
final char KEY_RIGHT = 'd';
final char KEY_UP = 'w';
final char KEY_DOWN = 's';
final char KEY_SHOOT = ' ';

// useful for debugging to turn textures or collisions on/off
final char KEY_TEXTURE = 't';
final char KEY_COLLISION = 'c';

final char KEY_BONUS = 'b';

boolean doBonus = false;
boolean doTextures = false;
boolean doCollision = false;

boolean isOrtho = true;
boolean isGridMoving =  true;

boolean moveLeft = false;
boolean moveRight = false;
boolean moveUp = false;
boolean moveDown = false;

void keyPressed()
{
  
  if(key == KEY_VIEW) // to change view
  {
    if(isOrtho)
    {
      eye.z =  8.5;
      window_edge_offset = 60;
      setProjection(projectPerspective);
      isOrtho = false;
    }
    else
    {
      eye.z = 0;
      window_edge_offset = 0;
      setProjection(projectOrtho);
      isOrtho = true;
    }
    
  }
  
  if (key == KEY_PAUSE)
  {
    isGridMoving = !isGridMoving;
  }
  
  if (key == KEY_UP)
  {
    moveUp = true;
  }
  
  if (key == KEY_DOWN)
  {
    moveDown = true;
  }
  
  if (key == KEY_LEFT)
  {
    moveLeft = true;
  }
  if (key == KEY_RIGHT)
  {
    moveRight = true;
  }
  
  if(key == KEY_SHOOT)
  {
    bullet_arr.add(new Bullet(p));
  }
}

void keyReleased() {
  if(key == KEY_UP)
  {
    moveUp = false;
    angleX = 0;
  }
  if (key == KEY_DOWN)
  {
    moveDown = false;
    angleX = 0;
  }
  if (key == KEY_LEFT)
  {
    moveLeft = false;
    angleY = 0;
  }
  if (key == KEY_RIGHT)
  {
    moveRight = false;
    angleY = 0;
  }
}
