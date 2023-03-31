from __future__ import annotations
from layer_store import SetLayerStore, AdditiveLayerStore, SequenceLayerStore
from data_structures.referential_array import ArrayR
class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
        raise NotImplementedError()
        if draw_style not in self.DRAW_STYLE_OPTIONS:
            raise ValueError("Invalid draw style.")

        self.x = x
        self.y = y
        self.draw_style = draw_style
        self.brush_size = self.DEFAULT_BRUSH_SIZE
        self.grid = ArrayR(x)
        for i in range(x):
            self.grid[i] = ArrayR(y)
            for j in range(y):
                if self.draw_style == Grid.DRAW_STYLE_SET:
                    self.grid[i][j] = SetLayerStore()
                elif self.draw_style == Grid.DRAW_STYLE_ADD:
                    self.grid[i][j] = AdditiveLayerStore()
                elif self.draw_style == Grid.DRAW_STYLE_SEQUENCE:
                    self.grid[i][j] = SequenceLayerStore()
    def __getitem__(self, index):
        return self.grid[index]
    def __setitem__(self, index, value):
        self.grid[index] = value
    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        raise NotImplementedError()
        if self.brush_size == 5: 
            print('The max brush size is 5.')
        elif self.brush_size < 5: 
            self.brush_size += 1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        raise NotImplementedError()
        if self.brush_size == 0: 
            print('The min brush size is 0.')
        elif self.brush_size > 0: 
            self.brush_size -= 1

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        raise NotImplementedError()
        for i in range(self.x):
            for j in range(self.y):
                layer_store = self.grid[i][j]
                if isinstance(layer_store, SetLayerStore):
                    layer_store.special()
                elif isinstance(layer_store, AdditiveLayerStore):
                    layer_store.special()
                elif isinstance(layer_store, SequenceLayerStore):
                    layer_store.special()