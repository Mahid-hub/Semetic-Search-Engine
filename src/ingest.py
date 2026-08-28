from pathlib import Path

def load_documents(path):
    data = Path(path)
    files = data.glob('*.txt')
    documents = []
    for file in files:
        f = {
            'id': file.stem,
            'source': file.name,
            'text': file.read_text()
        }
        documents.append(f)
        
    return documents

