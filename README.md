# GameOfLife_Python

This was originally made in mid-2024 as a fun demo. In mid-2026 I reviewed and substantially updated it, adding new features, greatly improving the algorithms, adding documentation, and python-ifying the code conventions.

The Game of Life is a fun little "simulation" of cell dynamics. It can be used to investigate emergent complexity, self-perpetuating systems, and cyclic patterns (it can also be used to screw around, which is almost as good.) It was designed by the mathematician James Conway. 
If you want to learn more, I'd recommend the Wikipedia page: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

The game uses an undirected graph as its central data structure. Each cell is is a vertex, and each vertex is connected by pointers (the edges) to its 8-or-less nearby neighbors. The cells themselves are contained in a 2D array. 

Features:
- Pausing
- Speed settings
- Wrapped or unwrapped mode (i.e., whether one edge of the screen should be connected to the opposite)
- Resetting
- Updating window caption that reflects the current settings  

This program uses pygame for its display.
