import libtcodpy as libtcod

from entity import Entity
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all

def main():
    # Screen size
    screen_width = 80
    screen_height = 50
    # Map parameters
    map_width = 80
    map_height = 45
    max_rooms = 30
    room_min_size = 6
    room_max_size = 10
    # Colors for blocked and non-blocked tiles outside field of view
    colors = {
        'dark_wall': libtcod.Color(0,0,100),
        'dark_ground': libtcod.Color(50,50,150)
    }

    # Player data, a white @ in the middle of the screen
    # Position needs to be forcefully cast to int
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    # Other entities
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)
    # Entity array
    entities = [npc, player]

    # Loads greyscale TCOD-mapping Arial 10x10 font
    libtcod.console_set_custom_font('arial10x10.png',
        libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # Creates the screen. Boolean indicates full screen
    libtcod.console_init_root(screen_width, screen_height, 'NeverDie', False)
    # Creates a new console
    con = libtcod.console_new(screen_width, screen_height)
    # Initialize the map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size,
                      map_width, map_height, player)

    # Store keyboard and mouse input
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Main game loop
    while not libtcod.console_is_window_closed():

        # Captures keyboard and mouse input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # Draws entities and map
        render_all(con, entities, game_map, screen_width, screen_height, colors)

        # Redraws the screen
        libtcod.console_flush()

        # Erases old positions of entities
        clear_all(con, entities)

        # Leaves a red dot to be drawn next time the @ moves
        libtcod.console_set_default_foreground(con, libtcod.red)
        libtcod.console_put_char(con, player.x, player.y, '.', libtcod.BKGND_NONE)

        # Handles key presses
        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        # If "move", moves the player
        if move:
            dx, dy = move
            # Check if the space is blocked before moving
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)
        if exit:
            return True
        # If "fullscreen"", toggles fullscreen
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
