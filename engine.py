import libtcodpy as libtcod

from input_handlers import handle_keys

def main():
    # Screen size
    screen_width = 80
    screen_height = 50

    # Player position
    # Need to be forcefully cast to int
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    # Loads greyscale TCOD-mapping Arial 10x10 font
    libtcod.console_set_custom_font('arial10x10.png',
        libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # Creates the screen. Boolean indicates full screen
    libtcod.console_init_root(screen_width, screen_height, 'NeverDie', False)
    # Creates a new console
    con = libtcod.console_new(screen_width, screen_height)


    # Store keyboard and mouse input
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Main game loop
    while not libtcod.console_is_window_closed():

        # Captures keyboard and mouse input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # Draws characters in console in white
        libtcod.console_set_default_foreground(con, libtcod.white)
        # Draws an @ at (x,y) without background in console
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        # Draws the console on top of console 0
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        # Redraws the screen
        libtcod.console_flush()

        # Leaves a red dot to be drawn next time the @ moves
        libtcod.console_set_default_foreground(con, libtcod.red)
        libtcod.console_put_char(con, player_x, player_y, '.', libtcod.BKGND_NONE)

        # Handles key presses
        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        # If "move", moves the player
        if move:
            dx, dy = move
            player_x += dx
            player_y += dy
        # If "exit", exits game
        if exit:
            return True
        # If "fullscreen"", toggles fullscreen
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
