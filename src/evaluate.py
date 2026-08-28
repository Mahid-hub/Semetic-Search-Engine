import json
from keyword_search import keyword_search
from dense_search import dense_search
from hybrid_search import hybrid_search

def load_queries():
    with open("queries/test_queries.json", "r", encoding="utf-8") as file:
        return json.load(file)

def recall_at_k(results, relevant_chunks, k):
    retrieved_ids = []
    for result in results[:k]:
        retrieved_ids.append(result["chunk_id"])

    retrieved_ids = set(retrieved_ids)
    relevant_chunks = set(relevant_chunks)
    found = retrieved_ids.intersection(relevant_chunks)

    if len(relevant_chunks) == 0:
        return 0.0

    return len(found) / len(relevant_chunks)


def reciprocal_rank(results, relevant_chunks):
    relevant_chunks = set(relevant_chunks)
    
    for rank, result in enumerate(results, start=1):
        chunk_id = result["chunk_id"]
        
        if chunk_id in relevant_chunks:
            return 1 / rank

    return 0.0

def evaluate_method(queries, search_function, k=5):
    recall_scores = []
    rr_scores = []

    for item in queries:
        query = item["query"]
        relevant_chunks = item["relevant_chunks"]
        
        results = search_function(query, k)
        recall = recall_at_k(results, relevant_chunks, k)
        rr = reciprocal_rank(results, relevant_chunks)
        
        recall_scores.append(recall)
        rr_scores.append(rr)

    average_recall = sum(recall_scores) / len(recall_scores)
    average_mrr = sum(rr_scores) / len(rr_scores)

    return average_recall, average_mrr


def evaluate():
    queries = load_queries()
    
    print("=" * 60)
    print("SEARCH EVALUATION")
    print("=" * 60)

    print(f"Number of queries: {len(queries)}")
    print("K: 5")

    print("Evaluating BM25...")
    bm25_recall, bm25_mrr = evaluate_method(queries, keyword_search, k=5)
    
    print("Evaluating Dense Search...")
    dense_recall, dense_mrr = evaluate_method(queries, dense_search, k=5)

    print("Evaluating Hybrid Search...")
    hybrid_recall, hybrid_mrr = evaluate_method(queries, hybrid_search, k=5)

    print()
    print("=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    print()

    print(f"{'Method':<15} {'Recall@5':<15} {'MRR':<15}")
    print("-" * 45)
    print(f"{'BM25':<15} {bm25_recall:<15.3f} {bm25_mrr:<15.3f}")
    print(f"{'Dense':<15} {dense_recall:<15.3f} {dense_mrr:<15.3f}")
    print(f"{'Hybrid':<15} {hybrid_recall:<15.3f} {hybrid_mrr:<15.3f}")
    print("=" * 60)

if __name__ == "__main__":
    evaluate()