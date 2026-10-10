"""
Books Manager - CRUD GUI (PyQt5) for books.csv

C - Create : add a new book
R - Read   : table view + search by title
U - Update : select a row, edit the fields, click Update
D - Delete : select a row, click Delete

Every change is saved to books.csv immediately, so when you close and
reopen the app everything is still there.

Run:  python books_crud.py   (keep books.csv in the same folder)
"""
import csv
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QPushButton,
    QMessageBox, QHeaderView, QAbstractItemView, QGroupBox, QLabel,
)

CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books.csv")
FIELDS = ["Title", "Price", "Rating"]
RATINGS = ["One", "Two", "Three", "Four", "Five"]


# ---------------------------------------------------------------- file layer
def load_books():
    """Read books.csv into a list of dicts. Returns [] if the file is missing."""
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
        return [
            {field: row.get(field, "") for field in FIELDS}
            for row in csv.DictReader(f)
        ]


def save_books(books):
    """Write the whole list back to books.csv."""
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(books)


def clean_price(text):
    """'51.77', '£51.77' or ' 51.77 ' -> '£51.77'. Raises ValueError if invalid."""
    value = float(text.replace("£", "").replace("Â", "").strip())
    if value < 0:
        raise ValueError("negative price")
    return f"£{value:.2f}"


# -------------------------------------------------------------------- the UI
class BooksWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Books Manager")
        self.resize(900, 650)
        self.books = load_books()
        self.build_ui()
        self.refresh_table()

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # search bar
        search_row = QHBoxLayout()
        search_row.addWidget(QLabel("Search title:"))
        self.search = QLineEdit()
        self.search.setPlaceholderText("Type to filter books...")
        self.search.textChanged.connect(self.refresh_table)
        search_row.addWidget(self.search)
        layout.addLayout(search_row)

        # table
        self.table = QTableWidget(0, len(FIELDS))
        self.table.setHorizontalHeaderLabels(FIELDS)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.itemSelectionChanged.connect(self.fill_form_from_selection)
        layout.addWidget(self.table)

        # form
        box = QGroupBox("Book details")
        form = QFormLayout(box)
        self.title_input = QLineEdit()
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("e.g. 51.77")
        self.rating_input = QComboBox()
        self.rating_input.addItems(RATINGS)
        form.addRow("Title:", self.title_input)
        form.addRow("Price (£):", self.price_input)
        form.addRow("Rating:", self.rating_input)
        layout.addWidget(box)

        # buttons
        buttons = QHBoxLayout()
        for text, handler in [
            ("Add", self.add_book),
            ("Update", self.update_book),
            ("Delete", self.delete_book),
            ("Clear form", self.clear_form),
        ]:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            buttons.addWidget(btn)
        layout.addLayout(buttons)

        self.statusBar()

    # ------------------------------------------------------------- helpers
    def refresh_table(self):
        """Rebuild the table from self.books, applying the search filter."""
        text = self.search.text().strip().lower()
        rows = [(i, b) for i, b in enumerate(self.books) if text in b["Title"].lower()]

        self.table.blockSignals(True)
        self.table.setRowCount(len(rows))
        for r, (index, book) in enumerate(rows):
            for c, field in enumerate(FIELDS):
                item = QTableWidgetItem(book[field])
                # remember which book in self.books this row belongs to
                item.setData(Qt.UserRole, index)
                self.table.setItem(r, c, item)
        self.table.blockSignals(False)

        self.statusBar().showMessage(f"Showing {len(rows)} of {len(self.books)} books")

    def selected_index(self):
        """Index in self.books of the selected row, or None."""
        row = self.table.currentRow()
        if row < 0 or self.table.item(row, 0) is None:
            return None
        return self.table.item(row, 0).data(Qt.UserRole)

    def select_index(self, index):
        for r in range(self.table.rowCount()):
            if self.table.item(r, 0).data(Qt.UserRole) == index:
                self.table.selectRow(r)
                return

    def read_form(self):
        """Validate the form. Returns a book dict, or None (after showing a warning)."""
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Missing title", "Please enter a title.")
            return None
        try:
            price = clean_price(self.price_input.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid price",
                                "Price must be a number, e.g. 51.77")
            return None
        return {"Title": title, "Price": price, "Rating": self.rating_input.currentText()}

    def fill_form_from_selection(self):
        index = self.selected_index()
        if index is None:
            return
        book = self.books[index]
        self.title_input.setText(book["Title"])
        self.price_input.setText(book["Price"].replace("£", "").replace("Â", ""))
        pos = self.rating_input.findText(book["Rating"])
        self.rating_input.setCurrentIndex(max(pos, 0))

    def clear_form(self):
        self.title_input.clear()
        self.price_input.clear()
        self.rating_input.setCurrentIndex(0)
        self.table.clearSelection()

    # ---------------------------------------------------------------- CRUD
    def add_book(self):
        book = self.read_form()
        if book is None:
            return
        self.books.append(book)
        save_books(self.books)
        self.search.clear()          # make sure the new book is visible
        self.refresh_table()
        self.select_index(len(self.books) - 1)
        self.table.scrollToBottom()
        self.statusBar().showMessage("Book added and saved.", 4000)

    def update_book(self):
        index = self.selected_index()
        if index is None:
            QMessageBox.information(self, "Nothing selected",
                                    "Click a book in the table first.")
            return
        book = self.read_form()
        if book is None:
            return
        self.books[index] = book
        save_books(self.books)
        self.refresh_table()
        self.select_index(index)
        self.statusBar().showMessage("Book updated and saved.", 4000)

    def delete_book(self):
        index = self.selected_index()
        if index is None:
            QMessageBox.information(self, "Nothing selected",
                                    "Click a book in the table first.")
            return
        title = self.books[index]["Title"]
        answer = QMessageBox.question(self, "Delete book", f'Delete "{title}"?')
        if answer != QMessageBox.Yes:
            return
        del self.books[index]
        save_books(self.books)
        self.clear_form()
        self.refresh_table()
        self.statusBar().showMessage("Book deleted and saved.", 4000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BooksWindow()
    window.show()
    sys.exit(app.exec_())