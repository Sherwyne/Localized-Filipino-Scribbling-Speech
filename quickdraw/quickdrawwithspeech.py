# Python
from __future__ import division
import io
import os
import re
import time
import sys

# QuickDraw
from quickdraw import QuickDrawDataGroup, QuickDrawing

# Google Cloud
from google.cloud import language, speech
from google.cloud.speech import enums
from google.cloud.speech import types

# 3rd party
import pyaudio
import tkinter
import random



# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# setup canvas
WIDTH=800
HEIGHT=800
window = tkinter.Tk()
canvas = tkinter.Canvas(window, width=WIDTH, height=HEIGHT)
canvas.pack()

# drawings
all_drawings = []

# offset addition
X_OFFSET_ADD = 250
wordDB = ['house','above','airplane','ambulance','flower']


class draw_thing():
    '''
    draws and animates objects
    also stores the canvas objects to be deleted later
    '''

    def __init__(self, drawings, name, padding_x=0, padding_y=0):
        self.drawings = drawings
        self.padding_x = padding_x
        self.padding_y = padding_y

        noun_keyword_offset = {
          'fish': 200,
          'flower':200,
          'bird': -200,
        }

        # some objects are sky or below sky
        if name in noun_keyword_offset:
            self.padding_y = self.padding_y + noun_keyword_offset[name]

        self.name = name
        self.lines = []


    def animate(self):
        window.update()

        # draw them
        for i in range(0, self.drawings.drawing_count):
            time.sleep(0.05)
            self.draw(drawing=self.drawings.get_drawing(index=i))
            if i < (self.drawings.drawing_count - 1):
                self.erase()


    def draw(self, drawing=0):
        self.lines = []
        for stroke in drawing.strokes:
            x_last = 0
            y_last = 0
            index = 0
            for x, y in stroke:
                x = x + self.padding_x
                y = y + self.padding_y
                if index > 0:
                    self.lines.append(canvas.create_line(x_last,
                                                         y_last,
                                                         x,
                                                         y,
                                                         width=5,
                                                         cap=tkinter.ROUND,
                                                         join=tkinter.ROUND))
                x_last = x
                y_last = y
                index = index + 1
                window.update()


    def erase(self):
        for line_id in self.lines:
            canvas.after(50, canvas.delete, line_id)
            window.update()

def word_entities(word):
    # word = translate_text(word)
    # document = language.types.Document(content=word,
    #                                    type=language.enums.Document.Type.PLAIN_TEXT,)
    # client = language.LanguageServiceClient()
    # response = client.analyze_entities(document=document,encoding_type='UTF32',)
    # get all drawings

    response = word
    global all_drawings

    # erase old scene if exists
    last_x_offset = 50
    for drawing_object in all_drawings:
        drawing_object.erase()

    y_offset = (HEIGHT / 2) - 100

    # loop through words and draw
    for entity in response:
        # print(entity.name)
        # print(entity.type)

        # special keywords can change y offset
        y_offset_keywords = {
          'above': -200,
          'top': -200,
          'below': 200,
          'bottom': 200
        }

        # check if this is something to draw or a keyword to influence drawing
        if entity in y_offset_keywords:
            y_offset = y_offset + y_offset_keywords[entity]
        else:
            # lowercase all entities, uppercase will find drawings
            name = entity.lower()
            print(name)
            # print("NAME:",  name)

            # Replacing common nouns with similar look (face = person)
            # replace_noun = {
            #     "someone" : "face",
            #     "dead" : "skull",
            # }
            # for key,value in replace_noun.items():
            #     if name == key:
            #         name = value
            
            # print("REPLACED NAME:",  name)
            try:
                # get 10 drawings if they exist
                drawings = QuickDrawDataGroup(name, max_drawings=10)

                # confirm there is someting to draw
                if drawings:
                    # change padding offsets to keep drawings separate
                    padding_x = last_x_offset
                    padding_y = (HEIGHT / 2) - 100
                    drawing = draw_thing(drawings,
                                         name,
                                         padding_x=padding_x,
                                         padding_y=padding_y)
                    drawing.animate()
                    all_drawings.append(drawing)
                    last_x_offset = last_x_offset + X_OFFSET_ADD
            except ValueError:
                print("No drawings found in dataset".format(entity))

def main():
    # Show canvas
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#ffffff")

    horizon = HEIGHT / 2 + 100
    canvas.create_line(0,
                       horizon,
                       WIDTH,
                       horizon,
                       width=2,
                       dash=(4, 4),
                       fill="#d3d3d3",
                       cap=tkinter.ROUND,
                       join=tkinter.ROUND)
    window.update()
    word_entities(wordDB)


if __name__ == '__main__':
    main()