import libtcodpy as libtcod

# Fucntion that processes the pressed key
def handle_keys(key):
    # Movement keys
    # Returns a dictionary with key "move" and 2 numbers as value
    # Numbers represent the x and y axes
    if key.vk == libtcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN:
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {'move': (1, 0)}

    # ALT+Enter
    # Returns a dictionary with key "fullscreen" and True as value
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Toggle full screen
        return {'fullscreen': True}

    # ESC
    # Returns a dictionary with key "exit" and True as value
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}
