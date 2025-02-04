# cshogi/kifu_parser.py

import re
import cshogi
from typing import Optional

class KifuParser:
    MOVE_RE = re.compile(r'\A *[0-9]+\s+(中断|投了|持将棋|千日手|詰み|切れ負け|反則勝ち|反則負け|(([１２３４５６７８９])([零一二三四五六七八九])|同　)([歩香桂銀金角飛玉と杏圭全馬龍])(打|(成?)\(([0-9])([0-9])\)))\s*(\( *([:0-9]+)/([:0-9]+)\))?.*\Z')

    def __init__(self, kifu_str: str):
        self.kifu_str = kifu_str
        self.moves = []
        self.times = []
        self.parse_kifu()

    def parse_kifu(self):
        kif_str = self.kifu_str.replace('\r\n', '\n').replace('\r', '\n')
        lines = kif_str.split('\n')
        for line in lines:
            if len(line) == 0:
                continue
            move, time, endmove = self.parse_move_str(line)
            if move is not None:
                self.moves.append(move)
            if time is not None:
                self.times.append(time)

    def parse_move_str(self, line):
        m = self.MOVE_RE.match(line)
        if m:
            return m.group(0), None, None
        return None, None, None

    def display_kifu(self):
        for move, time in zip(self.moves, self.times):
            print(f"手数: {self.moves.index(move) + 1}, 指し手: {self.move_to_kif(move)}, 消費時間: {time}秒")

    def move_to_kif(self, move):
        to_sq = cshogi.move_to(move)
        move_to = cshogi.KIFU_TO_SQUARE_NAMES[to_sq]
        if self.moves.index(move) > 0:
            prev_move = self.moves[self.moves.index(move) - 1]
            if cshogi.move_to(prev_move) == to_sq:
                move_to = "同　"
        if not cshogi.move_is_drop(move):
            from_sq = cshogi.move_from(move)
            move_piece = cshogi.PIECE_JAPANESE_SYMBOLS[cshogi.move_from_piece_type(move)]
            if cshogi.move_is_promotion(move):
                return '{}{}成({})'.format(move_to, move_piece, cshogi.KIFU_FROM_SQUARE_NAMES[from_sq])
            else:
                return '{}{}({})'.format(move_to, move_piece, cshogi.KIFU_FROM_SQUARE_NAMES[from_sq])
        else:
            move_piece = cshogi.HAND_PIECE_JAPANESE_SYMBOLS[cshogi.move_drop_hand_piece(move)]
            return '{}{}打'.format(move_to, move_piece)
