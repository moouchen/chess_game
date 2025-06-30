import pygame
import chess
import sys

pygame.init()

screenWidth = 480
screenHeight = 480
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("WolfChess")
icon = pygame.image.load("pics/nb.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
chessBoard = chess.Board()

# Your original naming for pieces and board setup
board = [
    ["rb", "nb", "bb", "qb", "kb", "bb", "nb", "rb"],
    ["b",  "b",  "b",  "b",  "b",  "b",  "b",  "b" ],
    ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
    ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
    ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
    ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
    ["w",  "w",  "w",  "w",  "w",  "w",  "w",  "w" ],
    ["rw", "nw", "bw", "qw", "kw", "bw", "nw", "rw"],
]

squares = [
    ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'],
    ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'],
    ['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'],
    ['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'],
    ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'],
    ['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'],
    ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],
    ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
]

pieces = []
selected_piece = None
move = None
from_sq = None
to_sq = None
original_piece_x = None
original_piece_y = None

#sounds 
moveS = pygame.mixer.Sound('sounds/move.mp3')
captureS = pygame.mixer.Sound('sounds/capture.mp3')
castleS = pygame.mixer.Sound('sounds/castle.mp3')
checkS = pygame.mixer.Sound('sounds/check.mp3')
promoteS = pygame.mixer.Sound('sounds/promote.mp3')
gameEndS = pygame.mixer.Sound('sounds/game-end.mp3')
illegalS = pygame.mixer.Sound('sounds/illegal.mp3')


class Square:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60

class Piece:
    def __init__(self, type_str, x, y):
        self.type = type_str
        self.x = x
        self.y = y
        self.img = pygame.image.load(f'pics/{type_str}.png')
        self.taked = False

    def __str__ (self):
        return f"type :  {self.type} , x : {self.x} , y : {self.y} , taked : {self.taked}"


def draw_squares(win):
    for row in SqBoard:
        for square in row:
            pygame.draw.rect(win, square.color, (square.x, square.y, square.width, square.height))

def draw_pieces(win):
    for piece in pieces:
        if not piece.taked:
            win.blit(piece.img, (piece.x, piece.y))

def get_piece_at_pixel(x, y):
    for piece in pieces:
        if not piece.taked:
            if piece.x <= x < piece.x + 60 and piece.y <= y < piece.y + 60:
                return piece
    return None

def get_piece_at_square(rank, file):
    px = file * 60
    py = rank * 60
    for piece in pieces:
        if not piece.taked and piece.x == px and piece.y == py:
            return piece
    return None

def is_white(piece_type):
    # white pieces end with 'w' or are just 'w' for pawn
    return piece_type.endswith('w') or piece_type == 'w'

def is_black(piece_type):
    # black pieces end with 'b' or are just 'b' for pawn
    return piece_type.endswith('b') or piece_type == 'b'

def checkmate():
    if chessBoard.is_checkmate():
        font_big = pygame.font.SysFont("comicsansms", 80, bold=True)
        font_shadow = pygame.font.SysFont("comicsansms", 80, bold=True)
        message = "🔥 Checkmate! 🔥"

        # Play sound first
        gameEndS.play()

        # Create a dimmed background
        overlay = pygame.Surface((screenWidth, screenHeight))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Text positions
        text_surface = font_big.render(message, True, (255, 50, 50))
        shadow_surface = font_shadow.render(message, True, (0, 0, 0))

        x = (screenWidth - text_surface.get_width()) // 2
        y = (screenHeight - text_surface.get_height()) // 2

        # Blit shadow and then text
        screen.blit(shadow_surface, (x + 4, y + 4))
        screen.blit(text_surface, (x, y))

        pygame.display.update()
        pygame.time.wait(3000)

        pygame.quit()
        sys.exit()

def stalemate():
    if chessBoard.is_stalemate():
        font_big = pygame.font.SysFont("comicsansms", 72, bold=True)
        font_shadow = pygame.font.SysFont("comicsansms", 72, bold=True)
        message = "😐 Stalemate! It's a Draw!"

        # Play draw sound effect if you have one
        # drawS.play()

        # Dim background
        overlay = pygame.Surface((screenWidth, screenHeight))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Render shadow and main text
        text_surface = font_big.render(message, True, (200, 200, 50))
        shadow_surface = font_shadow.render(message, True, (0, 0, 0))

        x = (screenWidth - text_surface.get_width()) // 2
        y = (screenHeight - text_surface.get_height()) // 2

        screen.blit(shadow_surface, (x + 4, y + 4))
        screen.blit(text_surface, (x, y))

        pygame.display.update()
        pygame.time.wait(3000)

        pygame.quit()
        sys.exit()



def action():
    global selected_piece, from_sq, to_sq, move, original_piece_x, original_piece_y

    mouse_x, mouse_y = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()[0]

    if pressed:
        if selected_piece is None:
            piece = get_piece_at_pixel(mouse_x, mouse_y)
            if piece:
                # Only allow selecting piece if it's that player's turn
                if (chessBoard.turn and is_white(piece.type)) or (not chessBoard.turn and is_black(piece.type)):
                    selected_piece = piece
                    original_piece_x = piece.x
                    original_piece_y = piece.y
                    from_sq = squares[piece.y // 60][piece.x // 60]
                    board[piece.y // 60][piece.x // 60] = "  "
        else:
            selected_piece.x = mouse_x - 30
            selected_piece.y = mouse_y - 30
    else:
        if selected_piece is not None:
            placed_on_square = None
            for row in SqBoard:
                for square in row:
                    if square.x <= mouse_x < square.x + 60 and square.y <= mouse_y < square.y + 60:
                        placed_on_square = square
                        break
                if placed_on_square:
                    break

            if placed_on_square:
                to_sq = squares[placed_on_square.y // 60][placed_on_square.x // 60]

                if from_sq != to_sq:
                    move_uci = from_sq + to_sq

                    # Handle promotion for white pawn reaching rank 8 or black pawn rank 1
                    if (selected_piece.type == 'w' and to_sq[1] == '8') or (selected_piece.type == 'b' and to_sq[1] == '1'):
                        promote = ''
                        while promote not in ['q', 'r', 'b', 'n']:
                            promote = input("Promote to (q, r, b, n): ").lower()
                        move_uci += promote
                        selected_piece.type = promote+selected_piece.type
                        selected_piece.img = pygame.image.load(f'pics/{selected_piece.type}.png')
                        promoteS.play()


                    move = chess.Move.from_uci(move_uci)
                    if move in chessBoard.legal_moves:
                        
                        # Capture logic
                        target_piece = get_piece_at_square(placed_on_square.y // 60, placed_on_square.x // 60)
                        if target_piece and target_piece != selected_piece:
                            target_piece.taked = True
                            captureS.play()

                        # Handle en passant capture
                        if chessBoard.is_en_passant(move):
                            ep_rank = placed_on_square.y // 60 + (1 if chessBoard.turn else -1)
                            ep_file = placed_on_square.x // 60
                            ep_captured = get_piece_at_square(ep_rank, ep_file)
                            if ep_captured:
                                ep_captured.taked = True
                            board[ep_rank][ep_file] = "  "
                            captureS.play()
                        
                        # Handle castling rook movement on GUI pieces
                        if chessBoard.is_castling(move):
                            castleS.play()
                            # White short castle
                            if move_uci == 'e1g1':
                                rook = get_piece_at_square(7, 7)
                                print(rook)
                                if rook :
                                    print(rook)
                                    rook.x = 5 * 60
                                    rook.y = 7 * 60
                                    board[7][7] = "  "
                                    board[7][5] = "rw"

                            # White long castle
                            elif move_uci == 'e1c1':
                                rook = get_piece_at_square(7, 0)
                                if rook:
                                    rook.x = 3 * 60
                                    rook.y = 7 * 60
                                    board[7][0] = "  "
                                    board[7][3] = "rw"
                            # Black short castle
                            elif move_uci == 'e8g8':
                                rook = get_piece_at_square(0, 7)
                                if rook:
                                    rook.x = 5 * 60
                                    rook.y = 0
                                    board[0][7] = "  "
                                    board[0][5] = "rb"
                            # Black long castle
                            elif move_uci == 'e8c8':
                                rook = get_piece_at_square(0, 0)
                                if rook:
                                    rook.x = 3 * 60
                                    rook.y = 0
                                    board[0][0] = "  "
                                    board[0][3] = "rb"
                        
                        #checkmate
                        if chessBoard.gives_check(move):
                            checkS.play()
                            
                        else : moveS.play()

                        # Push move to chess engine
                        chessBoard.push(move)

                        # Update board GUI
                        board[placed_on_square.y // 60][placed_on_square.x // 60] = selected_piece.type
                        selected_piece.x = placed_on_square.x
                        selected_piece.y = placed_on_square.y
                        board[original_piece_y // 60][original_piece_x // 60] = "  "

                        checkmate()
                        stalemate()

                    else:
                        # Illegal move, revert position and board
                        selected_piece.x = original_piece_x
                        selected_piece.y = original_piece_y
                        board[original_piece_y // 60][original_piece_x // 60] = selected_piece.type
                        illegalS.play()
                else:
                    # Same square, revert
                    selected_piece.x = original_piece_x
                    selected_piece.y = original_piece_y
                    board[original_piece_y // 60][original_piece_x // 60] = selected_piece.type
            else:
                # Dropped outside board, revert
                selected_piece.x = original_piece_x
                selected_piece.y = original_piece_y
                board[original_piece_y // 60][original_piece_x // 60] = selected_piece.type

            selected_piece = None

def redraw_screen():
    draw_squares(screen)
    draw_pieces(screen)
    pygame.display.update()

# Create squares
SqBoard = []
for row in range(8):
    boardRow = []
    for col in range(8):
        color = (118, 150, 86) if (row + col) % 2 == 0 else (238, 238, 210)
        square = Square(color, col * 60, row * 60)
        boardRow.append(square)
    SqBoard.append(boardRow)

# Create pieces from board array
pieces.clear()
for y in range(8):
    for x in range(8):
        if board[y][x] != "  ":
            piece = Piece(board[y][x], x * 60, y * 60)
            pieces.append(piece)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)
    action()
    redraw_screen()

pygame.quit()
