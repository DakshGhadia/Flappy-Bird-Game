# Name: Daksh Ghadia

# ID: mdd3wn@virginia.edu

#Instruction to play this game
'''
Press space to jump. Your goal is not let the bird touch the poles by going through the gap in between.
If your bird touches the poll, you health will be reduced by one heart. The game is over
when you no longer have any hearts in your health bar. While the game is on, there will be two
collectibles for you to collect: heart and clock. Heart adds a hear in your health bar and clock
reduces the speed at which the poles are coming at the bird so that the player has an easier time
going through the poles.
'''

# Description:
'''
My game will be like a flappy bird game where my character will be able to fly and
go between the poles where there is space in between. The poles will be coming at him and his job
will be to dodge those poles by going through the gap in the between via flying.
My game will end when my character hits exactly 3 poles that are coming at him. 
'''

# 3 basic features:
'''
The only user input will be from the pressing the space bar which will cause the bird to jump.

My game ends when the bird hits a pole.

I will use an image of flappy bird that will be the main character of the game which will be jumping
between the poles.
'''

# 4 additional features
'''
Restart from Game over: When the game is over, the screen will say "Press up arrow to restart"

Health Bar: At the beginning of the game, my health bar will have 3 bars. Each time the bird hits a pole,
health bar will lose one bar. When the bird hits 3 poles, there will no bars left and the game will end.

Timer: I will implement this a little bit differently. I will have 2 things: 1 being a regular timer, 2 
being best time. First time the user plays the game, both my timer and best timer will increment at the
same time going up by one point every second the game is not over. 
However, after the 1st game is over, my regular timer will reset to 0, and best time will stay
as it is. When the user goes above the best time when he plays next, best time will start incrementing again. 
It's like saving your personal best.


Collectibles: I will have 2 collectibles: 
- one to increase the health
- one to decrease the speed at which the poles are coming at the bird

I made some changes to what collectibles I'll have in my game since checkpoint 2
'''



import time
import random
import uvage

#initialize camera and the bird and its features
camera = uvage.Camera(800, 600)
bird = uvage.from_image(300, 100, 'flappybird Background Removed.png')
screen_height = 600
bird.scale_by(0.07)
gravity = 0.9

#intialize variables related to poles
poles = []
pole_speed = 5
pole_gap = 350
collided_poles = []

#initialize the borders on the screen
top_border = uvage.from_color(400, 0, "black", 800, 25)
bottom_border = uvage.from_color(400, 600, "black", 800, 25)

#initialize variables realted to poles
heart = uvage.from_image(0, 0, 'heart.png')
heart.scale_by(0.1)
health = 3
heart_speed = 5

#initialize variables realted to clock
clock = uvage.from_image(0,0, 'Clock_image.png')
clock.scale_by(0.1)
clock_speed = 5
clock_effect_duration = 8
clock_effect_end_time = 0

#initialize variables related to scores
time1 = time.time()
personal_best = 0
current_score = 0
increment_both_times = False

def initialize_clock(): #changed since Checkpoint 2
    global poles
    clock.x = random.randint(800, 4000)  # Set initial x position
    clock.y = random.randint(50, 550)  # Set initial y position

    # Check for collisions with poles
    while any(clock.touches(pole) for poles1 in poles for pole in poles1):
        #keep changing the clock's position until it is no longer colliding with the poles
        clock.x = random.randint(800, 4000)
        clock.y = random.randint(50, 550)

def draw_clock(): #changed since Checkpoint 2
    camera.draw(clock) #display the clock on the screen

def move_clock(): #changed since Checkpoint 2
    global clock_speed
    clock.x -= clock_speed #move the clock horizontally towards the bird

    if time.time() < clock_effect_end_time:
        #if the bird touched the clock collectibles, then slow down the clock's speed
        clock_speed = 3
    else:
        # if the clock effect has ended, go back to normal speed
        clock_speed = 5

    if clock.x < 0:
        # if the clock collectible is off the screen, then initialize it again
        initialize_clock()

def collect_clock(): #changed since Checkpoint 2
    global pole_speed, clock_effect_end_time, heart_speed, clock_speed
    if bird.touches(clock):
        #if the bird touched the clock collectible, then slow down the speed at which poles, hearts
        # and clocks are coming at it
        clock_effect_end_time = time.time() + clock_effect_duration
        pole_speed = 3
        heart_speed = 3
        clock_speed = 3
        initialize_clock()

def initialize_heart(): #changed since Checkpoint 2
    global poles

    heart.x = random.randint(800, 2000)  # Set initial x position
    heart.y = random.randint(50, 550)  # Set initial y position

    # Check for collisions with poles
    while any(heart.touches(pole) for poles1 in poles for pole in poles1):
        #keep changing the heart's position until it is no longer colliding with the poles
        heart.x = random.randint(800, 2000)
        heart.y = random.randint(50, 550)

def draw_heart(): #changed since Checkpoint 2
    camera.draw(heart) #display the heart on the screen

def move_heart(): #changed since Checkpoint 2
    global heart_speed
    heart.x -= heart_speed #move the heart horizontally towards the bird

    if time.time() < clock_effect_end_time:
        #if the bird touched the heart collectibles, then slow down the heart's speed
        heart_speed = 3
    else:
        # If the clock effect has ended, go back to normal speed
        heart_speed = 5

    if heart.x < 0:
        # if the heart collectible is off the screen, then initialize it again
        initialize_heart()

def collect_heart(): #changed since Checkpoint 2
    global health
    if bird.touches(heart):
        # if the bird touched the heart collectible, then add a heart to its health bar
        if health < 3:
            health += 1
        initialize_heart()
def generate_poles():
    gap_size = 110 #size of the gap from which the bird will pass through
    pole_height = screen_height - gap_size #sets the pole height
    pole1_y = random.randint(-pole_height, pole_height)/2 #sets the y position of the first pole
    pole2_y = pole1_y + pole_height + gap_size #sets the y position of the second pole
    return [uvage.from_color(start_lvl, pole1_y, "black", 30, pole_height),
            uvage.from_color(start_lvl, pole2_y, "black", 30, pole_height)]

def initialize_poles():
    global start_lvl
    start_lvl = 200 #distance between 2 poles
    for i in range(100):
        poles.append(generate_poles()) #adds 100 poles to the list
        start_lvl += pole_gap

def add_new_poles(): #changed since Checkpoint 2
    global start_lvl
    # Check if it's time to add new poles based on the distance between the last pole and the screen edge
    if poles[-1][0].x < 800:  # Checks if new poles are needed
        start_lvl = poles[-1][0].x + pole_gap  # Set the starting level based on the x-coordinate of the last pole
        poles.append(generate_poles())
        start_lvl += pole_gap
def draw_border():
    #displays the top and bottom border on the screen
    camera.draw(bottom_border)
    camera.draw(top_border)

def draw_poles():
    #draws the poles on the screen
    for poles1 in poles:
        for each_pole in poles1:
            camera.draw(each_pole)

    add_new_poles()  # call the add_new_poles function

def move_poles():
    global pole_speed,clock_effect_end_time

    if not game_over():
        # moves the poles towards the bird until the game is over
        for poles1 in poles:
            for each_pole in poles1:
                each_pole.x -= pole_speed

        # Check if the clock effect is still active
        if time.time() < clock_effect_end_time:
            pole_speed = 3
        else:
            # If the clock effect has ended, go back to normal speed
            pole_speed = 5



def move_bird():
    if not game_over():
        if uvage.is_pressing('space'):
            #the bird jumps if the player is playing pressing space bar
            bird.speedy = -10

        bird.speedy += gravity
        bird.move_speed()

        if bird.top_touches(top_border) or bird.bottom_touches(bottom_border):
            #prevents the bird from going off the screen from both the top and bottom
            if bird.bottom_touches(bottom_border):
                bird.move_to_stop_overlapping(bottom_border)
            else:
                bird.move_to_stop_overlapping(top_border)


def game_over(): #changed since Checkpoint 2
    global health, collided_poles
    #game is over if the runs of hearts in the health bar
    #a heart is removed from the health bar everytime the bird touches one of the poles
    for poles1 in poles:
        for each_pole in poles1:
            if bird.touches(each_pole) and each_pole not in collided_poles:
                collided_poles.append(each_pole)
                if health > 0:
                    health -= 1

    return health <= 0

def display_game_over():
    #display the game over text on the screen
    if game_over():
        camera.draw(uvage.from_text(400, 300, "GAME OVER :(", 80, "Red"))

def draw_health(): #changed since Checkpoint 2
    #draw 3 hearts for the health bar at the begining of the game. Decrement one everytime the bird touches the poles
    camera.draw(uvage.from_text(38, 25, "Health:", 30, "Red"))
    heart1 = uvage.from_image(10, 40, 'heart.png')
    heart1.scale_by(0.1)

    heart2 = uvage.from_image(30, 40, 'heart.png')
    heart2.scale_by(0.1)

    heart3 = uvage.from_image(50, 40, 'heart.png')
    heart3.scale_by(0.1)

    if health == 3:
        camera.draw(heart1)
        camera.draw(heart2)
        camera.draw(heart3)

    elif health == 2:
        camera.draw(heart1)
        camera.draw(heart2)

    elif health == 1:
        camera.draw(heart1)

def display_scores(): #changed since Checkpoint 2
    if not game_over():
        global current_score,personal_best, time2, time1, increment_both_times
        time2 = time.time()
        current_score = int(time2 - time1) #sets the current score
        if current_score>personal_best:
            # if the current score becomes larger than personal best, then increment personal best along with current score
            personal_best = current_score

    #Display both scores on the screen
    camera.draw(uvage.from_text(32, 70, "Score:", 30, "Green"))
    camera.draw(uvage.from_text(74, 70, str(current_score), 30, "Green"))
    camera.draw(uvage.from_text(52, 100, "Best Score:", 30, "Green"))
    camera.draw(uvage.from_text(120, 100, str(personal_best), 30, "Green"))

def restart_game(): #changed since Checkpoint 2
    if game_over() and uvage.is_pressing("up arrow"):
        global poles, pole_speed, time1, time2, collided_poles, health, clock_effect_end_time, current_score, increment_both_times
        poles = [] # empty the poles list
        pole_speed = 5 # set pole_speed to 5
        clock_effect_end_time=0 #eliminate the slowed time effect
        collided_poles = [] #empty the collide_poles list
        health = 3 #set health to 3
        current_score= 0 #set current score to 0
        time1 = time.time() #reset time
        #initialize poles, hearts, and clock
        initialize_poles()
        initialize_heart()
        initialize_clock()

def display_restart_prompt(): #changed since Checkpoint 2
    if game_over():
        #display the "Press Up Arrow to Restart" text
        camera.draw(uvage.from_text(400, 400, "Press Up Arrow to Restart", 80, "Red"))

# Initial floor generation, heart, and clock
initialize_poles()
initialize_heart()
initialize_clock()
def tick():
    camera.clear("White")
    camera.draw(bird)
    draw_poles()
    if not game_over():
        draw_heart()
        draw_clock()
    draw_health()
    move_poles()
    move_bird()
    if not game_over():
        move_heart()
        move_clock()
    collect_heart()
    collect_clock()
    draw_border()
    display_game_over()
    display_restart_prompt()
    restart_game()
    display_scores()
    camera.display()

uvage.timer_loop(30, tick)


