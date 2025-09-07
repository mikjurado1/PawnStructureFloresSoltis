index e6d8d4f7d1fb24de9ba1adb69b888759fe8cfe29..b44b744ed492bdae3e3b7fd00201e1d540e8d670 100644

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
diff --git a/PawnStructure b/PawnStructure
index e6d8d4f7d1fb24de9ba1adb69b888759fe8cfe29..b44b744ed492bdae3e3b7fd00201e1d540e8d670 100644
--- a/PawnStructure
+++ b/PawnStructure
@@ -585,83 +585,92 @@ def apply_suppression_rules(S):
     # 6) Hedgehog > Centro 3–3 vs 4–2 (si ambos saltan; Hedgehog es el “nombre canónico”)
     if _has_label(S, "Hedgehog/Erizo"):
         S = {s for s in S if "Centro 3–3 vs 4–2" not in s}
 
     # 7) Stonewall específico (blancas/negras) > Centro clásico genérico del mismo lado
     if _has_label(S, "Stonewall blancas"):
         S = {s for s in S if "Centro clásico blancas (d4+e4)" not in s}
     if _has_label(S, "Stonewall negras"):
         S = {s for s in S if "Centro clásico negras (d5+e5)" not in s}
 
     return S
 
 def _title_for_game(game):
     title = (game.headers.get("Event", "") or "").strip()
     if title:
         return title
     w = (game.headers.get("White", "") or "").strip()
     b = (game.headers.get("Black", "") or "").strip()
     if w or b:
         ev = (game.headers.get("Event", "") or "").strip()
         ev_part = f" ({ev})" if ev else ""
         return f"{w} vs {b}{ev_part}"
     return "Sin título"
 
 
def _format_detection(game_idx, title, structure, fullmove, moved_side, san):
    """Devuelve la línea de resultado con el formato requerido."""
    return (
        f"Partida #{game_idx} | {title} - {structure} - "
        f"Detectada en jugada {fullmove} tras {moved_side} jugar {san}"
    )


 
 # ---------- Análisis principal (imprime y opcional CSV) ----------
 def analyze_pgn(pgn_path: str, csv_out: str = None):
     results = []
     game_idx = 0
 
     with open(pgn_path, encoding="utf-8", errors="ignore") as f:
         while True:
             game = chess.pgn.read_game(f)
             if game is None:
                 break
             game_idx += 1
 
             title = _title_for_game(game)
             board = game.board()
             node = game
             last_seen = set()
 
             while node.variations:
                 move = node.variation(0).move
                 san = board.san(move)
                 board.push(move)
 
                 cur_structs = compute_structures(board)
                 new_structs = cur_structs - last_seen
 
                 if new_structs:
                     fullmove = board.fullmove_number
                     moved_side = "negras" if board.turn == chess.WHITE else "blancas"
                     for s in sorted(new_structs):
                        # Línea única con el formato solicitado
                        linea = _format_detection(
                            game_idx, title, s, fullmove, moved_side, san
                        )
                         print(linea)
 
                         results.append({
                             "game_number": game_idx,
                             "white": game.headers.get("White", ""),
                             "black": game.headers.get("Black", ""),
                             "event": game.headers.get("Event", ""),
                             "structure": s,
                             "move_number": fullmove,
                             "after_move_san": san,
                             "moved_side": moved_side
                         })
 
                 last_seen = cur_structs
                 node = node.variation(0)
 
     if csv_out and results:
         fieldnames = ["game_number","white","black","event","structure","move_number","after_move_san","moved_side"]
         with open(csv_out, "w", newline="", encoding="utf-8") as cf:
             writer = csv.DictWriter(cf, fieldnames=fieldnames)
             writer.writeheader()
             writer.writerows(results)
         print("CSV guardado en:", os.path.abspath(csv_out))
 
 

