import arcade

from player import Player
from constants import *


class MessageBox:
    def __init__(self, speaker, x, y, message):
        self.message = message
        self.width = 500
        self.height = 50
        self.x = x
        self.y = y
        self.speaker = speaker

    def on_draw(self):
        cx = self.x
        cy = self.y -200

        arcade.draw_rectangle_filled(cx,
                                     cy,
                                     self.width + MESSAGE_BOX_MARGIN * 2,
                                     self.height + MESSAGE_BOX_MARGIN * 2,
                                     arcade.color.LIGHT_GRAY)
        arcade.draw_rectangle_outline(cx,
                                      cy,
                                      self.width + MESSAGE_BOX_MARGIN * 2,
                                      self.height + MESSAGE_BOX_MARGIN * 2,
                                      self.speaker,
                                      4)

        arcade.draw_text(self.message,
                         cx,
                         cy,
                         arcade.color.BLACK,
                         MESSAGE_BOX_FONT_SIZE,
                         anchor_x="center", anchor_y="center", align="center",
                         width=500)

    # def on_key_press(self, _key, _modifiers):
    #     self.view.close_message_box()
    #     # self.message_box = None