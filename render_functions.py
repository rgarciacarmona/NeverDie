import libtcodpy as libtcod
"""
Contains the functions for drawing and clearing from the screen
"""

# Draw all entities and the map
def render_all(con, entities, game_map, screen_width, screen_height, colors):
    # Draw all the tiles in the game map
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight
            if wall:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)
    # Draw the entities
    for entity in entities:
        draw_entity(con, entity)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

# Clear all entities from the screen
# Call after every movement to erase old positions
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

# Draw an entity
def draw_entity(con, entity):
    libtcod.console_set_default_foreground(con, entity.color)
    # Draws the entity without background in console
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

# Clear an entity
def clear_entity(con, entity):
    # Erase the character that represents this entity
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
