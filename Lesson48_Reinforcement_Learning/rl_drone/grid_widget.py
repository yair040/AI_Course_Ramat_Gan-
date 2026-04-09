# rl_drone/grid_widget.py
# Author: Yair Levi
# Canvas grid: cells, drone image, arrows, heatmap, structures

import tkinter as tk
from tkinter import PhotoImage
import numpy as np
import os
from PIL import Image, ImageTk

from .config import (
    GRID_ROWS, GRID_COLS, CELL_SIZE, START_CELL, TARGET_CELL,
    STRUCT_NONE, STRUCT_BUILDING, STRUCT_TRAP, STRUCT_WIND,
    DRONE_IMG_ORIG, DRONE_IMG_SMALL, DRONE_IMG_SIZE,
    ACTIONS, ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT,
    PATH_HIGHLIGHT_COLOR,
)
from .logger_setup import setup_logger

log = setup_logger("grid_widget")

STRUCT_COLORS = {
    STRUCT_BUILDING: "#4a5568",   # steel grey
    STRUCT_TRAP:     "#8e44ad",   # purple
    STRUCT_WIND:     "#e67e22",   # dark orange — matches legend, distinct from amber arrows
}
ARROW_CHARS = {ACTION_UP: "↑", ACTION_DOWN: "↓", ACTION_LEFT: "←", ACTION_RIGHT: "→"}


def _prepare_drone_image():
    # Always regenerate so a new CELL_SIZE is picked up
    img = Image.open(DRONE_IMG_ORIG).convert("RGBA")
    img = img.resize((DRONE_IMG_SIZE, DRONE_IMG_SIZE), Image.LANCZOS)
    img.save(DRONE_IMG_SMALL)
    log.info("Drone image prepared at %dpx → %s", DRONE_IMG_SIZE, DRONE_IMG_SMALL)
    return DRONE_IMG_SMALL


class GridWidget(tk.Canvas):
    def __init__(self, parent, on_cell_click, **kwargs):
        w = GRID_COLS * CELL_SIZE
        h = GRID_ROWS * CELL_SIZE
        super().__init__(parent, width=w, height=h, bg="#0d1117", highlightthickness=0, **kwargs)
        self.on_cell_click = on_cell_click
        self.show_heatmap = False
        self.show_arrows = True
        self.show_qv = False
        self._drone_img = None
        self._drone_ref = None
        self._load_drone()
        self.bind("<Button-1>", self._handle_click)
        self._grid_data = np.zeros((GRID_ROWS, GRID_COLS), dtype=int)
        self._Q = None
        self._V = None
        self._arrows = {}
        self._drone_pos = START_CELL
        self._best_path = set()    # set of (r,c) on the highlighted best path
        self._draw_grid()

    def _load_drone(self):
        path = _prepare_drone_image()
        pil = Image.open(path).convert("RGBA")
        self._drone_img = ImageTk.PhotoImage(pil)

    def _cell_xy(self, r, c):
        x1 = c * CELL_SIZE
        y1 = r * CELL_SIZE
        return x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE

    def _draw_grid(self):
        self.delete("all")
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                self._draw_cell(r, c)
        if self._drone_pos:
            self._draw_drone()

    def _cell_color(self, r, c):
        if not self.show_heatmap:
            if (r, c) == START_CELL:  return "#27ae60"
            if (r, c) == TARGET_CELL: return "#e74c3c"
            stype = self._grid_data[r, c]
            if stype != STRUCT_NONE:
                return STRUCT_COLORS[stype]
            # Best-path highlight (only for empty cells)
            if (r, c) in self._best_path:
                return PATH_HIGHLIGHT_COLOR
            return "#161b22"
        else:
            if self._V is not None:
                v = self._V[r, c]
                vmin, vmax = self._V.min(), self._V.max()
                t = (v - vmin) / (vmax - vmin) if vmax > vmin else 0.0
                r_ = int(20 + t * 200)
                g_ = int(20 + t * 50)
                b_ = int(80 + t * 120)
                return f"#{r_:02x}{g_:02x}{b_:02x}"
            return "#161b22"

    def _draw_cell(self, r, c):
        x1, y1, x2, y2 = self._cell_xy(r, c)
        color = self._cell_color(r, c)
        self.create_rectangle(x1, y1, x2, y2, fill=color, outline="#30363d", width=1)
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        if self.show_qv and self._Q is not None:
            self._draw_qv_text(r, c, x1, y1, x2, y2)
        if self.show_arrows and (r, c) in self._arrows:
            a = self._arrows[(r, c)]
            # On best-path cells use bright yellow for contrast vs the navy background
            arrow_color = "#ffe066" if (r, c) in self._best_path else "#00d4ff"
            self.create_text(cx, cy, text=ARROW_CHARS[a], fill=arrow_color,
                             font=("Courier", 20, "bold"))

    def _draw_qv_text(self, r, c, x1, y1, x2, y2):
        q = self._Q[r, c]
        v = self._V[r, c] if self._V is not None else 0
        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
        font = ("Courier", 7)
        clr = "#aaaaaa"
        self.create_text(mid_x, y1 + 8,  text=f"{q[ACTION_UP]:.0f}",    fill=clr, font=font)
        self.create_text(mid_x, y2 - 8,  text=f"{q[ACTION_DOWN]:.0f}",  fill=clr, font=font)
        self.create_text(x1 + 8, mid_y,  text=f"{q[ACTION_LEFT]:.0f}",  fill=clr, font=font)
        self.create_text(x2 - 8, mid_y,  text=f"{q[ACTION_RIGHT]:.0f}", fill=clr, font=font)
        self.create_text(mid_x, mid_y,   text=f"V:{v:.0f}",             fill="#ffcc00", font=font)

    def _draw_drone(self):
        r, c = self._drone_pos
        x1, y1, x2, y2 = self._cell_xy(r, c)
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        self._drone_ref = self.create_image(cx, cy, image=self._drone_img)

    def _handle_click(self, event):
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE
        if 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS:
            self.on_cell_click(r, c)

    # Public update API
    def update_state(self, grid, Q, V, arrows, drone_pos, best_path=None):
        self._grid_data = grid
        self._Q = Q
        self._V = V
        self._arrows = arrows
        self._drone_pos = drone_pos
        if best_path is not None:
            self._best_path = set(best_path)
        self._draw_grid()

    def clear_best_path(self):
        self._best_path = set()
        self._draw_grid()
