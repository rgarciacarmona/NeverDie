import libtcodpy as libtcod

from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
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
    max_monsters_per_room = 3
    # Field of view parameters
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10
    # Colors for blocked and non-blocked tiles
    colors = {
        'dark_wall': libtcod.Color(0,0,100),
        'dark_ground': libtcod.Color(50,50,150),
        'light_wall': libtcod.Color(130,110,50),
        'light_ground': libtcod.Color(200,180,50)
    }

    # Player data, a white @ in the middle of the screen
    # Position needs to be forcefully cast to int
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@',
        libtcod.white, 'Player', blocks=True)
    # Entity array
    entities = [player]

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
                      map_width, map_height, player, entities,
                      max_monsters_per_room)

    # Variable to recompute FOV
    fov_recompute = True
    # Initialize field of view
    fov_map = initialize_fov(game_map)

    # Store keyboard and mouse input
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Initiatlize the game state
    game_state = GameStates.PLAYER_TURN

    # Main game loop
    while not libtcod.console_is_window_closed():

        # Captures keyboard and mouse input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # Recompute FOV if player has moved
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius,
                fov_light_walls, fov_algorithm)

        # Draws entities and map
        render_all(con, entities, game_map, fov_map, fov_recompute,
            screen_width, screen_height, colors)
        fov_recompute = False

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

        # If "move" and is the player's turn, moves the player
        if move and game_state == GameStates.PLAYER_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            # Check if the space is blocked by a wall before moving
            if not game_map.is_blocked(destination_x, destination_y):
                # And if it's blocked by an entity
                target = get_blocking_entities_at_location(entities,
                    destination_x, destination_y)
                if target:
                    print('You kick the ' + target.name + ' in the shins, ' +
                        'much to its annoyance!')
                else:
                    player.move(dx, dy)
                    # Recompute FOV after moving
                    fov_recompute = True
                # Change to enemy's turn
                game_state = GameStates.ENEMY_TURN

        # If it's the enemy's turn, move the enemies
        if game_state == GameStates.ENEMY_TURN:
            # Every monster does nothing
            for entity in entities:
                if entity != player:
                    print('The ' + entity.name + ' ponders the meaning of ' +
                        'its existence.')
            # Change to player's turn
            game_state = GameStates.PLAYER_TURN

        if exit:
            return True
        # If "fullscreen"", toggles fullscreen
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
