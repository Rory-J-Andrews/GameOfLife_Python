import math
import sys
import Cell
import pygame
import time

# Creates the array that contains the cells.
# The key data structure here in an undirected, unweighted graph. Each cell represents as a vertex,
# and each cell knows its neighbors via pointers, i.e. the edges.
# The graph is stored as a 2D array, with each individual sub-array representing a new row,
# starting from the top row and leftmost column.
def create_cell_array():
    # Initializes array of cells, and the current position to iterate from.
    cell_array = []
    x = 0; y = 0

    # Creates the needed amount of rows.
    for row_index in range(0, amount_rows):
        # Creates a temporary array to store the current row.
        row = []
        # Adds each cell for each column of the row.
        for col_index in range(0, amount_columns):
            cell = Cell.Cell(x, y, cell_side_length)
            row.append(cell)
            y = y + cell_side_length
        # Adds the current row to array, and resets position.
        cell_array.append(row)
        x = x + cell_side_length
        y = 0
    return cell_array

# Returns the cell contained at a given coordinate in the array.
# If wrapped mode is enabled, then it uses modulo to find the "wrapped cell".
# If wrapped mode is disabled, it checks that the coordinate is in bounds; if not, it returns None.
def cell_from_coords(x, y):
    if not IS_WRAPPED:
        if not 0<= x < amount_rows or not 0<= y < amount_columns:
            return None
        else:
            return cell_array[x][y]
    else:
        return cell_array[x % amount_rows][y % amount_columns]

# For each cell in the array, sets the pointers to its neighbors, with help from the previous method.
def set_cell_connections():
    for row in cell_array:
        curr_row_index = cell_array.index(row)
        for cell in row:
            curr_col_index = row.index(cell)

            up = cell_from_coords(curr_row_index-1, curr_col_index)
            down = cell_from_coords(curr_row_index+1, curr_col_index)
            left = cell_from_coords(curr_row_index, curr_col_index-1)
            right = cell_from_coords(curr_row_index, curr_col_index + 1)
            up_left = cell_from_coords(curr_row_index-1, curr_col_index-1)
            up_right = cell_from_coords(curr_row_index-1, curr_col_index+1)
            down_left = cell_from_coords(curr_row_index+1, curr_col_index-1)
            down_right = cell_from_coords(curr_row_index+1, curr_col_index+1)

            cell.set_connections(up, down, left, right, up_left, up_right, down_left, down_right)

# If not paused, updates the cells according to the state of the previous frame and the rules of the GoL.
def update_cells():
    if not PAUSED:
        for row in cell_array:
            for cell in row:
                # Obtains the number of living neighbors.
                num_prev_live_neighbors = cell.how_many_prev_live_neighbors()

                # If the cell is alive, then:
                # - If it has less than two or more than live neighbors, it will die.
                # - Else, it stays alive for the next round.
                if cell.alive:
                    if num_prev_live_neighbors < 2 or num_prev_live_neighbors > 3:
                        cell.set_dead()
                # If the cell is dead, and it has exactly 3 live neighbors, then it will become alive.
                else:
                    if num_prev_live_neighbors == 3:
                        cell.set_alive()

# Sets all cells to dead.
def reset_cells():
    for row in cell_array:
        for cell in row:
            cell.set_dead()

# Draws the grid and the cells onto the pygame screen.
# Also sets cells' current status to their previous status, to be used by the next update loop.
def draw_cells(screen):
    # Fills the screen with a black background.
    screen.fill((0, 0, 0))
    # Using the info of the side lengths for each cell, we draw white lines to separate each.
    # By default, each cell is black.
    w = screen.get_size()[0]

    # For each factor of the cell side length, we draw straight vertical and horizontal lines as a grid.
    for i in range(1, int(math.sqrt(amount_cells)) + 1):
        # Draws each vertical white line.
        pygame.draw.line(screen, (255, 255, 255), (int(i * cell_side_length), 0),
                         (int(i * cell_side_length), w), 1)
        # Draws each horizontal white line.
        pygame.draw.line(screen, (255, 255, 255), (0, int(i * cell_side_length)),
                         (w, int(i * cell_side_length)), 1)

    # For each cell, if it is alive, we fill in a corresponding white square.
    for row in cell_array:
        for cell in row:
            if cell.alive:
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(cell.lower_x, cell.lower_y,
                                                                cell_side_length+1, cell_side_length+1))
                cell.set_was_alive()
            else:
                cell.set_was_dead()

# Returns the cell found at a given position of the mouse.
#
# Instead of asking every cell individually, we use modular arithmetic to reduce mouse position
# to a factor of the cell side length, then math.floor that to the greatest less-than integer;
# this we use as the coordinate for the cell array.
def cell_from_pos(x, y):
    row_index = math.floor(x / cell_side_length)
    col_index = math.floor(y / cell_side_length)
    try:
        return cell_array[row_index][col_index]
    except:
        return None

# Changes the caption of the screen to reflect settings.
def set_caption():
    caption = ("Game of Life   |   " + paused_caption + ",  " + speed_caption + ",  " + wrapped_caption +
               "   |   Reset [R]")
    pygame.display.set_caption(caption)

# Sets the size of the window and initializes the pygame screen.
window_sides_length = 800
pygame.init()
screen = pygame.display.set_mode([window_sides_length, window_sides_length])
running = True

# Sets up the amount of cells.
# You can change it, but you must put in a square number; else the program will terminate.
amount_cells = 900

# Checks to see if the square root of the amount of cells is an integer,
# i.e. if the amount of cells inputted is a square number.
if math.sqrt(amount_cells) != int(math.sqrt(amount_cells)):
    print("The amount of cells must be a square number.")
    sys.exit()

# Obtains the required length of the sides of each cell.
# Each cell is square, and the number of rows / columns is the same, so we just
# divide the window side length by the square of the amount of cells.
# CHANGE THIS TO cell_side_length
cell_side_length = window_sides_length / int(math.sqrt(amount_cells))

# Sets amountRows and amountColumns to be equal to the square of the amount of cells.
amount_rows = int(math.sqrt(amount_cells)); amount_columns = int(math.sqrt(amount_cells))

# Decides whether the grid is wrapped or not -- i.e. whether the game-world is a finite plane or a torus :)
IS_WRAPPED = True
# Sets the game to be paused by default.
PAUSED = True

# Creates the data structure of the cell array, and sets the connections each cell.
cell_array = create_cell_array()
set_cell_connections()

# Sets some input options to be false at the start.
space_down = space_down_last = mouse_down = r_down = r_down_last = s_down = s_down_last = w_down \
    = w_down_last = False

# The program keeps track of time by taking the difference of the time of the current update loop from
# the time the game started. It checks to see if the time modulo 2 = 0 or 1; if the game has not updated
# on that modulo yet, then it updates.
# This technique is done to avoid the issue of especially long update loops "missing" the exact integer
# values of time.
start = time.time()
update_on_mod = 1

# The 5 speeds available, each as "(Speed) updates per second".
speed_choices = [.25, .5, 1, 2, 4]
# The default speed is set to 1/second.
speed_index = 2

# The caption of the window shows button ifo, and updates depending on the current settings.
paused_caption = "Paused [SPACE]"
speed_caption = "Speed: 1x/s [S]"
wrapped_caption = "Wrapped [W]"
set_caption()

# This is the fundamental update loop.
while running:
    # Collects data on any button pressing that's happened.
    # Most of these are self-explanatory.
    for event in pygame.event.get():
        # If the exit button has been pressed, then we let the program know to stop running.
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_down = True
            if event.key == pygame.K_r:
                r_down = True
            if event.key == pygame.K_s:
                s_down = True
            if event.key == pygame.K_w:
                w_down = True

    # If the mouse is being clicked, we obtain the cell at that point.
    # If there is no cell, the helper method will return None, and nothing happens.
    if mouse_down:
        mouseX, mouseY = pygame.mouse.get_pos()
        try:
            cell_from_pos(mouseX, mouseY).set_alive()
        except: pass

    # Checks if the spacebar is currently being held down, AND it was not also held down
    # on the previous update loop, to keep input effects precisely on the first moment.
    if space_down and not space_down_last:
        # If currently unpaused, switches to paused, and updates the caption.
        if not PAUSED:
            PAUSED = True
            paused_caption = "Paused [SPACE]"
            set_caption()

        # If currently paused, switches to unpaused, and updates the caption.
        # We also reset the time, and set the next update to be on mod 2 = 1; that way, upon unpausing
        # there is a guarenteed break before the next update.
        elif PAUSED:
            PAUSED = False
            start = time.time()
            update_on_mod = 1
            paused_caption = "Unpaused [SPACE]"
            set_caption()
        space_down_last = True

    # If the space bar is not at all being held down, we set spaceBarLast to be False, so that
    # on the next loop the program knows the button was not pressed on the last frame.
    elif not space_down:
        space_down_last = False
    # After this, spaceDown is set to False; this is because our previous code doesn't automatically
    # check for a button *not* being pressed, only if it is.
    # We work around this by setting space_down to be false at the start of every frame by default.
    space_down = False

    # If R is pressed, reset the cells.
    # Similar general implementation to the spacebar.
    if r_down and not r_down_last:
        reset_cells()
        r_down_last = True
    elif not r_down:
        r_down_last = False
    r_down = False

    # If S is pressed, we swap to the next speed.
    # Similar general presentation to the spacebar.
    if s_down and not s_down_last:
        # We iterate to the next entry in the list, wrapping back to the first if needed.
        speed_index = (speed_index + 1) % len(speed_choices)

        # We update the caption.
        speed_caption = "Speed: " + str(speed_choices[speed_index]) + "x/s [S]"
        set_caption()
        # We reset the time, reducing discontinuous "jumping" between speed switches.
        start = time.time()
        updateOnMod = 1

        sDownLast = True
    elif not s_down:
        s_down_last = False
    s_down = False

    # If W is pressed, we swap between wrapped and unwrapped.
    # Similar general presentation to the spacebar.
    if w_down and not w_down_last:
        # Swap whether the game is wrapped, and reset the cell connections accordingly.
        IS_WRAPPED = not IS_WRAPPED
        set_cell_connections()

        # We update the captions.
        if IS_WRAPPED:
            wrapped_caption = "Wrapped [W]"
        else:
            wrapped_caption = "Unwrapped [W]"
        set_caption()

        w_down_last = True
    elif not w_down:
        w_down_last = False
    w_down = False

    # Determines whether to update, based on the algorithm described before.
    # The speed effect is achieved by multiplying the current time, achieving a "slowdown" or
    # "stretching" effect on the time difference in the program's eyes.
    second = math.floor(speed_choices[speed_index] * (time.time() - start))
    if second % 2 == 0 and update_on_mod == 0:
        update_cells()
        update_on_mod = 1
    elif second % 2 == 1 and update_on_mod == 1:
        update_cells()
        update_on_mod = 0

    # Finally, we draw the cells on the window, and let pygame update the display.
    draw_cells(screen)
    pygame.display.flip()

# When the loop has been ended, we end the program.
pygame.quit()
