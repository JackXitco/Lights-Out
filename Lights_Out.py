import turtle
import math
import random
import time

#Side length of each square in the grid
side = 50
#Angle used by turtle to draw each square of the grid
angle = 90
#Count is used by draw_square() as its poisiton in the board list when it calls is_on()
#This number increments up from 0 to 24 as the grid is draw, and then is reset to 0 at the end of draw_grid()
count = 0
#Keeps track of the number of moves the user has made, displayed by draw_grid()
moves = 0
#List of the state of each square on the grid, -1 = "off", 1 = "on"
board = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
#The board starts off as initially solved, and then becomes "unsolved" when randomize_board() is called in main
#This was done to prevent creating boards that are unsolvable
blockcolors = ["grey64", "blue", "yellow", "green", "goldenrod2", "magenta", "teal"]
bgcolors = ["LightSlateBlue", "LightCoral", "white", "LightSeaGreen", "honeydew", "alice blue", "lavender", "navajo white", "light cyan"]

def choose_color(colors):
    '''
    Sig: list(str) ---> str
    Randomly chooses a color from a list of colors, removes it from the list, and returns it
    '''
    x = random.randint(0, len(colors) - 1)
    color = colors[x]
    colors.remove(color)#Chosen color is removed from the list to avoid having "on_color" and "off_color" assigned to the same color
    return color

#Assigning the on and off colors for the board from the blockcolors list
on_color = choose_color(blockcolors)
off_color = choose_color(blockcolors)
#Assigning the background color from the bgcolor list
bk_color = choose_color(bgcolors)
turtle.bgcolor(bk_color)

def randomize_board():
    '''
    Sig: NoneType ---> list(int)
    Assigns random positions in the list "board" to be turned on at the start of the game
    '''
    global board
    number_of_initial_random_clicks = random.randint(3,20)#Creates a number of initial moves to make on the initially solved board
    for i in range(number_of_initial_random_clicks):
        position_to_turn_on = random.randint(0, 24)#Chooses a position in the board to simulate a click on
        switch_pressed(position_to_turn_on)
    return board#Returns the randomized, solvable board that the user sees at the beginning of the game

def flick(position):
    '''
    Sig: int ---> NoneType
    Checks to see if a given position is valid, then inverts its value in the board list
    '''
    global board
    if position >= 0 and position <= 24:#Handles the possibilty that flick is called for an index that is out of range of the board, such as on the corners
        board[position] *= (-1)
    
def switch_pressed(position):
    '''
    Sig: int ---> NoneType
    Performs the light switching action of the game at a position on the board by calling the
    flick function
    '''
    if position % 5 == 0:#Handles positions on the left edge of the board
        flick(position - 5)
        flick(position)
        flick(position + 1)
        flick(position + 5)
    elif position % 5 == 4:#Handles positions on the right edge of the board
        flick(position - 5)
        flick(position)
        flick(position - 1)
        flick(position + 5)
    else:#Handles all middle columns of the board
        flick(position - 5)
        flick(position - 1)
        flick(position)
        flick(position + 1)
        flick(position + 5)
             
def is_on(board, n):
    '''
    Sig: list(int), int ---> bool
    Checks to see if a given position "n" in the list "board" is currently on or off
    '''
    if board[n] == (-1):
        return True
    else:
        return False

def move_to(x, y):
    '''
    Sig: int, int ---> NoneType
    Moves turtle to a location without drawing a line from its previous location
    This function mostly serves to make code in draw_grid(), draw_key(), clickhandler() and title_screen() more concise
    '''
    turtle.up()
    turtle.goto(x,y)
    turtle.down()
    
def draw_square(x, y):
    '''
    Sig: int, int ---> NoneType
    Draws an individual square of the board and checks if the position of that
    square in "board" is on or off using the is_on function. If the position is
    turned on, the function draws a colored square
    '''
    global count
    turtle.color("Black")#Sets the border of each box in the grid to be black
    move_to(x,y)
    if (is_on(board, count)):#Checks to see if the position being drawn is an "on" or "off" square
        turtle.fillcolor(off_color)#If the position is "off", the square is colored the randomly selected "off" color
        turtle.begin_fill()
        for i in range(4):
            turtle.forward(side)
            turtle.right(angle)
        turtle.end_fill()
        count += 1#Position counter is incremented
    else:
        turtle.fillcolor(on_color)#If the position is "off", the square is colored the randomly selected "off" color
        turtle.begin_fill()
        for i in range(4):
            turtle.forward(side)
            turtle.right(angle)
        turtle.end_fill()
        count += 1#Position counter is incremented
        
def draw_row(x,y):
    '''
    Sig: int, int ---> NoneType
    Calls the draw_square function 5 times to draw a single row of the board
    '''
    for i in range(5):
        draw_square(x,y)
        x += 50
        
def draw_key():
    '''
    Sig: NoneType ---> NoneType
    Draws a sample key of the randomized on and off squres for the user in the top left corner of the screen
    '''
    move_to(-350, 300)
    turtle.write("On Lights =", font = ("Arial", 20, "normal"))
    move_to(-235, 325)
    turtle.fillcolor(on_color)#Drawing the "on" light sample box
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(side - 25)
        turtle.right(angle)
    turtle.end_fill()
    move_to(-350, 250)
    turtle.write("Off Lights =", font = ("Arial", 20, "normal"))
    move_to(-235, 275)
    turtle.fillcolor(off_color)#Drawing the "off" light sample box
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(side - 25)
        turtle.right(angle)
    turtle.end_fill()
    
def draw_grid():
    '''
    Sig: NoneType ---> NoneType
    Calls the draw_row function 5 times to draw the whole board
    '''
    global count
    global moves
    turtle.clear()#Clears the board to display the most current state after a move is made by the user
    draw_key()#Draws the key in the top left corner for the user
    x = -125
    y = 125
    for i in range(5):
        draw_row(x, y)
        y -= 50
     #The grid is drawn after each move, and turtle updates the number of moves made by the user in the top right of the screen
    move_to(150, 300)
    turtle.write("Moves Made: " + str(moves), font = ("Arial", 25, "normal"))
    if moves < 999:#Realistically the user should never make this many moves, but this is done to prevent the text from being cut off the edge of the screen
        moves += 1#Number of moves is incremented by 1 so the counter in top right updates after every user click
    turtle.update()
    count = 0#Resets the global position counter called by draw_square() to avoid an index out of range error, since by this point counter's value is 24

def clickhandler(x, y):
    '''
    Sig: int, int ---> NoneType
    Takes coordinates from the User's mouse click in onscreenclick() and calls usermove()
    at those coordinates, then calls for the board to be updated accordingly
    '''
    global board
    if usermove((x, y)):#Calls user move to find the switch pressed based on where the user clicked
        draw_grid()#Clears and then redraws the newly updated grid
        if check_gameover(board):#If the game is won, the user is notified
            move_to(-50, -175)
            turtle.write("Winner!", font = ("Arial", 30, "normal"))
            move_to(-75, -215)
            turtle.write("Click to exit", font = ("Arial", 30, "normal"))
            turtle.exitonclick()#Terminates the program when the user clicks in the window
    
def usermove(coordinates):
    '''
    Sig: tuple(int, int) ---> Bool
    Takes in coordinates from clickhandler() and translates them into the position on the board
    that was clicked, and then returns True or False depending on if the move was valid
    '''
    right_bound = -75
    bottom_bound = 75
    clickx = coordinates[0]#The coordinates being called by the clickhandler
    clicky = coordinates[1]
    position = 0
    while not clickx <= right_bound:
        right_bound += 50#Iterates along the top row of boxes until it finds the correct column
        position += 1
    while not clicky >= bottom_bound:
        bottom_bound -= 50#Iterates downwards through rows until it find correct row
        position += 5
    if clickx >= -125 and clickx <= 125 and clicky >= -125 and clicky <= 125:#Checks to make sure click was within the grid area
        switch_pressed(position)
        return True
    else:#Cancels the move from being made and instead notifies the user to give correct input
        turtle.goto(-215, 150)
        turtle.write("Please Click Inside the Area of the Board", font = ("Arial", 25, "normal"))
        return False
    
def check_gameover(board):
    '''
    Sig: List(int) ---> Bool
    Checks to see if the game has been won by the user
    '''
    status = True
    for n in board:
        if n == 1:
            #If any value in the board list is "on", status is set to False
            status = False
    return status

def title_screen():
    '''
    Sig: NoneType() ---> NoneType()
    Displays the title screen for the Lights Out game for 3 seconds before clearing so board is revealed to the user
    '''
    move_to(-200, 25)
    turtle.speed(10)
    turtle.write("Welcome to Lights Out", font = ("Arial", 40, "normal"))
    move_to(-150, -25)
    turtle.write("Created by Jack Xitco", font = ("Arial", 30, "normal"))
    time.sleep(3)
    turtle.clear()#Clears Title screen so board can be shown in main()
    
def main():
    '''
    Sig: NoneType ---> NoneType
    Runs the Lights Out game
    '''
    turtle.ht()
    #Title screen is displayed to the user
    title_screen()
    #Sets up turtle for initial drawing of the grid
    turtle.tracer(0,0)
    turtle.width(5)
    #The initial state of the board is randomized and displayed to the user
    randomize_board()
    turtle.onscreenclick(clickhandler)
    draw_grid()
    turtle.mainloop()
        
main()

