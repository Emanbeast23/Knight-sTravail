# Knight-sTravail

# Chess Knight Pathfinding

This project is a visual simulation of a chess knight's pathfinding on an 8x8 chessboard using **A*** and **Dijkstra's algorithm**. Users can select a starting and ending position for the knight, and the program calculates and visualizes the shortest path between the two points.

---

## Features
- Interactive 8x8 chessboard for user input.
- Real-time visualization of the knight's path.
- Implementation of **A*** and **Dijkstra's algorithm** for shortest-path computation.
- Option to toggle between the two algorithms.
- Reset functionality to select new positions.

---

## How to Run
1. **Install Python**:
   Ensure you have Python 3.7 or later installed on your system. Download it [here](https://www.python.org/downloads/).

2. **Install Pygame**:
   Install the Pygame library by running:
   ```bash
   pip install pygame
   ```

3. **Clone or Download the Repository**:
   Clone the repository using Git or download the ZIP file and extract it:
   ```bash
   git clone https://github.com/Emanbeast23/KnightsTravail.git
   cd KnightsTravail
   ```

4. **Add Assets**:
   Ensure the `assets` folder includes the following:
   - `chessboard.jpg`: A chessboard image.
   - `knight.png`: A knight chess piece image.
   - `pawn.png`: Optional pawn image (currently unused).
   - `RobotoMono.ttf`: Font file for rendering text.

5. **Run the Program**:
   Run the Python script:
   ```bash
   python knight_pathfinding.py
   ```

---

## How to Use
1. **Select Start and Goal**:
   - Click a square on the chessboard to place the knight's starting position.
   - Click another square to set the goal.

2. **View the Results**:
   - The shortest path is displayed with step numbers and a graphical knight icon.
   - A* or Dijkstra's algorithm calculates the path based on the current toggle state.

3. **Switch Algorithms**:
   - Press `SPACE` to toggle between **A*** and **Dijkstra** algorithms.
   - Results update instantly after switching.

4. **Reset the Board**:
   - Press `Left Shift` to clear the board and select new positions.

---

## Keyboard Shortcuts
| Key         | Action                        |
|-------------|-------------------------------|
| `Left Shift`| Reset the chessboard          |
| `SPACE`     | Toggle between A* and Dijkstra|

---

## Dependencies
- **Python 3.7+**
- **Pygame** library

---

## Screenshots
*(Add screenshots of the program showing the knight's path and the chessboard here.)*

---

## Future Improvements
- Add support for additional chess pieces.
- Allow for dynamic board resizing.
- Include more detailed visualizations for algorithm processing.

---

## License
This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
