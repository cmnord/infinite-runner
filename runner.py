"""
INFINITE RUNNER
6.177 Project (IAP 2016)
Completed by:
    Claire Nord   (cnord@mit.edu)
    Shavina Chau  (shavinac@mit.edu)
    Janelle Sands (jcsands@mit.edu)
    Michelle Chen (mxchen@mit.edu)
"""

import pygame, sys
import random
from example_menu import main as menu
from losers_menu import main as losers_menu

### Global Variables
WIDTH = 75  # this is the width of an individual square
HEIGHT = 75 # this is the height of an individual square
NUM_ROWS = 8 #number of rows
NUM_COLS = 4 #number of columns

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

def update_text(screen, message):
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
    textRect.centerx = (NUM_COLS + 1) * WIDTH + 10
    textRect.centery = textY
    screen.blit(text, textRect)

def new_game():
    """
    Sets up all necessary components to start a new game.
    """
    pygame.init() # initialize all imported pygame modules

    window_size = [ NUM_COLS * WIDTH + 200, NUM_ROWS * HEIGHT + 20] # width, height
    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption("Infinite Runner") # caption sets title of Window 

    board = Board()

    moveCount = 0

    clock = pygame.time.Clock()
    #Menu function
    result = menu(screen)
    if result == 0: #THIS MEANS USER SELECTED START GAME
        main_loop(screen, board, moveCount, clock, False, False)
    elif result == 1: #USER SELECTED LOAD GAME
        print "you can't load games -- yet!"
    elif result == 2: #USER SELETED OPTIONS
        print "you have no options -- yet!"

def draw_grid(screen):
    """
    Draw the border grid on the screen.
    """
    #draw the vertical lines
    for i in range(NUM_COLS + 1):
        start_pos_top = get_col_left_loc(i, WIDTH)
        pygame.draw.line(screen, red, (start_pos_top, 10), (start_pos_top, NUM_ROWS*HEIGHT + 10), 1)

    #draw the horizontal lines
    for i in range(NUM_ROWS+1):
        start_pos_left = get_row_top_loc(i, HEIGHT)
        pygame.draw.line(screen, red, (10, start_pos_left), (NUM_COLS*WIDTH + 10, start_pos_left), 1)

# Main program Loop: (called by new_game)
def main_loop(screen, board, moveCount, clock, stop, pause):
    board.squares.draw(screen) # draw Sprites (Squares)
    draw_grid(screen)
    board.thePlayer.draw(screen) # draw player Sprite
    board.theItems.draw(screen)
    pygame.display.flip() # update screen

   
    #how to quit the game
    if stop == True:
        again = raw_input("Would you like to play again? If yes, type 'yes'\n")
        if again == 'yes':
            new_game()

    while stop == False:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #user clicks close
                stop = True
                pygame.quit()
            #how to pause the game, move player right, and move player left
            elif event.type==pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                        board.player.move_right()
                        draw_grid(screen)
                        board.theItems.draw(screen)
                        board.thePlayer.draw(screen)
                elif event.key == pygame.K_LEFT:
                        board.player.move_left()
                        draw_grid(screen)
                        board.theItems.draw(screen)
                        board.thePlayer.draw(screen)
                elif event.key==pygame.K_p:
                    if pause:
                        pause = False
                    else:
                        pause = True
        
        if stop == False and pause == False and board.player.health>0: 
            #print random_number
            board.squares.draw(screen) # draw Sprites (Squares)
            # draw the grid here
            draw_grid(screen)
            board.thePlayer.draw(screen) # draw player Sprite
            board.theItems.draw(screen)
            update_text(screen, "Total meters traveled: " + str(moveCount) +"H: " + str(board.player.health))
            pygame.display.flip() # update screen
            clock.tick(10)
            moveCount += 1
            
            # ------------------------
            if moveCount % 10 == 0:
                #print "Move down!!!"
                board.update_board() #will progress everything 1 row down
                board.squares.draw(screen) # draw Sprites (Squares)
                draw_grid(screen)
                board.thePlayer.draw(screen) # draw player Sprite
                board.theItems.draw(screen)
                pygame.display.flip()

        if board.player.health<=0:
            result = losers_menu(screen)
            pygame.display.flip()
            if result == 0: #THIS MEANS USER SELECTED YOU LOSE
                print ":("
            elif result == 1: #USER SELECTED NEW GAME
                board.player.modify_health(10)
                main_loop(screen, board, moveCount, clock, False, False)
            elif result == 2: #USER SELETED OPTIONS
                print "you have no options -- yet!"       
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
   
class Board(object):
    def __init__(self):
        self.rows = NUM_ROWS
        self.cols = NUM_COLS
        self.items = [] #a list of every food and obstacle object
                        #new items created (at the top) will be appended
        
        #---Initializes Squares (the "Board")---#
        self.squares = pygame.sprite.RenderPlain()
        self.boardSquares = []
        
        #---Populate boardSquares with Squares---#
        for i in range(self.rows): #rows in 2d array
            col = []
            for j in range(self.cols): #cols #j=col, i=row
                s = Square(i,j,white)
                col.append(s)
                self.squares.add(s)
            self.boardSquares.append(col)
            
        #---Initialize the Player---#
        self.player = Player(self,1) #board, col=1, row=bottom row (default value)

        #---Adds Player to the "thePlayer" Sprite List---#
        self.thePlayer = pygame.sprite.RenderPlain()
        self.thePlayer.add(self.player)

        self.theItems = pygame.sprite.RenderPlain()
        #Sprite group for items
    
    def move_down(self):
        """
        Probably unneeded now; everything is in move_down in item class
        """
        pass
    
    def new_food(self, col, nutrients=1):
        """
        Will create a Food object at the location (row=0, col)
        """
        self.boardSquares[0][col] = Food(self,col, nutrients)
        self.items.append(self.boardSquares[0][col])
        self.theItems.add(self.boardSquares[0][col]) #adds to sprite group
        return self.boardSquares[0][col]
        #nutrients = how much it heals
    
    def new_obstacle(self, col, power=1):
        """
        Will create an Obstacle object at the location (row, col)
        """
        self.boardSquares[0][col] = Obstacle(self, col, power)
        self.items.append(self.boardSquares[0][col])
        self.theItems.add(self.boardSquares[0][col]) #adds to sprite group
        return self.boardSquares[0][col]
        #power = how much damage it deals
        
    def remove_object(self, row, col):
        """
        Will remove the object at the location (row, col)
        "Remove" = replace with a white Square object
        """
        pass
        
    def update_board(self):
        """
        Will call move_down on every square in the grid
        """
        new_items = []
        self.theItems = pygame.sprite.RenderPlain()
        for item in self.items: #items = list of obstacles and food
            if(item.move_down(self.player)):
                #if move_down returns true, it has moved and stays on the board
                new_items.append(item)
                self.theItems.add(item)

        self.items = new_items
        #Now everything has been moved down, leaving first row empty
        
        #Filling in the now-vacant first row
        self.generate_new_row() 
        #gen_new_row takes a probability list as an optional argument
        #when initializing new items, automatically adds to items list and sprite group
        
        #Refilling the squares ----
        self.squares = pygame.sprite.RenderPlain()
        self.boardSquares = []
        
        for i in range(self.rows): #rows in 2d array
            col = []
            for j in range(self.cols): #cols #j=col, i=row
                s = Square(i,j,white)
                col.append(s)
                self.squares.add(s)
            self.boardSquares.append(col)
        
        #Adding the self.items list into the boardSquares array
        for k in self.items:
            location = k.get_location() #returns a list
            self.boardSquares[location[0]][location[1]] = k  
                    
    def generate_new_row(self, probability_list=[.30,.10]):
        """
        Takes in a list of probabilities [% obstacle, % food] and generates
        a row with those probabilities
        Returns a list
        """
        #probability_list = percent chance of getting an obstacle, food
        new_row = []
        for i in range(4):
            rand_num = random.random()
            if rand_num <= probability_list[0]: #probability of obstacle
                new_row.append(self.new_obstacle(i))
            elif rand_num <= probability_list[0]+probability_list[1]: #prob of food
                new_row.append(self.new_food(i))
            else: #prob of neither (blank square)
                continue
        #print len(new_row), "items in first row"
        #return new_row
    
    def is_valid(self, section_of_grid):
        """
        Check if a section of grid is passable
        """
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self, board, col, row=NUM_ROWS-1):
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
        Returns the square that the player is currently on
        """
        return self.board.get_square(self.col, self.row)
   
    def get_location(self):
        """
        Returns a list (rows,cols) of the player's location
        """

        return [self.row, self.col]
        
    def move_left(self):
        """
        Moves the player one column to the left 
        If the Player is at an edge, the Player will not move off-screen or wrap around.
        """
        if self.col>0: #not in the leftmost column
            self.col -= 1
        #actually changes player's location
        self.rect.x = get_col_left_loc(self.col)
        self.rect.y = get_row_top_loc(self.row)

    def move_right(self):
        """
        Moves the player one column to the right
        If the Player is at an edge, the Player will not move off-screen or wrap around.
        """
        if self.col<3: #not in rightmost column
            self.col += 1
    
        #actually changes player's location
        self.rect.x = get_col_left_loc(self.col)
        self.rect.y = get_row_top_loc(self.row)

    def modify_health(self,potency): #get the potency from the check_potency method
        #Increase/decrease the health of the Player by the amount of potency of the object it collides with
        self.health += potency
        print 'health', self.health 

    """
    def check_potency (self,objs): #objs is a list
                    #receives object in the list of the objects at the bottom row
                    #We only care about the square that the player is on.  So get player location.  If there's an object there that's a Food or Obstacle, then get potency of item and modify health.
                        item = objs[self.col]
                        if isinstance(item,Food) or isinstance(item,Obstacle): #Objs is a list being passed to us.  If nothing there, it's just a Square.
                            self.modify_health(item.get_potency()) #Modify player health
    """

class Item(pygame.sprite.Sprite):
    def __init__(self, board, col, row=0):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.rect = self.image.get_rect()
        self.board = board
        self.rect.x = get_col_left_loc(self.col)
        self.rect.y = get_row_top_loc(self.row)
        self.potency = 1

    def get_location(self):
    	#note: using this for modify_health method in Player class
        return list([self.row, self.col]) #returns the coordinates of the item in a list, e.g. [0, 1]

    def get_potency(self): #returns the item potency for the modify_health method in Player class
    	return self.potency 

    def move_down(self, player):
        #print "Got to the move_down function!"
        if self.get_location() == player.get_location():
            player.modify_health(self.potency)
            self.remove_item() 
            #print "Collision!"
            return False
        if self.get_location()[0] >= NUM_ROWS-1: #if in row 7, remove
            self.remove_item()
            #print "Out of bounds!"
            return False
        else:
            self.row += 1
            self.rect.y = get_row_top_loc(self.row)
            return True
    
    def remove_item(self):
        pass

class Obstacle(Item):
    def __init__(self, board, col, power):
        self.image = pygame.image.load("tourist.png").convert_alpha()
        super(Obstacle, self).__init__(board, col)
        self.power = power
        self.potency = power * -1

class Food (Item):
    def __init__ (self, board, col, nutrients):
        self.image = pygame.image.load("strawberry.png").convert_alpha()
        super(Food, self).__init__(board, col)
        self.potency = nutrients
        
    def effect(self):
        #will apply the effect of the powerup on the game
        pass

if __name__ == "__main__":
    # Uncomment this line to call new_game when this file is run:
    new_game()
    pass
