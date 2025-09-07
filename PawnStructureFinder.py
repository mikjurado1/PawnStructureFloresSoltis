!pip install python-chess -q

#### Upload pgn file

from google.colab import files
uploaded = files.upload()  # Selecciona tu .pgn
# Sugerencia: si subes más de un archivo, usa la clave para elegir el nombre:
pgn_path = list(uploaded.keys())[0]  # o reemplaza por "pgnFourKnightsOpening.pgn"
print("Usando PGN:", pgn_path)


### Find Structure Pawn Andrew Soltis & Flores Ríos

import csv
import os
import chess
import chess.pgn

# ---------- Utilidades de peones ----------

def dragon_black(board):
    import chess
    return (board.piece_at(chess.C5) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.D6) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.G6) == chess.Piece(chess.PAWN, chess.BLACK))

def benko_black(board):
    import chess
    return (board.piece_at(chess.A6) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.B5) == chess.Piece(chess.PAWN, chess.BLACK))

def center_3v3_vs_4v2(board):
    import chess
    return (board.piece_at(chess.C4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.D4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.E4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.C5) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.D6) == chess.Piece(chess.PAWN, chess.BLACK))

def ruy_closed(board):
    import chess
    return (board.piece_at(chess.E4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.D3) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.C3) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.E5) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.D6) == chess.Piece(chess.PAWN, chess.BLACK))

def king_indian_center(board):
    import chess
    return (board.piece_at(chess.D4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.E4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.D6) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.E5) == chess.Piece(chess.PAWN, chess.BLACK))

def fianchetto_white(board):
    import chess
    return (board.piece_at(chess.G3) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.G2) == chess.Piece(chess.BISHOP, chess.WHITE))

def fianchetto_black(board):
    import chess
    return (board.piece_at(chess.G6) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.G7) == chess.Piece(chess.BISHOP, chess.BLACK))

def samisch_white(board):
    import chess
    return (board.piece_at(chess.F3) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.E4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.D4) == chess.Piece(chess.PAWN, chess.WHITE))

def slav_structure(board):
    import chess
    return (board.piece_at(chess.D4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.C4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.D5) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.C6) == chess.Piece(chess.PAWN, chess.BLACK))

def caro_kann_advanced(board):
    import chess
    return (board.piece_at(chess.E5) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.C6) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.E6) == chess.Piece(chess.PAWN, chess.BLACK))

def najdorf_black(board):
    import chess
    return (board.piece_at(chess.A6) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.E6) == chess.Piece(chess.PAWN, chess.BLACK))

def scheveningen_black(board):
    import chess
    return (board.piece_at(chess.D6) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.E6) == chess.Piece(chess.PAWN, chess.BLACK))


def stonewall_white(board):
    import chess
    return (board.piece_at(chess.F4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.E3) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.D4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.C3) == chess.Piece(chess.PAWN, chess.WHITE))

def stonewall_black(board):
    import chess
    return (board.piece_at(chess.F5) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.E6) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.D5) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.C6) == chess.Piece(chess.PAWN, chess.BLACK))

def french_chain(board):
    import chess
    return (board.piece_at(chess.E5) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.D4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.E6) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.D5) == chess.Piece(chess.PAWN, chess.BLACK))

def benoni_asym(board):
    import chess
    return (board.piece_at(chess.D5) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.C5) == chess.Piece(chess.PAWN, chess.BLACK))


def has_p(board, color, sq):
    import chess
    return board.piece_at(sq) == chess.Piece(chess.PAWN, color)

def no_p_on(board, color, files_idx):
    # files_idx es lista de índices de columna: a=0,...,h=7
    for f in files_idx:
        if pawns_on_file(board, color, f):
            return False
    return True

# --- 1) Isolani (IQP)  (ya tenías para d4/d5; lo dejamos por simetría)
def is_isolani_white(board):
    import chess
    return has_p(board, chess.WHITE, chess.D4) and no_p_on(board, chess.WHITE, [2,4])  # sin c ni e
def is_isolani_black(board):
    import chess
    return has_p(board, chess.BLACK, chess.D5) and no_p_on(board, chess.BLACK, [2,4])

def has_white_iqp_d4_strict(board):
    # Sin peones BLANCOS en TODA la columna c ni e
    return (board.piece_at(chess.D4) == chess.Piece(chess.PAWN, chess.WHITE)
            and not pawns_on_file(board, chess.WHITE, 2)  # c-file
            and not pawns_on_file(board, chess.WHITE, 4)) # e-file

def has_black_iqp_d5_strict(board):
    # Sin peones NEGROS en TODA la columna c ni e
    return (board.piece_at(chess.D5) == chess.Piece(chess.PAWN, chess.BLACK)
            and not pawns_on_file(board, chess.BLACK, 2)  # c-file
            and not pawns_on_file(board, chess.BLACK, 4)) # e-file

def has_white_iqp_d4_practical(board):
    import chess
    # Peón en d4 y AUSENCIA total de peones blancos en archivos c y e.
    if board.piece_at(chess.D4) != chess.Piece(chess.PAWN, chess.WHITE):
        return False
    no_c = not pawns_on_file(board, chess.WHITE, 2)  # c-file
    no_e = not pawns_on_file(board, chess.WHITE, 4)  # e-file
    return no_c and no_e

def has_black_iqp_d5_practical(board):
    import chess
    if board.piece_at(chess.D5) != chess.Piece(chess.PAWN, chess.BLACK):
        return False
    no_c = not pawns_on_file(board, chess.BLACK, 2)
    no_e = not pawns_on_file(board, chess.BLACK, 4)
    return no_c and no_e


# --- 2) Peones colgantes
def hanging_white_c4d4(board):
    import chess
    return (has_p(board, chess.WHITE, chess.C4) and has_p(board, chess.WHITE, chess.D4)
            and no_p_on(board, chess.WHITE, [1,4]))  # sin b ni e
def hanging_black_c5d5(board):
    import chess
    return (has_p(board, chess.BLACK, chess.C5) and has_p(board, chess.BLACK, chess.D5)
            and no_p_on(board, chess.BLACK, [1,4]))

# --- 3) Carlsbad (clásica): blancos c4–d4 vs negros c6–d5
def carlsbad_white(board):
    import chess
    return (has_p(board, chess.WHITE, chess.C4) and has_p(board, chess.WHITE, chess.D4)
            and has_p(board, chess.BLACK, chess.C6) and has_p(board, chess.BLACK, chess.D5))

# --- 4) Maróczy: blancos c4+e4; (a menudo con ...c5 de negras)
def maroczy(board):
    import chess
    base = has_p(board, chess.WHITE, chess.C4) and has_p(board, chess.WHITE, chess.E4)
    return base

def maroczy_vs_c5(board):
    import chess
    return maroczy(board) and has_p(board, chess.BLACK, chess.C5)

# --- 5) Hedgehog (Erizo) "esqueleto" típico de negras: a6,b6,d6,e6 y sin peones negros en c5/d5/e5
def hedgehog_black(board):
    import chess
    req = (has_p(board, chess.BLACK, chess.A6) and has_p(board, chess.BLACK, chess.B6) and
           has_p(board, chess.BLACK, chess.D6) and has_p(board, chess.BLACK, chess.E6))
    no_advance = not any(has_p(board, chess.BLACK, sq) for sq in [chess.C5, chess.D5, chess.E5])
    return req and no_advance

# --- 6) Panov (según Flores): cadena blanca d4–c5
def panov_chain_white(board):
    import chess
    return has_p(board, chess.WHITE, chess.D4) and has_p(board, chess.WHITE, chess.C5)  # :contentReference[oaicite:11]{index=11}


def pawns_on_file(board: chess.Board, color: chess.Color, file_idx: int) -> bool:
    pawns = board.pieces(chess.PAWN, color)
    for sq in pawns:
        if chess.square_file(sq) == file_idx:
            return True
    return False

def open_game_e4_e5(board):
    # Centro simétrico típico de Partidas Abiertas
    return (board.piece_at(chess.E4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.E5) == chess.Piece(chess.PAWN, chess.BLACK))

def ruy_italian_d3_structure(board):
    # Plan d3 de Ruy/Italiana: e4+d3 contra e5 (sin d4)
    has_e4 = board.piece_at(chess.E4) == chess.Piece(chess.PAWN, chess.WHITE)
    has_d3 = board.piece_at(chess.D3) == chess.Piece(chess.PAWN, chess.WHITE)
    no_d4  = board.piece_at(chess.D4) != chess.Piece(chess.PAWN, chess.WHITE)
    has_e5 = board.piece_at(chess.E5) == chess.Piece(chess.PAWN, chess.BLACK)
    return has_e4 and has_d3 and no_d4 and has_e5

def black_shell_c6_e5(board):
    # “Concha” negra con …c6 y …e5 (frecuente en muchas líneas contra Bb5)
    has_c6 = board.piece_at(chess.C6) == chess.Piece(chess.PAWN, chess.BLACK)
    has_e5 = board.piece_at(chess.E5) == chess.Piece(chess.PAWN, chess.BLACK)
    return has_c6 and has_e5


def has_white_iqp_d4(board: chess.Board) -> bool:
    if board.piece_at(chess.D4) == chess.Piece(chess.PAWN, chess.WHITE):
        no_c = not pawns_on_file(board, chess.WHITE, 2)  # FILE_C = 2
        no_e = not pawns_on_file(board, chess.WHITE, 4)  # FILE_E = 4
        return no_c and no_e
    return False

# --- IQP flexibles (añadir junto a los otros detectores) ---
def has_white_iqp_d4_flexible(board):
    import chess
    # Igual que práctica (sin peones en c/e), y además sin apoyos avanzados típicos
    # que cambian la etiqueta (evitar confundir con colgantes o centro clásico).
    if not has_white_iqp_d4_practical(board):
        return False
    no_c3 = board.piece_at(chess.C3) != chess.Piece(chess.PAWN, chess.WHITE)
    no_e3 = board.piece_at(chess.E3) != chess.Piece(chess.PAWN, chess.WHITE)
    no_c4 = board.piece_at(chess.C4) != chess.Piece(chess.PAWN, chess.WHITE)
    no_e4 = board.piece_at(chess.E4) != chess.Piece(chess.PAWN, chess.WHITE)
    return no_c3 and no_e3 and no_c4 and no_e4
    
def has_black_iqp_d5_flexible(board):
    import chess
    if not has_black_iqp_d5_practical(board):
        return False
    no_c6 = board.piece_at(chess.C6) != chess.Piece(chess.PAWN, chess.BLACK)
    no_e6 = board.piece_at(chess.E6) != chess.Piece(chess.PAWN, chess.BLACK)
    no_c5 = board.piece_at(chess.C5) != chess.Piece(chess.PAWN, chess.BLACK)
    no_e5 = board.piece_at(chess.E5) != chess.Piece(chess.PAWN, chess.BLACK)
    return no_c6 and no_e6 and no_c5 and no_e5


def has_black_iqp_d5(board: chess.Board) -> bool:
    if board.piece_at(chess.D5) == chess.Piece(chess.PAWN, chess.BLACK):
        no_c = not pawns_on_file(board, chess.BLACK, 2)
        no_e = not pawns_on_file(board, chess.BLACK, 4)
        return no_c and no_e
    return False

def has_white_hanging_c4d4(board: chess.Board) -> bool:
    c4 = board.piece_at(chess.C4) == chess.Piece(chess.PAWN, chess.WHITE)
    d4 = board.piece_at(chess.D4) == chess.Piece(chess.PAWN, chess.WHITE)
    no_b = not pawns_on_file(board, chess.WHITE, 1)  # FILE_B = 1
    no_e = not pawns_on_file(board, chess.WHITE, 4)
    return c4 and d4 and no_b and no_e

def has_black_hanging_c5d5(board: chess.Board) -> bool:
    c5 = board.piece_at(chess.C5) == chess.Piece(chess.PAWN, chess.BLACK)
    d5 = board.piece_at(chess.D5) == chess.Piece(chess.PAWN, chess.BLACK)
    no_b = not pawns_on_file(board, chess.BLACK, 1)
    no_e = not pawns_on_file(board, chess.BLACK, 4)
    return c5 and d5 and no_b and no_e

# ==== Ayudas específicas ====
def count_pawns_on_files(board, color, files_idx):
    import chess
    total = 0
    for f in files_idx:
        for r in range(8):
            if board.piece_at(chess.square(f, r)) == chess.Piece(chess.PAWN, color):
                total += 1
    return total

def doubled_on_file(board, color, file_idx):
    import chess
    cnt = 0
    for r in range(8):
        if board.piece_at(chess.square(file_idx, r)) == chess.Piece(chess.PAWN, color):
            cnt += 1
    return cnt >= 2

# ==== Nuevos detectores ====
def boleslavsky_hole_black(board):
    import chess
    # …d6 + …e5 y SIN peón negro en la columna c (c-file = 2)
    return (board.piece_at(chess.D6) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.E5) == chess.Piece(chess.PAWN, chess.BLACK) and
            not pawns_on_file(board, chess.BLACK, 2))

def boleslavsky_wall(board):
    import chess
    # negro: c6+d6 ; blanco: c4+e4
    return (board.piece_at(chess.C6) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.D6) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.C4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.E4) == chess.Piece(chess.PAWN, chess.WHITE))

def rauzer_formation(board):
    import chess
    # negro: c6+e5 ; blanco: c4+e4
    return (board.piece_at(chess.C6) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.E5) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.C4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.E4) == chess.Piece(chess.PAWN, chess.WHITE))

def d5_chain(board):
    import chess
    # blanca: d5+e4 ; negra: e5+d6
    return (board.piece_at(chess.D5) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.E4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.E5) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.D6) == chess.Piece(chess.PAWN, chess.BLACK))

def closed_sicilian(board):
    import chess
    # blanca: e4+d3 ; negra: c5+d6
    return (board.piece_at(chess.E4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.D3) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.C5) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.D6) == chess.Piece(chess.PAWN, chess.BLACK))

def botvinnik_system(board):
    import chess
    # blanca: c4+e4+d3 ; negra: c5+d6+e5
    return (board.piece_at(chess.C4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.E4) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.D3) == chess.Piece(chess.PAWN, chess.WHITE) and
            board.piece_at(chess.C5) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.D6) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.E5) == chess.Piece(chess.PAWN, chess.BLACK))

def triangle_slav_black(board):
    import chess
    # …c6+…d5+…e6
    return (board.piece_at(chess.C6) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.D5) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.E6) == chess.Piece(chess.PAWN, chess.BLACK))

def noteboom_black(board):
    import chess
    # peones negros avanzados b4 + c4
    return (board.piece_at(chess.B4) == chess.Piece(chess.PAWN, chess.BLACK) and
            board.piece_at(chess.C4) == chess.Piece(chess.PAWN, chess.BLACK))

def berlin_endgame_like(board):
    import chess
    # Dobles peones negros en "c" + mayoría blanca 4v3 en (e,f,g,h)
    doubled_c = doubled_on_file(board, chess.BLACK, 2)
    white_kingside = count_pawns_on_files(board, chess.WHITE, [4,5,6,7])  # e,f,g,h
    black_kingside = count_pawns_on_files(board, chess.BLACK, [4,5,6,7])
    return doubled_c and (white_kingside >= 4) and (black_kingside <= 3)


def has_white_maroczy(board: chess.Board) -> bool:
    return (board.piece_at(chess.C4) == chess.Piece(chess.PAWN, chess.WHITE)
            and board.piece_at(chess.E4) == chess.Piece(chess.PAWN, chess.WHITE))

def classical_center_white(board: chess.Board) -> bool:
    return (board.piece_at(chess.D4) == chess.Piece(chess.PAWN, chess.WHITE)
            and board.piece_at(chess.E4) == chess.Piece(chess.PAWN, chess.WHITE))

def classical_center_black(board: chess.Board) -> bool:
    return (board.piece_at(chess.D5) == chess.Piece(chess.PAWN, chess.BLACK)
            and board.piece_at(chess.E5) == chess.Piece(chess.PAWN, chess.BLACK))

def doubled_pawns_files(board: chess.Board, color: chess.Color):
    files = []
    for f in range(8):
        cnt = 0
        for r in range(8):
            sq = chess.square(f, r)
            if board.piece_at(sq) == chess.Piece(chess.PAWN, color):
                cnt += 1
        if cnt >= 2:
            files.append("abcdefgh"[f])
    return files

def passed_pawns(board: chess.Board, color: chess.Color):
    """Peones pasados (simplificado): sin peones enemigos por delante en mismo/adyacentes archivos."""
    res = []
    enemy = chess.BLACK if color == chess.WHITE else chess.WHITE
    my_pawns = list(board.pieces(chess.PAWN, color))
    for sq in my_pawns:
        f = chess.square_file(sq)
        r = chess.square_rank(sq)
        if color == chess.WHITE:
            ahead = [(ff, rr) for ff in (f-1, f, f+1) for rr in range(r+1, 8) if 0 <= ff <= 7]
        else:
            ahead = [(ff, rr) for ff in (f-1, f, f+1) for rr in range(0, r) if 0 <= ff <= 7]
        blocked = False
        for ff, rr in ahead:
            s2 = chess.square(ff, rr)
            if board.piece_at(s2) == chess.Piece(chess.PAWN, enemy):
                blocked = True
                break
        if not blocked:
            res.append(chess.square_name(sq))
    return res

def compute_structures(board: chess.Board):
    S = set()

    # --- Grupo Siciliana/Benko/Ruy
    if dragon_black(board):
        S.add("Pawn Structure Detected: Siciliana Dragón (…c5 + …d6 + …g6) - Flores & Soltis")
    if benko_black(board):
        S.add("Pawn Structure Detected: Benko/Volga (…a6 + …b5) - Flores & Soltis")
    if center_3v3_vs_4v2(board):
        S.add("Pawn Structure Detected: Centro 3–3 vs 4–2 (blancas c4+d4+e4 vs negras c5+d6) - Flores")
    if ruy_closed(board):
        S.add("Pawn Structure Detected: Ruy Cerrada (blancas e4+d3+c3 vs negras e5+d6) - Flores & Soltis")

    # --- India de Rey
    if king_indian_center(board):
        S.add("Pawn Structure Detected: India de Rey (centro cerrado: d4+e4 vs d6+e5) - Flores & Soltis")
    if fianchetto_white(board):
        S.add("Pawn Structure Detected: Fianchetto blanco (g3+Bg2) - Flores")
    if fianchetto_black(board):
        S.add("Pawn Structure Detected: Fianchetto negro (g6+Bg7) - Flores")
    if samisch_white(board):
        S.add("Pawn Structure Detected: Sämisch (f3+e4+d4) - Flores")

    # --- Slav / Caro-Kann / Najdorf / Scheveningen
    if slav_structure(board):
        S.add("Pawn Structure Detected: Eslava (c4+d4 vs c6+d5) - Flores & Soltis")
    if caro_kann_advanced(board):
        S.add("Pawn Structure Detected: Caro-Kann Avanzada (e5 vs c6+e6) - Flores")
    if najdorf_black(board):
        S.add("Pawn Structure Detected: Najdorf (…a6+…e6) - Flores & Soltis")
    if scheveningen_black(board):
        S.add("Pawn Structure Detected: Scheveningen (…d6+…e6) - Flores & Soltis")

    # --- Stonewall / Francesa / Benoni
    if stonewall_white(board):
        S.add("Pawn Structure Detected: Stonewall blancas (f4,e3,d4,c3) - Flores & Soltis")
    if stonewall_black(board):
        S.add("Pawn Structure Detected: Stonewall negras (f5,e6,d5,c6) - Flores & Soltis")
    if french_chain(board):
        S.add("Pawn Structure Detected: Cadena Francesa (e5–d4 vs e6–d5) - Flores & Soltis")
    if benoni_asym(board):
        S.add("Pawn Structure Detected: Benoni asimétrica (d5 vs c5) - Flores & Soltis")

    # --- Otros patrones menores
    if open_game_e4_e5(board):
        S.add("Pawn Structure Detected: Centro simétrico e4 vs e5 (Partida Abierta) - Soltis")
    if ruy_italian_d3_structure(board):
        S.add("Pawn Structure Detected: Italiana/Ruy con d3 (e4+d3 vs …e5) - Soltis")
    if black_shell_c6_e5(board):
        S.add("Pawn Structure Detected: Concha negra (…c6+…e5) - Soltis")

    # --- Centros clásicos
    if classical_center_white(board):
        S.add("Pawn Structure Detected: Centro clásico blancas (d4+e4) - Flores & Soltis")
    if classical_center_black(board):
        S.add("Pawn Structure Detected: Centro clásico negras (d5+e5) - Flores & Soltis")

    # --- IQP (Isolani) ---
    if has_white_iqp_d4_flexible(board):
        S.add("Pawn Structure Detected: Isolani blancas en d4 (flexible) - Flores & Soltis")
    elif has_white_iqp_d4_practical(board):
        S.add("Pawn Structure Detected: Isolani blancas en d4 (práctico) - Flores & Soltis")
    elif has_white_iqp_d4_strict(board):
        S.add("Pawn Structure Detected: Isolani blancas en d4 (estricto) - Flores & Soltis")

    if has_black_iqp_d5_flexible(board):
        S.add("Pawn Structure Detected: Isolani negras en d5 (flexible) - Flores & Soltis")
    elif has_black_iqp_d5_practical(board):
        S.add("Pawn Structure Detected: Isolani negras en d5 (práctico) - Flores & Soltis")
    elif has_black_iqp_d5_strict(board):
        S.add("Pawn Structure Detected: Isolani negras en d5 (estricto) - Flores & Soltis")

    # --- Hanging pawns ---
    if has_white_hanging_c4d4(board):
        S.add("Pawn Structure Detected: Peones colgantes blancas (c4+d4) - Flores & Soltis")
    if has_black_hanging_c5d5(board):
        S.add("Pawn Structure Detected: Peones colgantes negras (c5+d5) - Flores & Soltis")



    # --- Maróczy / Hedgehog / Panov
    if has_white_maroczy(board):
        S.add("Pawn Structure Detected: Maróczy (c4+e4) - Flores & Soltis")
    if hedgehog_black(board):
        S.add("Pawn Structure Detected: Hedgehog/Erizo (a6,b6,d6,e6 sin …c5/d5/e5) - Flores & Soltis")
    if panov_chain_white(board):
        S.add("Pawn Structure Detected: Panov (d4–c5) - Flores")

    # --- Extras (fuera del catálogo b\u00e1sico Flores/Soltis) ---
    if boleslavsky_hole_black(board):
        S.add("Pawn Structure Detected: Boleslavsky hole (…d6 + …e5, sin peón en columna c) - Wikipedia")
    if boleslavsky_wall(board):
        S.add("Pawn Structure Detected: Boleslavsky Wall (negro c6+d6; blancas c4+e4) - Wikipedia")
    if rauzer_formation(board):
        S.add("Pawn Structure Detected: Rauzer formation (negro c6+e5; blancas c4+e4) - Wikipedia")
    if d5_chain(board):
        S.add("Pawn Structure Detected: d5-chain (d5+e4 vs d6+e5) - Wikipedia")
    if closed_sicilian(board):
        S.add("Pawn Structure Detected: Closed Sicilian (e4+d3 vs …c5+…d6) - Wikipedia")
    if botvinnik_system(board):
        S.add("Pawn Structure Detected: Botvinnik System (c4+e4+d3 vs …c5+d6+e5) - Wikipedia")
    if triangle_slav_black(board):
        S.add("Pawn Structure Detected: Triangle Slav / Semi-Slav (…c6+…d5+…e6) - TheChessWorld/Wikipedia")
    if noteboom_black(board):
        S.add("Pawn Structure Detected: Noteboom (peones negros b4+c4) - Chess.com/ChessPublishing")
    if berlin_endgame_like(board):
        S.add("Pawn Structure Detected: Berlin endgame-like (dobles peones negros en c + 4v3 blanca en flanco de rey) - ChessPathways/Chess.com")


    # --- Otras características
    d_w = doubled_pawns_files(board, chess.WHITE)
    d_b = doubled_pawns_files(board, chess.BLACK)
    if d_w:
        S.add(f"Pawn Structure Detected: Peones doblados blancas en columna {','.join(d_w)} - Soltis")
    if d_b:
        S.add(f"Pawn Structure Detected: Peones doblados negras en columna {','.join(d_b)} - Soltis")
    pp_w = passed_pawns(board, chess.WHITE)
    pp_b = passed_pawns(board, chess.BLACK)
    if pp_w:
        S.add(f"Pawn Structure Detected: Peones pasados blancas en {','.join(pp_w)} - Soltis")
    if pp_b:
        S.add(f"Pawn Structure Detected: Peones pasados negras en {','.join(pp_b)} - Soltis")

    S = apply_suppression_rules(S)
    return S

def _has_label(S, substr):
    return any(substr in s for s in S)

def apply_suppression_rules(S):
    """
    Recibe el set S de etiquetas detectadas y elimina las genéricas
    cuando exista una más específica equivalente.
    """
    S = set(S)  # copia

    # 1) India de Rey (centro cerrado) > Centro clásico blancas
    if _has_label(S, "India de Rey (centro cerrado"):
        S = {s for s in S if "Centro clásico blancas (d4+e4)" not in s}

    # 2) Maróczy contra ...c5 > Maróczy base
    if _has_label(S, "Maróczy contra ...c5"):
        S = {s for s in S if s != "Pawn Structure Detected: Maróczy (c4+e4) - Flores & Soltis"}

    # 3) Carlsbad > Peones colgantes blancas (cuando ambos aparezcan por transición)
    if _has_label(S, "Carlsbad"):
        S = {s for s in S if "Peones colgantes blancas (c4+d4)" not in s}

    # 4) Scheveningen o Najdorf > "Concha negra …c6+…e5" (patrón auxiliar)
    if _has_label(S, "Scheveningen") or _has_label(S, "Najdorf"):
        S = {s for s in S if "Concha negra (…c6+…e5)" not in s}

    # 5) Ruy Cerrada > Italiana/Ruy con d3 (genérico)
    if _has_label(S, "Ruy Cerrada"):
        S = {s for s in S if "Italiana/Ruy con d3" not in s}

    # 6) Hedgehog > Centro 3–3 vs 4–2 (si ambos saltan; Hedgehog es el “nombre canónico”)
    if _has_label(S, "Hedgehog/Erizo"):
        S = {s for s in S if "Centro 3–3 vs 4–2" not in s}

    # 7) Stonewall específico (blancas/negras) > Centro clásico genérico del mismo lado
    if _has_label(S, "Stonewall blancas"):
        S = {s for s in S if "Centro clásico blancas (d4+e4)" not in s}
    if _has_label(S, "Stonewall negras"):
        S = {s for s in S if "Centro clásico negras (d5+e5)" not in s}

    return S



# ---------- Análisis principal (imprime y opcional CSV) ----------
def analyze_pgn(pgn_path: str, csv_out: str = None):
    results = []
    with open(pgn_path, encoding="utf-8", errors="ignore") as f:
        game_idx = 0
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            game_idx += 1

            board = game.board()
            last_seen = set()
            node = game
            while node.variations:
                move = node.variation(0).move
                san = board.san(move)
                board.push(move)

                # 1) Calcula estructuras de la posición ACTUAL
                cur_structs = compute_structures(board)

                # 2) Qué hay de NUEVO en esta jugada
                new_structs = cur_structs - last_seen

                # 3) Imprime solo lo nuevo (incluye Isolani y el resto)
                if new_structs:
                    fullmove = board.fullmove_number
                    mover = "negras" if board.turn == chess.WHITE else "blancas"  # quién movió la jugada previa
                    for s in sorted(new_structs):
                        row = {
                            "game_number": game_idx,
                            "white": game.headers.get("White", ""),
                            "black": game.headers.get("Black", ""),
                            "event": game.headers.get("Event", ""),
                            "structure": s,
                            "move_number": fullmove,
                            "after_move_san": san,
                            "moved_side": mover
                        }
                        results.append(row)
                        print(f"Partida #{row['game_number']} | {row['white']} vs {row['black']} ({row['event']})")
                        print(f"  - {row['structure']}")
                        print(f"  - Detectada en jugada {row['move_number']} tras {row['moved_side']} jugar {row['after_move_san']}\n")

                # 4) Actualiza el conjunto visto y avanza
                last_seen = cur_structs
                node = node.variation(0)

    if csv_out:
        fieldnames = ["game_number","white","black","event","structure","move_number","after_move_san","moved_side"]
        with open(csv_out, "w", newline="", encoding="utf-8") as cf:
            writer = csv.DictWriter(cf, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print("CSV guardado en:", os.path.abspath(csv_out))

# Ejecuta con impresión en pantalla:
import chess, chess.pgn, os

def debug_iqp_all(pgn_file):
    # Abre primer juego del PGN
    with open(pgn_file, encoding="utf-8", errors="ignore") as f:
        game = chess.pgn.read_game(f)

    board = game.board()
    node = game
    ply = 0
    found = False

    print(f"Analizando IQP en: {os.path.basename(pgn_file)}\n")
    print("ply | SAN   | d4 d5 | c3 e3 c4 e4  ||  c6 e6 c5 e5  |  W(flex/prac/strict)  B(flex/prac/strict)")
    print("----+-------+-------+--------------++---------------+----------------------+-------------------")

    while node.variations:
        move = node.variations[0].move
        san = board.san(move)
        board.push(move)
        ply += 1

        # Estados casillas relevantes
        d4 = board.piece_at(chess.D4)
        d5 = board.piece_at(chess.D5)
        c3 = board.piece_at(chess.C3); e3 = board.piece_at(chess.E3)
        c4 = board.piece_at(chess.C4); e4 = board.piece_at(chess.E4)
        c6 = board.piece_at(chess.C6); e6 = board.piece_at(chess.E6)
        c5 = board.piece_at(chess.C5); e5 = board.piece_at(chess.E5)

        # Detectores
        w_flex = has_white_iqp_d4_flexible(board)
        w_prac = has_white_iqp_d4_practical(board)
        w_strc = has_white_iqp_d4_strict(board)

        b_flex = has_black_iqp_d5_flexible(board)
        b_prac = has_black_iqp_d5_practical(board)
        b_strc = has_black_iqp_d5_strict(board)

        # Línea de traza
        def sym(x):  # imprime 'P' si hay peón, '-' si no
            import chess
            return 'P' if x == chess.Piece(chess.PAWN, chess.WHITE) or x == chess.Piece(chess.PAWN, chess.BLACK) else '-'

        print(f"{ply:>3} | {san:<5} | {sym(d4)}  {sym(d5)} | {sym(c3)}  {sym(e3)}  {sym(c4)}  {sym(e4)}  ||  {sym(c6)}  {sym(e6)}  {sym(c5)}  {sym(e5)}  |  "
              f"W({int(w_flex)}/{int(w_prac)}/{int(w_strc)})        B({int(b_flex)}/{int(b_prac)}/{int(b_strc)})")

        # ¿Se detecta algún IQP aquí?
        if any([w_flex, w_prac, w_strc, b_flex, b_prac, b_strc]) and not found:
            print(f"\n➡️ IQP detectado en ply {ply} tras {san}: "
                  f"White[flex={w_flex}, practical={w_prac}, strict={w_strc}] | "
                  f"Black[flex={b_flex}, practical={b_prac}, strict={b_strc}]")
            found = True
            # Si quieres, descomenta para parar en el primer hallazgo:
            # break

        node = node.variations[0]

    if not found:
        print("\n(No se detectó IQP en la línea principal con los detectores actuales.)")

# Ejecuta depuración sobre tu archivo subido:
debug_iqp_all(pgn_path)  # asegúrate de que pgn_path apunta a tu pgnIsolani1.pgn


