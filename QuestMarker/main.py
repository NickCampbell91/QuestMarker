import random
import arcade
import os
import math
import time

from player import Player
from constants import *
from message_box import MessageBox

class Marker(arcade.Sprite):
    
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

class Objective(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title, fullscreen=True)

        # Variables that will hold sprite lists
        self.player_list = None
        self.objective_list = None
        self.king_list = None
        self.marker_list = None

        # Set up the player info
        self.player_sprite = None
        self.objective_sprite = None

        # A camera to follow the player
        self.camera = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.questActive = False
        self.returning = False

        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)

        self.message_box = None

        self.endIsNear = False

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Setup the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.objective_list = arcade.SpriteList()
        self.king_list = arcade.SpriteList()
        self.marker_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player("images/player.png",
                                    SPRITE_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player_sprite)

        # Create king
        king = arcade.Sprite("images/king.png", SPRITE_SCALING)

        # King position
        king.center_x = 200
        king.center_y = 210

        # Add king to list
        self.king_list.append(king)
        
        # Create marker
        self.marker = Marker("images/marker2.png", SPRITE_SCALING)

        # Marker position
        self.marker.center_x = 400
        self.marker.center_y = 550

        # Add marker to list
        self.marker_list.append(self.marker)

        for i in range(len(QUEST_DIALOGUE)):
            # Create ojective 
            self.objective_sprite = Objective("images/objective.png", SPRITE_SCALING)

            # Objective position
            self.objective_sprite.center_x = random.randrange(-SCREEN_WIDTH, SCREEN_WIDTH * 2)
            self.objective_sprite.center_y = random.randrange(-SCREEN_HEIGHT, SCREEN_HEIGHT * 2)

            # Add objective to list
            self.objective_list.append(self.objective_sprite)

        self.audio_name = arcade.sound.load_sound("music/2019-12-09_-_Retro_Forest_-_David_Fesliyan.mp3")
        arcade.sound.play_sound(self.audio_name)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Activate our Camera
        self.camera.use()

        # Draw all the sprites.
        self.player_list.draw()
        self.objective_list.draw()
        self.king_list.draw()
        self.marker_list.draw()

        # Draw any message boxes
        if self.message_box:
            self.message_box.on_draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        # Position the camera
        self.center_camera_to_player()

        # Call update to move the sprite
        # If using a physics engine, call update player to rely on physics engine
        # for movement, and call physics engine here.
        self.player_list.update()

        # Check for king collision
        king_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.king_list)

        # Handle King collision
        for king in king_hit_list:
            if not QUEST_DIALOGUE and self.returning == True:
                self.message_box = MessageBox(arcade.color.INDIGO, self.player_sprite.center_x, self.player_sprite.center_y, "You're still here? You've found everything my kingdom has to offer. Kinda ruined things for future generations if I'm being honest. For your crimes against posterity, you're being removed from this world.")
                self.endIsNear = True
            elif (self.questActive == True and self.message_box == None and self.returning == True):
                self.message_box = MessageBox(arcade.color.INDIGO, self.player_sprite.center_x, self.player_sprite.center_y, "Took you long enough! Gimme! Gimme! Gimme!")
                self.questActive = False
                self.returning = False
                if (self.objective_list[0] == None):
                    self.objective_list.pop(0)
            elif (self.questActive == False and self.message_box == None): #and self.returning == True):
                self.message_box = MessageBox(arcade.color.INDIGO, self.player_sprite.center_x, self.player_sprite.center_y, QUEST_DIALOGUE.pop(random.randint(0, len(QUEST_DIALOGUE) - 1)))
                self.questActive = True
                self.returning = False
            
        # To be honest, I don't think this does anything.
        self.objective_list.update()

        # Check for objective collision
        objective_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.objective_list)

        # Loop through each colliding sprite, remove it.
        # Put this in a loop in case I add multiple objective sprites later.
        for objective in objective_hit_list:
            if (self.questActive == False or objective != self.objective_list[0]):
                self.message_box = MessageBox(arcade.color.BLACK, self.player_sprite.center_x, self.player_sprite.center_y, '"That looks pretty!"')
                
            else: 
                self.message_box = MessageBox(arcade.color.BLACK, self.player_sprite.center_x, self.player_sprite.center_y, '"Finally found it! Better return this to the King."')
                objective.kill()
                self.questActive = False
                self.returning = True

        if (self.questActive):
            # Find the direction to the objective
            myradian = math.atan2(self.player_sprite.center_y - self.objective_list[0].center_y, self.player_sprite.center_x - self.objective_list[0].center_x)
        else:
            # Find the direction to the king
            myradian = math.atan2(self.player_sprite.center_y - self.king_list[0].center_y, self.player_sprite.center_x - self.king_list[0].center_x)

        mydegree = math.degrees(myradian)
        #print(mydegree)

        # Rotate marker
        self.marker.angle = mydegree + 90

        # Move marker
        self.marker.center_x = self.player_sprite.center_x - (math.cos(myradian) * 90)
        self.marker.center_y = self.player_sprite.center_y - (math.sin(myradian) * 90)       

        if (self.endIsNear and self.message_box == None):
            quit()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if self.message_box:
            self.message_box = None
            #return

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)   

def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()