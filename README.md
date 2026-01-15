# OCR Engine (PaddleOCR)

Offline OCR Engine built using **PaddleOCR** and **Streamlit**.

## Features
- Image upload & preview
- Offline OCR (no API / no billing)
- Clean JSON & text output
- Responsive UI
- Client-demo ready

## Tech Stack
- Python 3.9
- PaddleOCR
- OpenCV
- Streamlit

## Setup

```bash
# Create virtual environment
py -3.9 -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run app
python -m streamlit run app.py
