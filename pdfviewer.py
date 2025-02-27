import sys
import fitz  # PyMuPDF
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QFileDialog,
    QScrollArea, QWidget, QVBoxLayout, QLabel
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QEvent, QRect, QTimer

BATCH_SIZE = 20  # Number of placeholder widgets to create per batch

class PDFPageWidget(QLabel):
    def __init__(self, page_number, parent=None):
        super().__init__(parent)
        self.page_number = page_number
        self.loaded = False
        self.current_zoom = None
        self.setAlignment(Qt.AlignCenter)
        self.setText(f"Page {page_number + 1}\n(Loading...)")

    def loadPage(self, pdf_document, zoom):
        """Render and display the page if not already loaded at this zoom level."""
        if self.loaded and self.current_zoom == zoom:
            return
        try:
            page = pdf_document.load_page(self.page_number)
            matrix = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=matrix)
            # Create a QImage; try RGBA and fall back to RGB if needed.
            image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGBA8888)
            if image.isNull():
                image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.setPixmap(pixmap)
            self.current_zoom = zoom
            self.loaded = True
        except Exception as e:
            self.setText(f"Error loading page {self.page_number + 1}")

class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minimal PDF Viewer")
        self.resize(900, 700)
        self.pdf_document = None
        self.zoom = 1.0
        self.page_widgets = []  # List to hold PDFPageWidget instances
        self.currentPlaceholderIndex = 0  # For batch creation
        self.initUI()

    def initUI(self):
        # Create a scrollable area with a vertical layout for pages.
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.setCentralWidget(self.scrollArea)
        # Connect scrollbar changes to check which pages are visible.
        self.scrollArea.verticalScrollBar().valueChanged.connect(self.checkVisiblePages)
        # Install an event filter to capture Ctrl+Scroll events for zooming.
        self.scrollArea.viewport().installEventFilter(self)

        # Container widget to hold the pages.
        self.pagesWidget = QWidget()
        self.vbox = QVBoxLayout(self.pagesWidget)
        self.pagesWidget.setLayout(self.vbox)
        self.scrollArea.setWidget(self.pagesWidget)

        self.createToolBar()

    def createToolBar(self):
        # Minimal toolbar with essential actions.
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.openFile)
        toolbar.addAction(open_action)

        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.triggered.connect(self.zoomIn)
        toolbar.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.triggered.connect(self.zoomOut)
        toolbar.addAction(zoom_out_action)

    def openFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if file_path:
            try:
                self.pdf_document = fitz.open(file_path)
            except Exception as e:
                self.setWindowTitle("Failed to open PDF")
                return
            self.zoom = 1.0
            self.renderAllPages()
            self.setWindowTitle(f"Minimal PDF Viewer - {file_path}")

    def renderAllPages(self):
        """Clear existing pages and create placeholder widgets in batches."""
        # Safely clear existing widgets from the layout.
        while self.vbox.count():
            item = self.vbox.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.page_widgets = []
        self.currentPlaceholderIndex = 0

        if not self.pdf_document:
            return

        # Begin batch creation of placeholder widgets.
        self._createPlaceholdersBatch()

    def _createPlaceholdersBatch(self):
        total_pages = self.pdf_document.page_count
        end_index = min(self.currentPlaceholderIndex + BATCH_SIZE, total_pages)
        for page_num in range(self.currentPlaceholderIndex, end_index):
            widget = PDFPageWidget(page_num)
            self.vbox.addWidget(widget)
            self.page_widgets.append(widget)
        self.currentPlaceholderIndex = end_index

        # If there are more pages to create, schedule the next batch.
        if self.currentPlaceholderIndex < total_pages:
            QTimer.singleShot(0, self._createPlaceholdersBatch)
        else:
            # Once all pages are created, add a stretch and check visible pages.
            self.vbox.addStretch()
            self.checkVisiblePages()

    def checkVisiblePages(self):
        """Check which page widgets are visible and trigger their rendering."""
        if not self.pdf_document:
            return

        # Determine the visible region in the coordinate space of pagesWidget.
        scroll_value = self.scrollArea.verticalScrollBar().value()
        viewport_width = self.scrollArea.viewport().width()
        viewport_height = self.scrollArea.viewport().height()
        visible_rect = QRect(0, scroll_value, viewport_width, viewport_height)

        # Load each page that intersects with the visible area.
        for widget in self.page_widgets:
            if widget.geometry().intersects(visible_rect):
                widget.loadPage(self.pdf_document, self.zoom)

    def zoomIn(self):
        if self.pdf_document:
            self.zoom += 0.1
            # Mark all pages as not loaded so they refresh with the new zoom.
            for widget in self.page_widgets:
                widget.loaded = False
            self.checkVisiblePages()

    def zoomOut(self):
        if self.pdf_document and self.zoom > 0.2:
            self.zoom -= 0.1
            for widget in self.page_widgets:
                widget.loaded = False
            self.checkVisiblePages()

    def eventFilter(self, source, event):
        # Handle Ctrl+Scroll for zooming.
        if event.type() == QEvent.Wheel and (event.modifiers() & Qt.ControlModifier):
            if event.angleDelta().y() > 0:
                self.zoomIn()
            else:
                self.zoomOut()
            return True  # Mark event as handled.
        return super().eventFilter(source, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec_())
