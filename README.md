# Halma

<img width="400" alt="Screenshot 2023-03-31 at 7 41 28 PM" src="https://user-images.githubusercontent.com/63039479/229101012-1efe1fb2-6198-4ffc-b2c8-4f1cbd5a7119.png">

## Description

<p>This is a Python implementation of the board game Halma, using the Pygame library for the graphical user interface.
Halma is a two-player strategy board game invented in the 19th century. This version of the game is played on an 8x8 square board between a player and the computer. Similar to the game Chinese Checkers, gameplay involves players taking turns moving their pieces from their starting corner of the board into the opposite corner before their opponent.
<p>

### Features
- Single-player gameplay against an AI opponent
- AI opponent utilizes the minimax algorithm with alpha-beta pruning to make its moves
- Graphical user interface using the Pygame library for an enjoyable playing experience
- Game board displays valid potential moves for the player

### Motivation

I decided to build this project after finishing my second quarter as a CS student at Oregon State University. My motivation for the project was to apply some of the heavy concepts I've learned so far in my coursework towards a tangible working product. Working on this game pushed me to get my hands dirty with larger scale Object Oriented Programming, recursion, modules, and thorough documentation as well as the opportunity to learn more about AI.

### Challenges

<p>While I ran into many challenges while working on this project, the two biggest ones were move validation and evaluating states of the game board to enable proper decision making by the AI.
<p>

#### Move Validation

<p>Enforcing proper move validation was the biggest hurdle I had to overcome during this build. In Halma, players may move a piece to any empty adjacent square in any of the eight directions surrounding their piece. If such a move is made, their turn ends. Players may also make a jump over any adjacent piece of any color into an empty space on the other side of that piece. Multiple jumps can be chained together in a single move as long as each jump is over a different piece and into an unvisited space.
<p>

The solution came down to building a list of all valid moves into adjacent spaces with a helper function and adding all valid jumps to that list using a separate recursive function. 

#### Evaluation

The other main challenge I faced was writing an evaluation function that properly informed the AI's movements based on the current state of the game board. While I tried out different factors such as central control of the board, and blocking opposing pieces, I eventually settled on evaluation based on three factors:

1. Distance between each player's pieces and the opposing starting zone
2. Number of pieces in the opponent's starting zone
3. Penalty for pieces remaining in their own starting zone

The three factors are determined as numeric values and totaled as a floating-point number representing the evaluation score. The final stage of development for the project as a whole, came down to playing test games against the AI and adjusting the weight of these three factors to facilitate the strongest decision making by the AI.

## About the AI
<img src="https://user-images.githubusercontent.com/63039479/229261936-c99157d1-437b-45f5-9aad-bcb135cbebc7.gif" alt="Halma10" style="width: 400px;">

<p>The GIF above illustrates the minimax algorithm in action as the AI calculates its first move in a game
<p>

In the minimax algorithm, the AI simulates future moves by both itself and the opponent. It then chooses the move that leads to the best possible outcome, assuming the opponent will also make the best possible move in response. This process continues recursively, with the AI looking ahead to future moves and the opponent's responses, until a certain depth is reached or a winning outcome is found. The algorithm also uses alpha-beta pruning to speed up the search by cutting off branches that are known to lead to worse outcomes.


## Requirements
- Python 3.x
- Pygame library

## Installation
1. Clone the repository to your local machine
2. Install the Pygame library: pip install pygame
3. Run the game using the command: python main.py

## How to Play
<img src="https://user-images.githubusercontent.com/63039479/229262690-1195eef6-0823-4d85-8ad8-7167b332cb7f.gif" alt="Halma Play" width="400"/>

- The player competes against the AI opponent to move
- Use the mouse to select and move pieces, and to see the available moves for each piece
- The game ends when one player moves all their pieces from their starting zone to the opposite corner before their opponent


