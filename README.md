# Minimal PDF Viewer

<div align="center">

</div>

## 📖 Overview

Minimal PDF Viewer is a lightweight, efficient PDF viewing application built with Python, PyQt5, and PyMuPDF. It focuses on simplicity while providing essential functionality for comfortable document reading.

## ✨ Features

- **Fast rendering** - Efficiently loads only visible pages
- **Smooth scrolling** through documents of any size
- **Batch loading** for improved performance with large documents
- **Zoom controls** via toolbar buttons or Ctrl+Scroll
- **Memory efficient** design for handling large PDFs

## 📋 Requirements

- Python 3.6+
- PyQt5
- PyMuPDF (fitz)

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/minimal-pdf-viewer.git
cd minimal-pdf-viewer
```

2. Install required dependencies:
```bash
pip install PyQt5 PyMuPDF
```

3. Run the application:
```bash
python pdfviewer.py
```

## 🎮 Usage

- **Open a PDF file**: Click "Open" in the toolbar and select your PDF file
- **Navigate**: Scroll up and down to move through the document
- **Zoom**: 
  - Click "Zoom In" or "Zoom Out" buttons on the toolbar
  - Hold Ctrl and scroll with mouse wheel for dynamic zooming

## 🔧 Code Structure

- `PDFViewer`: Main application window with toolbar and page container
- `PDFPageWidget`: Widget for displaying individual PDF pages
- Page loading is optimized with:
  - Lazy loading (only visible pages are rendered)
  - Batch creation of page widgets for smoother UI
  - Memory-efficient page handling

## 🔍 Implementation Details

- **Viewport optimization**: Only renders pages visible in the viewport
- **Zoom management**: Maintains proper zoom state across all pages
- **Error handling**: Gracefully handles loading errors for individual pages
- **Event filtering**: Custom event handler for Ctrl+Scroll zooming

## 🖼️ Screenshots

<div align="center">
  

![Screenshot 2025-02-27 163242](https://github.com/user-attachments/assets/754bead5-7bd8-4ad6-a12f-368399ff5659)

</div>

## 🛠️ Future Improvements

- [ ] Dark mode support
- [ ] Search functionality
- [ ] Bookmarks and annotations
- [ ] Tabbed interface for multiple documents
- [ ] Print support
- [ ] Document outline/table of contents navigation


Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

