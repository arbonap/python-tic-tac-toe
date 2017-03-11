import emoji
import sys
import pdb
import random


# def is_space_free(, ):
    # Return true if the passed move is free on the passed board.
    # return board[move] == ' '
already_seen_position = ''

def who_goes_first():
    """Randomly determines if the human or computer goes first. """
    if random.randint(0,1) == 0:
        return 'X'
    else:
        return 'O'

def play_again():
    print(emoji.emojize("Would you like to play again? (Yes or no) :cherries: ",
                        use_aliases=True))
    return raw_input().lower().startswith('y')

def get_move():
    while True:
        move = raw_input("Please enter a move (from 1-9)> ")
        if move.isdigit() is False:
            print(emoji.emojize("Please input only digits :hibiscus:", use_aliases=True))
        elif len(move) != 1:
            print(emoji.emojize('Please only enter one digit. :exclamation: ',
                                use_aliases=True))
        elif move in already_seen_position:
            print(emoji.emojize("That position on the board has already been taken, please guess another position :crescent_moon:", use_aliases=True))
        else:
            return move

def setup_board():
  """Create an empty tic-tac-toe board.

  Create a board as a list-of-rows, each row being a list-of-cells.

  Put '.' in each cell to mark it as empty.

  Return the board.

  >>> setup_board()
  [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]
  """

  return [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]


def is_board_full(board):
  """Return True is board is full, False otherwise.

  >>> is_board_full([['.', '.', '.'], ['X', '.', 'O'], ['.', '.', '.']])
  False

  >>> is_board_full([['X', 'O', '.'], ['X', 'O', 'X'], ['X', 'O', 'X']])
  False

  >>> is_board_full([['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'O', 'O']])
  True
  """
  for row in board:
      for coli in range(3):
          if row[coli] == '.':
              return False

  return True


def make_random_move(board, player):
  """Find an empty cell and play into it.

  player = 'X' or 'O'

  This should change the board in-place. It should return the
  position (1-9) it played into.

  >>> board = [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'O', '.']]
  >>> make_random_move(board, 'X')
  9

  >>> board
  [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'O', 'X']]
  """
  for rowi in range(3):
      for coli in range(3):
          if board[rowi][coli] == '.':
              board[rowi][coli] = player
              return rowi * 3 + coli + 1

  raise Exception("No more empty spot!")

def find_winner(bd):
  """"Given board, determine if winner. Return 'X', 'O', or None if no winner.

  >>> print find_winner([['.', '.', '.'], ['X', '.', 'O'], ['.', '.', '.']])
  None

  >>> find_winner([['X', '.', '.'], ['X', '.', 'O'], ['X', '.', '.']])
  'X'

  >>> find_winner([['X', 'O', 'X'], ['O', 'O', 'X'], ['O', 'X', 'X']])
  'X'

  >>> find_winner([['X', '.', 'O'], ['X', 'O', 'O'], ['O', '.', '.']])
  'O'
  """
  # Check for win in each row
  for rowi in range(3):
      if bd[rowi][0] != '.' and bd[rowi][0] == bd[rowi][1] == bd[rowi][2]:
          return bd[rowi][0]

  # Check for win in each col
  for coli in range(3):
      if bd[0][coli] != '.' and bd[0][coli] == bd[1][coli] == bd[2][coli]:
          return bd[0][coli]

  # Check for \ diagonal
  if bd[0][0] != '.' and bd[0][0] == bd[1][1] == bd[2][2]:
      return bd[0][0]

  # Check for / diagonal
  if bd[2][0] != '.' and bd[2][0] == bd[1][1] == bd[0][2]:
      return bd[2][0]

def print_board(board):
  """Given a board[col][row], print it.

  >>> print_board([['.', '.', '.'], ['X', '.', 'O'], ['.', '.', '.']])
  . . .
  X . O
  . . .
  """

  for row in board:
      for cell in row:
          print cell,
      print


def make_move(board, position, player):
  """Play into position 1-9.

  position = 1-9 (top-left, top-middle, top-right ... bottom-right)
  player = 'X' or 'O'

  Updates board.

  >>> board = [['X', '.', 'O'], ['X', 'O', 'O'], ['O', '.', '.']]

  >>> make_move(board, 2, 'O')
  >>> board
  [['X', 'O', 'O'], ['X', 'O', 'O'], ['O', '.', '.']]

  >>> make_move(board, 9, 'X')
  >>> board
  [['X', 'O', 'O'], ['X', 'O', 'O'], ['O', '.', 'X']]
  """

  coli, rowi = divmod(position - 1, 3)

  board[coli][rowi] = player


def tic_tac_toe_game():
      """Tic-tac-toe implementation--

      The human will be X and the computer will be O.

      Loop:
      - Show the board
      - If it's the human's turn, prompt for a position (1-9) and make their move
      - If it's the computer's turn, make any legal move
      - If there's a winner or the board is full, quit the game

      Annouce winner, if any.
      """
      global already_seen_position

      board = setup_board()
      current_player = who_goes_first()
      winner = None
      full = False

      print(emoji.emojize("Welcome to a :snake: Pythonic :snake: tic-tac-toe game! \nLet's begin, shall we?", use_aliases=True))
      print(emoji.emojize("Please wait while the first player is being randomly generated :four_leaf_clover:", use_aliases=True))

      while not winner and not is_board_full(board):
          print
          print_board(board)
          print
          if current_player == 'X':
              print(emoji.emojize("It's your turn, please enter a digit :blue_heart:", use_aliases=True))
              move = get_move()
              already_seen_position += move
            #   pdb.set_trace()
              position = int(move)
              make_move(board, position, 'X')
              current_player = 'O'
          else:
              print(emoji.emojize("It's the computer's turn, please wait...:purple_heart:", use_aliases=True))
              position = make_random_move(board, 'O')
              print(emoji.emojize("It's your turn, please enter a digit :blue_heart:", use_aliases=True))
              print(emoji.emojize("The computer :computer:, Player O, played in position %s" % position, use_aliases=True))
              current_player = 'X'

          winner = find_winner(board)

      if winner:
          print(emoji.emojize(":tada:Congratulations to " + winner + ":sparkles: :raised_hands: ", use_aliases=True))
      else:
          print(emoji.emojize("~It's a tie~ :musical_note:", use_aliases=True))

      if play_again():
          board = setup_board()
          current_player = who_goes_first()
          winner = None
          full = False
          already_seen_position = ''

      else:
          print(emoji.emojize("Goodbye! Have a wonderful day :sunny:", use_aliases=True))
          sys.exit()

if __name__ == "__main__":
  # import sys
  #
  # if len(sys.argv) > 1 and sys.argv[1] == '--test':
  #     import doctest
  #
  #     if doctest.testmod().failed == 0:
  #         print "\nTests passed! Hooray!\n"
  # else:
    tic_tac_toe_game()
