"""
INFINITE RUNNER
6.177 Project (IAP 2016)
Completed by:
    Claire Nord   (cnord@mit.edu)
    Shavina Chau  (shavinac@mit.edu)
    Janelle Sands (jcsands@mit.edu)
"""

import pygame, sys

### Global Variables
WIDTH = 75  # this is the width of an individual square
HEIGHT = 75 # this is the height of an individual square

# RGB Color definitions
black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)
blue  = (0, 0, 255)

def get_row_top_loc(rowNum, height = HEIGHT):
    """
    Returns the location of the top pixel in a square in
    row rowNum, given the row height.
    """
    return rowNum * height + 10

def get_col_left_loc(colNum, width = WIDTH):
    """
    Returns the location of the leftmost pixel in a square in
    column colNum, given the column width.
    """
    return colNum * width + 10

def update_text(screen, message, size = 10):
    """
    Used to display the text on the right-hand part of the screen.
    You don't need to code anything, but you may want to read and
    understand this part.
    """
    textSize = 20
    font = pygame.font.Font(None, 20)
    textY = 0 + textSize
    text = font.render(message, True, white, black)
    textRect = text.get_rect()
    textRect.centerx = (size + 1) * WIDTH + 10
    textRect.centery = textY
    screen.blit(text, textRect)

def new_game(size = 10):
    """
    Sets up all necessary components to start a new game
    of Langton's Ant.
    """
    pygame.init() # initialize all imported pygame modules

    window_size = [size * WIDTH + 200, size * HEIGHT + 20] # width, height
    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption("Langton's Ant") # caption sets title of Window 

    board = Board(size)

    moveCount = 0

    clock = pygame.time.Clock()

    main_loop(screen, board, moveCount, clock, False, False)

def draw_grid(screen, size):
    """
    Draw the border grid on the screen.
    """
    #draw the vertical lines
    for i in range(size+1):
        start_pos_top = get_col_left_loc(i, WIDTH)
        pygame.draw.line(screen, red, (start_pos_top, 10), (start_pos_top, size*HEIGHT + 10), 1)

    #draw the horizontal lines
    for i in range(size+1):
        start_pos_left = get_row_top_loc(i, HEIGHT)
        pygame.draw.line(screen, red, (10, start_pos_left), (size*WIDTH + 10, start_pos_left), 1)

# Main program Loop: (called by new_game)
def main_loop(screen, board, moveCount, clock, stop, pause):
    board.squares.draw(screen) # draw Sprites (Squares)
    draw_grid(screen, board.size)
    board.theAnt.draw(screen) # draw ant Sprite
    pygame.display.flip() # update screen
    
    if stop == True:
        again = raw_input("Would you like to run the simulation again? If yes, type 'yes'\n")
        if again == 'yes':
            new_game()
    while stop == False:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #user clicks close
                stop = True
                pygame.quit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    if pause:
                        pause = False
                    else:
                        pause = True

        if stop == False and pause == False: 
            board.squares.draw(screen) # draw Sprites (Squares)
            # draw the grid here
            draw_grid(screen, board.size)
            board.theAnt.draw(screen) # draw ant Sprite
        
            update_text(screen, "Move #" + str(moveCount), board.size)
            pygame.display.flip() # update screen
            clock.tick(10)

            #--- Do next move ---#

            # Step 1: Rotate class Ant(pygame.sprite.Sprite):
            #rotate the ant and save its current square
            current_square = board.rotate_ant_get_square()
            board.squares.draw(screen) # draw Sprites (Squares) - they should cover up the ant's previous position
            # draw the grid here
            draw_grid(screen, board.size)
            board.theAnt.draw(screen) # draw ant Sprite (rotated)
            
            pygame.display.flip() # update screen
            clock.tick(5)
            
            # Step 2: Flip color of square:
            current_square.flip_color()
            board.squares.draw(screen) # draw Sprites (Squares) - they should cover up the ant's previous position
            # draw the grid here
            draw_grid(screen, board.size)
            board.theAnt.draw(screen) # draw ant Sprite (rotated)
            
            pygame.display.flip() #update screen
            clock.tick(5)
            
            # Step 3: Move Ant
            # make the ant step forward here
            board.ant.step_forward(board)
            board.squares.draw(screen) # draw Sprites (Squares) - they should cover up the ant's previous position
            # draw the grid here
            draw_grid(screen, board.size)

            board.theAnt.draw(screen) # draw ant Sprite (rotated)
            
            pygame.display.flip() # update screen
            clock.tick(5)
            
            moveCount += 1
            # ------------------------

    pygame.quit() # closes things, keeps idle from freezing

class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect() # gets a rect object with width and height specified above
                                          # a rect is a pygame object for handling rectangles
        self.rect.x = get_col_left_loc(col)
        self.rect.y = get_row_top_loc(row)
        self.color = color   

    def get_rect_from_square(self):
        """
        Returns the rect object that belongs to this Square
        """
        return self.rect

    def flip_color(self):
        """
        Flips the color of the square (white -> black or 
        black -> white)
        """
        if self.color == black:
            self.color = white
        else:
            self.color=black
        
        self.image.fill(self.color)
   
class Board:
    def __init__(self, size):

        self.size = size
        
        #---Initialize the Player---#
        self.player = Player(self,size/2,size/2)

        #---Adds Player to the "thePlayer" Sprite List---#
        self.thePlayer = pygame.sprite.RenderPlain()
        self.thePlayer.add(self.player)
    
    def move_down(self, row, col):
        pass
    
    def new_food(self, row, col):
        pass
    
    def new_obstacle(self, row, col):
        pass
        
    def remove_object(self, row, col):
        pass
        
    def update_board(self):
        pass
        
    def is_collision(self, player, items):
        pass
        
    def is_valid(self, section_of_grid):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self, board, col, row):
        pygame.sprite.Sprite.__init__(self)
        self.col = col
        self.row = row
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.board = board
        self.rect.x = get_col_left_loc(self.col)
        self.rect.y = get_row_top_loc(self.row)
        self.health=10
        
    def get_current_square(self):
        """
        Returns the square that the ant is currently on
        """
        return self.board.get_square(self.col, self.row)
   
    def get_location(self):
        #Returns the square? that the player is currently on? Returns rows and col?
        pass
        
    def move_left(self):
        #Moves the player one column to the left
        #If the Player is at an edge, the Player will not move off-screen or wrap around.
        self.col -= 1
    
        #actually changes player's location
        self.rect.x = get_col_left_loc(self.col)
        self.rect.y = get_row_top_loc(self.row)

    def move_right(self):
        #Moves the player one column to the right
        #If the Player is at an edge, the Player will not move off-screen or wrap around.
        self.col += 1
    
        #actually changes player's location
        self.rect.x = get_col_left_loc(self.col)
        self.rect.y = get_row_top_loc(self.row)

    def take_damage(self):
        #Decrease the health of the Player by a given amount if the Player collides with an Obstacle
        pass

    def increase_health(self):
        #Increase the health of the Player by a given amount if the Player collides with a Food
        pass

class Food (pygame.sprite.Sprite):
    def __init__ (self, board, col, nutrients):
        pass
        self.nutrients=nutrients
        self.image = pygame.image.load("strawberry.png").convert_alpha()
        self.col = col
        self.row = 0
        self.rect = self.image.get_rect()
        self.board = board
        self.rect.x = get_col_left_loc(self.col)
        self.rect.y = get_row_top_loc(self.row)

    def get_location():
        #return the location of the Food on the Board
        pass

    def effect():
        #will apply the effect of the powerup on the game
        pass
        
    def remove_from_board():
        #remove the Food object from the board after collision 
        #or after it travels "off-screen" i.e. out of the Board range

if __name__ == "__main__":
    # Uncomment this line to call new_game when this file is run:
    new_game()
    pass
