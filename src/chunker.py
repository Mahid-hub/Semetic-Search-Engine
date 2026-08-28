

def chunk_text(c_size, c_overlap, text, doc):
    chunks = []

    start = 0
    chunk_number = 0
    
    while start < len(text):
        
        end = start + c_size
        chunk = text[start:end]
        start = start + (c_size - c_overlap)
        chunk_number += 1
        
        chunks.append({
                'chunk_id': f"{doc['id']}_{chunk_number:03d}",
                'document_id': doc['id'],
                'source': doc['source'],
                'text': chunk
            })

    return chunks

