from random import randint
from map_objects.tile import Tile
from map_objects.rectangle import Rect

class GameMap:
    """
    Contains a 2d array of tiles and methods for
    setup and interactions.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        # Tiles are blocked by default
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size,
                 map_width, map_height, player):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # Random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_min_size)
            # Random position withouth going out of bounds
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)
            # Create the room
            new_room = Rect(x, y, w, h)
            # Discard the room if intersects with other rooms
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            # for-else, if the loop didn't break, create the room
            else:
                self.create_room(new_room)
                (center_x, center_y) = new_room.center()
                # If it's the first room, put the player inside it
                if num_rooms == 0:
                    player.x = center_x
                    player.y = center_y
                # If it's not the first room, connect it with the previous one
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    # Coin flip
                    if randint(0,1) == 1:
                        # First horizontal tunnel, then vertical
                        self.create_h_tunnel(prev_x, center_x, prev_y)
                        self.create_v_tunnel(prev_y, center_y, center_x)
                    else:
                        # First vertical tunnel, then horizontal
                        self.create_v_tunnel(prev_y, center_y, prev_x)
                        self.create_h_tunnel(prev_x, center_x, center_y)
                # Add the room to the list
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, rect):
        # Make all tiles inside a rectangle (but not the borders) not-blocked
        for x in range(rect.x1 + 1, rect.x2):
            for y in range(rect.y1 + 1, rect.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False
