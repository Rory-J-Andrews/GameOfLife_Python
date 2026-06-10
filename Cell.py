# The object of each cell.
class Cell:
    # Initializes the cell and sets up its qualities.
    def __init__(self, x, y, sideLength):
        # We se the upper-left coordinate, and then derive the lower-right coord from the
        # length of the cell sides decided by the program.
        self.lower_x = x
        self.lower_y = y
        self.upper_x = self.lower_x + sideLength
        self.upper_y = self.lower_y + sideLength

        # We set all relationships to be None by default.
        self.up = self.down = self.left = self.right = self.up_left = self.up_right \
            = self.down_left = self.down_right = None

        # Indicates whether the cell is currently alive.
        self.alive = False

        # Indicates whether the cell was alive on the previous frame.
        self.was_alive = False

    # Sets the pointers to the cell's neighbors.
    def set_connections(self, up, down, left, right, up_left, up_right, down_left, down_right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.up_left = up_left
        self.up_right = up_right
        self.down_right = down_right
        self.down_left = down_left

    # Brings the cell to life.
    def set_alive(self):
        self.alive = True

    # Terminates the cell (with love and gratitude).
    def set_dead(self):
        self.alive = False

    # Notes that the cell was previously alive.
    def set_was_alive(self):
        self.was_alive = True

    # Notes that the cell was previous dead.
    def set_was_dead(self):
        self.was_alive = False

    # Returns the number of live neighbors the cell had in the previous frame.
    def how_many_prev_live_neighbors(self) -> int:
        count = 0
        try:
            if self.up.was_alive:
                count += 1
        except: pass
        try:
            if self.down.was_alive:
                count += 1
        except: pass
        try:
            if self.left.was_alive:
                count += 1
        except: pass
        try:
            if self.right.was_alive:
                count += 1
        except: pass
        try:
            if self.up_left.was_alive:
                count += 1
        except: pass
        try:
            if self.up_right.was_alive:
                count += 1
        except: pass
        try:
            if self.down_left.was_alive:
                count += 1
        except: pass
        try:
            if self.down_right.was_alive:
                count += 1
        except: pass
        return count