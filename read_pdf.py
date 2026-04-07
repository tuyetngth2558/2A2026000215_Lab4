import sys
import subprocess

try:
    import PyPDF2
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
    import PyPDF2

try:
    reader = PyPDF2.PdfReader(r'Lab 4.pdf')
    text = ''.join(page.extract_text() + '\n' for page in reader.pages)
    with open('lab4_text.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS")
except Exception as e:
    print("ERROR:", e)
