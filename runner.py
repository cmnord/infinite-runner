"""
INFINITE RUNNER
6.177 Project (IAP 2016)
Completed by:
    Claire Nord   (cnord@mit.edu)
    Shavina Chau  (shavinac@mit.edu)
    Janelle Sands (jcsands@mit.edu)
"""

"""
***** Langton's Ant *****
"""

# Algorithm described at http://en.wikipedia.org/wiki/Langton%27s_ant

import pygame, sys
import tests as T

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
        
        #---Initializes Squares (the "Board")---#
        self.squares = pygame.sprite.RenderPlain()
        self.boardSquares = []
        
        #---Populate boardSquares with Squares---#
        for rows in range(size):
            columns = []
            for cols in range(size):
                #initialize squares
                s = Square(rows, cols, white)
                #add them to the squares group
                columns.append(s)
                self.squares.add(s)
            #add columns list to boardSquares list to create 2d array
            self.boardSquares.append(columns)

        #---Initialize the Ant---#
        self.ant = Ant(self, size/2, size/2)
                          
        #---Adds Ant to the "theAnt" Sprite List---#
        self.theAnt = pygame.sprite.RenderPlain()
        self.theAnt.add(self.ant)

    def get_square(self, x, y):
        """
        Given an (x, y) pair, return the Square at that location
        """
        return self.boardSquares[y][x]

    def rotate_ant_get_square(self):
        """ 
        Rotate the ant, depending on the color of the square that it's on,
        and returns the square that the ant is currently on
        """
        if self.ant.get_current_square().color == black:
            self.ant.rotate_left()
        if self.ant.get_current_square().color == white:
            self.ant.rotate_right()
        return self.ant.get_current_square()

class Ant(pygame.sprite.Sprite):
    def __init__(self, board, col, row):
        pygame.sprite.Sprite.__init__(self)
        self.col = col
        self.row = row
        self.set_pic()
        self.rect = self.image.get_rect()
        self.rotation = (0, 1) # pointing up
        self.board = board
        self.rect.x = get_col_left_loc(self.col)
        self.rect.y = get_row_top_loc(self.row)
        
    def get_current_square(self):
        """
        Returns the square that the ant is currently on
        """
        return self.board.get_square(self.col, self.row)
   
    def rotate_left(self):
        #Rotates the ant 90 degrees counterclockwise
        self.image = pygame.transform.rotate(self.image, 90)
        self.rotation = (-1 * self.rotation[1], self.rotation[0])
        

    def rotate_right(self):
        #Rotates the ant 90 degrees clockwise
        self.image = pygame.transform.rotate(self.image, -90)
        self.rotation = (self.rotation[1], -1 * self.rotation[0])
    
    
    
    def step_forward(self, board):
        """
        Make the ant take a step forward in whatever direction it's currently pointing.
        Don't forget - row numbers increase from top to bottom and column numbers
        increase from left to right!
        """
        self.col += self.rotation[0]
        self.row -= self.rotation[1]

        #actually changes ant's location
        self.rect.x = get_col_left_loc(self.col)
        self.rect.y = get_row_top_loc(self.row)
    
    def set_pic(self):
        """
        Sets the picture that represents our Ant.
        If you want to use a new picture, you'll need to change
        this method.
        """
        self.image = pygame.image.load("ant.png").convert_alpha()

if __name__ == "__main__":
    # Uncomment this line to call new_game when this file is run:
    new_game()
    
    pass
