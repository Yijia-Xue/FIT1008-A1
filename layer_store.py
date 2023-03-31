from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack 
from data_structures.array_sorted_list import ArraySortedList
from layers import rainbow, black, lighten, invert, red, green, blue, sparkle, darken

class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """
    def __init__(self): 
        super().__init__()
        self.current_layer = None
        self.color_inverted = False

    def add(self, layer:Layer): 
        self.current_layer = layer
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        bottom_color = start 
        if self.current_layer is not None:
            bottom_color = self.current_layer.apply(bottom_color, timestamp, x, y)
        if self.color_inverted:
            inverted_color = tuple(255 - c for c in bottom_color)
            return inverted_color
        return bottom_color

    def erase(self, layer: Layer) -> bool: 
        self.current_layer = None
        return True

    def special(self): 
        self.color_inverted = not self.color_inverted
        return True
    
class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
     """
    
    def __init__(self, max_capacity = 900):
        super().__init__()
        self.layers = CircularQueue(max_capacity)
        self.max_capacity = max_capacity

    def add(self, layer: Layer) -> bool:
        self.layers.append(layer)
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        bottom_color = start 
        layer_store = ArrayStack(max_capacity=900)
        if self.layers is not None:
            for _ in range(len(self.layers)): 
                item = self.layers.serve()
                if isinstance(item, Layer):
                    bottom_color = item.apply(bottom_color, timestamp, x, y)
                    self.layers.append(item)
        return bottom_color
    
    def erase(self, layer: Layer) -> bool:
        if len(self.layers) == 0: 
            return False
        else: 
            self.layers.serve()
            return True

    def special(self):
        reverse = ArrayStack(self.layers.__len__())
        for _ in range(len(self.layers)): 
            reverse.push(self.layers.serve())
        for _ in range(len(reverse)):
            self.layers.append(reverse.pop())
    

class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """
    def __init__(self):
        super().__init__()
        self.applied_layers = ArraySortedList(20)
        self.cur_layer_index = 0

    def add(self, layer: Layer) -> bool:
        self.applied_layers.__setitem__(self.cur_layer_index, layer)
        self.cur_layer_index += 1
        return True

    def erase(self, layer: Layer) -> None:
        if self.applied_layers is not None: 
            if self.applied_layers.__contains__(layer): 
                index = self.applied_layers.index(layer)
                self.applied_layers.delete_at_index(index)
                return True
        return False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        bottom_color = start 
        if self.applied_layers is not None:
            for i in range(0, self.applied_layers.__len__()): 
                item = self.applied_layers.__getitem__(i)
                if isinstance(item, Layer):
                    bottom_color = item.apply(bottom_color, timestamp, x, y)
        return bottom_color


    def special(self):
        if len(self.applied_layers) != 0:
            layer_store = ArrayStack(len(self.applied_layers))
            for i in range(len(self.applied_layers)): 
                layer = self.applied_layers.delete_at_index(0)
                if layer == black: 
                    layer.key = 0
                if layer == blue: 
                    layer.key = 1
                if layer == darken:
                    layer.key = 2
                if layer == green:
                    layer.key = 3
                if layer == invert:
                    layer.key = 4 
                if layer == lighten:
                    layer.key = 5 
                if layer == rainbow:
                    layer.key = 6
                if layer == red: 
                    layer.key = 7
                if layer == sparkle:
                    layer.key = 8
                layer_store.pop(layer)
            for i in range(len(layer_store)): 
                self.applied_layers.add(layer_store.pop())
            

            len_layer = self.applied_layers.__len__()

            median_index = len_layer // 2
            if median_index == 0: 
                self.applied_layers.delete_at_index(median_index)
            else:
                self.applied_layers.delete_at_index(median_index + 1)
