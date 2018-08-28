class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    Contains coordinates, the ASCII character, its color,
    its name and if it blocks passage or not.
    """
    def __init__(self, x, y, char, color, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

# Out of class functions
# Checks if any entity is blocking pass to a location
# It assumes there can only be one entity at any given location
def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    return None
