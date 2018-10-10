"""
A simple SET card game implemented in Python
Using tkinter for visualization
"""
import base64
import math
import time
import tkinter as tk
from tkinter import messagebox

from set_logic import *

__author__ = "Frederik Leira"
__version__ = "0.1"

CARD_HEIGHT = 300
CARD_WIDTH = 225
CARD_SPACE = 10

CARD_BACK_BACKGROUND = "white"
CARD_BACK_FOREGROUND = "red"
CARD_BACK_TEXT_COLOUR = "blue"
CARD_BACK_TEXT = "SET"

def timer_to_string(timer):
    timer = int(timer)
    time_string = "Time: "
    time_string += str(math.floor(timer/60))+':'+str(timer%60).zfill(2)
    return time_string

def PointsInCircum(x, y, r,n=30):
    return [(x+math.cos(2*math.pi/n*i)*r,y+math.sin(2*math.pi/n*i)*r) for i in range(0,n+1)]

def _create_square(self, x, y, r, **kwargs):
    return self.create_rectangle(x-r, y-r, x+r, y+r, **kwargs)

def _create_circle(self, x, y, r, **kwargs):
    points = PointsInCircum(x,y,r)
    return self.create_polygon(points, **kwargs)
#return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

def _create_triangle(self, x, y, r, **kwargs):
    points = [x-r,y+r,x,y-r,x+r,y+r]
    return self.create_polygon(points, **kwargs)

tk.Canvas.create_circle = _create_circle
tk.Canvas.create_square = _create_square
tk.Canvas.create_triangle = _create_triangle

class CardView:
    """
    A class to manage the drawing of a SET card on a canvas.
    """

    def __init__(self, canvas, card, left_side, top_side,
                 background_colour=CARD_BACK_BACKGROUND,
                 foreground_colour=CARD_BACK_FOREGROUND,
                 text_colour=CARD_BACK_TEXT_COLOUR, text=CARD_BACK_TEXT):
        """
        Construct a new card to be drawn on the given canvas at the left_position.

        Parameters:
            canvas (tk.Canvas): The canvas to draw the card onto.
            left_side (int): The amount of pixels in the canvas to draw the card.
            background_colour (tk.Color): Backface card background colour.
            foreground_colour (tk.Color): Backface card foreground colour.
            text_colour (tk.Color): Backface card text colour.
            text (str): Backface card text to display.
        """
        self._canvas = canvas
        self.card = card
        self.left_side = left_side
        self.right_side = left_side + CARD_WIDTH
        self.top_side = top_side
        self.bottom_side = top_side + CARD_HEIGHT

        self._background = background_colour
        self._foreground = foreground_colour
        self._text_colour = text_colour
        self._text = text
        self._image = None

        self.draw()

    def getShapeView(self):
        shape = str(self.card.getShape().name)
        if shape == "circle":
            return self._canvas.create_circle
        elif shape == "square":
            return self._canvas.create_square
        elif shape == "triangle":
            return self._canvas.create_triangle

    def draw(self):
        """Draw the backface of the card to the canvas."""
        self._back = self.draw_back(self._background)
        color = str(self.card.getColor().name)
        fill = str(self.card.getFill().name)
        fill_color = color
        stipple = ''

        shapenumber = int(self.card.getNumber().value)
        shape = str(self.card.getShape().name)

        if fill == 'half':
            stipple = 'gray25'
        elif fill == 'none':
            fill_color = ''
        drawShape = self.getShapeView()
        for i in range(0,shapenumber):
            drawShape(self.left_side+(CARD_WIDTH // 2), self.top_side+(CARD_HEIGHT // (shapenumber+1))*(i+1), 30, \
                    outline=color, fill=fill_color, stipple=stipple, width=2)
        return 1

    def draw_back(self, colour):
        """Draw the back of the canvas (the background not the backface).

        Parameters:
            colour (tk.Color): The colour of the background.
        """
        return self._canvas.create_rectangle(self.left_side, self.top_side,
                                             self.right_side, self.bottom_side,
                                             fill=colour)

    def draw_text(self, text, colour):
        """Draw text in the middle of the card.

        Parameters:
            text (str): The text to display on the card.
            colour (tk.Color): The colour of the text to display.
        """
        return self._canvas.create_text(self.left_side + (CARD_WIDTH // 2),
                                        CARD_HEIGHT // 2, text=text, fill=colour,
                                        font=('Times', '16', 'bold italic'))

class TableView(tk.Canvas):
    """
    A Canvas that displays a table of set cards on a board.
    """

    def __init__(self, master, table, pick_card=None, border_color="#6D4C41",
                 active_border="red", offset_x=CARD_WIDTH, offset_y=CARD_HEIGHT, *args, **kwargs):
        """
        Construct a table view.

        Parameters:
            master (tk.Tk|tk.Frame): The parent of this canvas.
            pick_card (callable): The callback when card in this deck is clicked.
                                  Takes an int representing the cards index.
            border_colour (tk.Color): The colour of the table border.
            offset (int): The offset between cards on the deck.
        """
        super().__init__(master, *args, **kwargs, bg=border_color,
                         highlightthickness=5, highlightbackground=border_color)

        self.pick_card = pick_card
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.cards = {}
        self.num_of_cols = int(len(table.getCards())/3)

        self._border_color = border_color
        self._active_border = active_border

        self.bind("<Button-1>", self._handle_click)


    def _handle_click(self, event):
        """Handles when the player clicks the deck."""
        # the index of the card in the deck
        slot_x = event.x // CARD_WIDTH
        slot_y = event.y // CARD_HEIGHT
        self.pick_card(int(slot_y*self.num_of_cols+slot_x))
        
    def draw_card(self, card, slot):
        """
        Draw a card in the given slot on the table.

        Parameters:
            card (Card): The card to draw to the table.
            slot (int): The position on the table to draw the card.

        Returns:
            (CardView): The card view drawn at the slot for a given card.
        """
        left_side = (slot%self.num_of_cols) * self.offset_x
        top_side = math.floor(slot/self.num_of_cols) * self.offset_y

        self.cards[slot] = CardView(self, card, left_side, top_side)

        return self.cards[slot]

    def draw(self, table, show=True):
        """
        Draw the cards based of the data in a given table instance.

        Parameter:
            table (Table): The current table to draw.
            show (bool): Whether the cards should be displayed or not.
        """
        # resize the canvas to fit all the cards in the deck
        self.resize(len(table.getCards()))#deck.get_amount())

        for i, card in enumerate(table.getCards()):
            self.draw_card(card, i)
            #view.redraw(card if show else None)

    def resize(self, size):
        """
        Calculate the dimensions required to fit 'size' cards in this canvas
        and update the canvas size.

        Parameters:
            size (int): The amount of cards that should be displayed on this table.
        """
        self.num_of_cols = size/3
        width = min(size, self.num_of_cols)*CARD_WIDTH
        height = math.floor(size/self.num_of_cols)*CARD_HEIGHT

        # resize canvas, adjust for border
        self.config(width=width - 10, height=height - 10)


class SetApp:
    """A graphical SET application"""

    def __init__(self, master, game, board_color="#F9B05A"):
        """Create a new SET application based on a given SetGame.

        Parameters:
            master (tk.Tk): The root window for the SET application.
            game (SEtGame): The game to display in this application.
            board_colour (tk.Color): The background colour of the board.
        """
        self._master = master
        self.game = game
        self.card_picks = []
        self.board_color = board_color
        self.start = time.time()
        self.timer = 0
        self.status = ""
        # define all the class variables
        self._board = self.deck = self.table = None

        self.render_board()
        self.add_menu()

    def render_board(self):
        # remove old frame, if it exists
        if self._board is not None:
            self._board.pack_forget()

        # create a board frame
        self._board = board = tk.Frame(self._master, width=5*CARD_WIDTH, height=4*CARD_HEIGHT, padx=20, pady=20,
                                       bg=self.board_color,
                                       borderwidth=2, relief="groove")
        board.pack(expand=True, fill=tk.BOTH)    

        # draw the table with cards
        self.table = self.draw_board()

        # draw the status bar
        self.timer_label, self.status_label, self.cards_left_label = self.draw_status()

        # start updating the status bar
        self.onUpdate()

    def new_game(self):
        """Start a new game"""
        deck = Deck()
        deck.shuffle()

        self.game = SetGame(deck)
        self.start = time.time()
        self.timer = 0
        self.status_label.config(text="")
        self.render_board()

    def add_menu(self):
        """Create a menu for the application"""
        menu = tk.Menu(self._master)

        # file menu with new game and exit
        file = tk.Menu(menu)
        file.add_command(label="New Game", command=self.new_game)
        file.add_command(label="Exit", command=self._master.destroy)

        # add file menu to menu
        menu.add_cascade(label="File", menu=file)
        self._master.config(menu=menu)

    def pick_card(self, slot):
        """Called when a given playable player selects a slot.

        Parameters:
            slot (int): The card index they selected.
        """
        card_view = self.table.cards[slot]
        if slot in self.card_picks:
            self.card_picks.remove(slot)
            card_view._canvas.itemconfig(card_view._back, fill='white')#str(card.getColor().name))
            return
        else:
            self.card_picks.append(slot)
            card_view._canvas.itemconfig(card_view._back, fill='gray')#str(card.getColor().name))

        if len(self.card_picks) == 3:
            cards = self.game.getTable().getCards()
            s = Set(cards[self.card_picks[0]], cards[self.card_picks[1]], cards[self.card_picks[2]])
            if s.isSetValid():
                #append to found_sets
                self.game.getTable().removeCards(self.card_picks)
                self.game.getTable().fillTable(self.game.getDeck())

            self.card_picks = []
            self.table.draw(self.game.getTable())
            self.cards_left_label.config(text="Cards Left: "+str(len(self.game.getDeck().getCards())))

    def draw_board(self):
        """Draw the board (table with cards).

        Returns:
            TableView: the active TableView for this SetGame
        """
        board = tk.Frame(self._board, width=4*CARD_WIDTH, height=3*CARD_HEIGHT, bg="#6D4C41")
        board.pack(side=tk.TOP, pady=20, fill=tk.BOTH, expand=True)

        # left pickup card pile view
        table = TableView(board, self.game.getTable(), pick_card=lambda card: self.pick_card(card))
        table.pack(side=tk.TOP)
        table.draw(self.game.getTable(), show=True)

        return table

    def draw_status(self):
        """Draw a status bar below the tableview."""

        timer_label = tk.Label(self._board, text=timer_to_string(self.timer),
                         font=('Times', '24', 'bold italic'),
                         bg=self.board_color)
        timer_label.pack(side=tk.LEFT, expand=True, fill=tk.X)

        status_label = tk.Label(self._board, text="",
                         font=('Times', '24', 'bold italic'),
                         bg=self.board_color)
        status_label.pack(side=tk.LEFT, expand=True, fill=tk.X)

        cards_left_label = tk.Label(self._board, text="Cards Left: "+str(len(self.game.getDeck().getCards())), \
            font=('Times', '24', 'bold italic'),
            bg=self.board_color)
        cards_left_label.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        return timer_label, status_label, cards_left_label

    def onUpdate(self):
        # update displayed time
        if self.game.isActive(): self.timer = time.time()-self.start
        else: self.status_label.config(text="You Win")
        self.timer_label.config(text=timer_to_string(self.timer))
        # schedule timer to call myself after 1 second
        self._board.after(1000, self.onUpdate)

def main():
    # create window for uno
    root = tk.Tk()
    root.title("SET Card Game")

    # build a pickup pile
    deck = Deck(number_of_attributes=4)
    deck.shuffle()

    # create and play the game
    game = SetGame(deck)
    app = SetApp(root, game)

    # update window dimensions
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()


if __name__ == "__main__":
    main()
