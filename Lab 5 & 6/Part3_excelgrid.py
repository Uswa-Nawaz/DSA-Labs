#   1. Grid layout   : 10 x 10 editable text boxes, column headers A..J, row numbers 1..10
#   2. Navigation    : arrow keys move the active cell, which is highlighted
#   3. Data entry    : type in any cell; Enter or moving away saves the value
#   4. Optional      : selected-cell address label, "Clear All" and "Save" buttons
import sys
import csv
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLayout,
                             QLineEdit, QLabel, QPushButton, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
 
ROWS = 10
COLS = 10
 
 
def column_name(c):
    """0 -> 'A', 1 -> 'B', ... (enough for 26 columns)."""
    return chr(ord('A') + c)
 
 
def address(r, c):
    """(0, 0) -> 'A1', (1, 1) -> 'B2' ... column letter + row number."""
    return column_name(c) + str(r + 1)
 
 
class Cell(QLineEdit):
    """One spreadsheet cell: a small text box that knows its row/column."""
    moved = pyqtSignal(int, int, int, int)      # emitted as (row, col, d_row, d_col) when the user wants to move
    selected = pyqtSignal(int, int)             # emitted when this cell becomes the active one
 
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.setFixedSize(80, 28)
        # the :focus rule is what highlights the active cell
        self.setStyleSheet("""
            QLineEdit { border: 1px solid #c8c8c8; padding-left: 4px; background: white; }
            QLineEdit:focus { border: 2px solid #1f7a45; background: #e8f5ec; }
        """)
 
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Right:
            self.moved.emit(self.row, self.col, 0, 1)
        elif key == Qt.Key_Left:
            self.moved.emit(self.row, self.col, 0, -1)
        elif key == Qt.Key_Up:
            self.moved.emit(self.row, self.col, -1, 0)
        elif key == Qt.Key_Down:
            self.moved.emit(self.row, self.col, 1, 0)
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            super().keyPressEvent(event)         # lets QLineEdit finish editing (emits editingFinished)
            self.moved.emit(self.row, self.col, 1, 0)   # Enter saves and moves down, like Excel
        else:
            super().keyPressEvent(event)         # normal typing / backspace / etc.
 
    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.selected.emit(self.row, self.col)
        QTimer.singleShot(0, self.selectAll)     # selected text gets replaced when you start typing
 
 
class ExcelGrid(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel Grid View")
        self.data = [["" for _ in range(COLS)] for _ in range(ROWS)]   # the saved values (2D grid)
        self.cells = []                                                  # the 2D grid of Cell widgets
 
        # --- top bar: address label ---
        self.address_label = QLabel("Selected cell: A1")
        self.address_label.setStyleSheet("font-weight: bold; font-size: 14px;")
 
        # --- the grid itself ---
        grid = QGridLayout()
        grid.setSpacing(0)
        for c in range(COLS):                                            # column headers A, B, C...
            header = QLabel(column_name(c))
            header.setAlignment(Qt.AlignCenter)
            header.setFixedSize(80, 28)                                  # same size as a cell
            header.setStyleSheet("background: #e6e6e6; font-weight: bold; border: 1px solid #c8c8c8;")
            grid.addWidget(header, 0, c + 1)
        for r in range(ROWS):
            header = QLabel(str(r + 1))                                  # row numbers 1, 2, 3...
            header.setAlignment(Qt.AlignCenter)
            header.setFixedSize(34, 28)
            header.setStyleSheet("background: #e6e6e6; font-weight: bold; border: 1px solid #c8c8c8;")
            grid.addWidget(header, r + 1, 0)
 
            row_cells = []
            for c in range(COLS):
                cell = Cell(r, c)
                cell.moved.connect(self.move_to)
                cell.selected.connect(self.on_selected)
                cell.editingFinished.connect(lambda cell=cell: self.save_cell(cell))
                grid.addWidget(cell, r + 1, c + 1)
                row_cells.append(cell)
            self.cells.append(row_cells)
 
        # --- buttons ---
        clear_btn = QPushButton("Clear All")
        save_btn = QPushButton("Save")
        clear_btn.clicked.connect(self.clear_all)
        save_btn.clicked.connect(self.save_to_file)
        buttons = QHBoxLayout()
        buttons.addWidget(clear_btn)
        buttons.addWidget(save_btn)
        buttons.addStretch()
 
        grid.setSizeConstraint(QLayout.SetFixedSize)                     # grid never grows or spreads out
        grid_holder = QWidget()
        grid_holder.setLayout(grid)
 
        layout = QVBoxLayout(self)
        layout.addWidget(self.address_label)
        layout.addWidget(grid_holder, alignment=Qt.AlignLeft | Qt.AlignTop)
        layout.addLayout(buttons)
        layout.addStretch()                                              # extra window space stays empty at the bottom
 
        self.cells[0][0].setFocus()                                      # start on A1
 
    # ---------- behaviour ----------
    def move_to(self, row, col, d_row, d_col):
        """Move the active cell by (d_row, d_col); stay put at the edges of the grid."""
        new_r = row + d_row
        new_c = col + d_col
        if 0 <= new_r < ROWS and 0 <= new_c < COLS:
            self.cells[new_r][new_c].setFocus()
 
    def on_selected(self, row, col):
        self.address_label.setText("Selected cell: " + address(row, col))
 
    def save_cell(self, cell):
        """Called on Enter or when the cell loses focus: store its text in our 2D data grid."""
        self.data[cell.row][cell.col] = cell.text()
 
    def clear_all(self):
        for r in range(ROWS):
            for c in range(COLS):
                self.cells[r][c].clear()
                self.data[r][c] = ""
        self.cells[0][0].setFocus()
 
    def save_to_file(self):
        # make sure the cell being edited right now is included
        focused = QApplication.focusWidget()
        if isinstance(focused, Cell):
            self.save_cell(focused)
        path, _ = QFileDialog.getSaveFileName(self, "Save grid", "grid.csv", "CSV files (*.csv)")
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([""] + [column_name(c) for c in range(COLS)])      # header row
                for r in range(ROWS):
                    writer.writerow([r + 1] + self.data[r])
            QMessageBox.information(self, "Saved", "Grid saved to:\n" + path)
        except OSError as e:
            QMessageBox.warning(self, "Error", "Could not save file:\n" + str(e))
 
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExcelGrid()
    window.show()
    sys.exit(app.exec_())