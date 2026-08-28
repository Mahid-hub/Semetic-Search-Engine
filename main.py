from src.qdrant_db import index_documents
from src.keyword_search import keyword_search
from src.dense_search import dense_search
from src.hybrid_search import hybrid_search
from src.evaluate import evaluate


def print_results(title, results):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    if not results:
        print("No results found.")
        return

    for i, result in enumerate(results, start=1):
        print(f"\nResult #{i}")
        print(f"Chunk ID    : {result['chunk_id']}")
        print(f"Document ID : {result['document_id']}")
        print(f"Source      : {result['source']}")

        if "score" in result:
            print(f"Score       : {result['score']:.4f}")

        if "rrf_score" in result:
            print(f"RRF Score   : {result['rrf_score']:.4f}")

        print("\nText:")
        print(result["text"])


def search_menu():

    while True:
        print("\n")
        print("=" * 70)
        print("SEARCH MENU")
        print("=" * 70)

        print("1. BM25 Keyword Search")
        print("2. Dense Semantic Search")
        print("3. Hybrid Search")
        print("4. Compare All Search Methods")
        print("5. Back to Main Menu")

        choice = input("\nChoose an option: ").strip()

        if choice == "5":
            break

        if choice not in ["1", "2", "3", "4"]:
            print("Invalid option.")
            continue

        query = input("\nEnter your search query: ").strip()

        if not query:
            print("Query cannot be empty.")
            continue

        limit_input = input("Number of results [default = 5]: ").strip()

        if limit_input:
            try:
                limit = int(limit_input)

                if limit <= 0:
                    print("Limit must be greater than 0.")
                    continue

            except ValueError:
                print("Invalid number. Using 5.")
                limit = 5

        else:
            limit = 5

        print("\nSearching...")

        try:
            # BM25
            if choice == "1":
                results = keyword_search(query, limit)
                print_results("BM25 KEYWORD SEARCH", results)

            # Dense
            elif choice == "2":
                results = dense_search(query, limit)
                print_results("DENSE SEMANTIC SEARCH", results)

            # Hybrid
            elif choice == "3":
                results = hybrid_search(query, limit)
                print_results("HYBRID SEARCH", results)

            # Compare all
            elif choice == "4":
                bm25_results = keyword_search(query, limit)
                dense_results = dense_search(query, limit)
                hybrid_results = hybrid_search(query, limit)
                
                print_results("BM25 KEYWORD SEARCH", bm25_results)
                print_results("DENSE SEMANTIC SEARCH", dense_results)
                print_results("HYBRID SEARCH", hybrid_results)

        except Exception as error:
            print("\nSearch error:")
            print(error)

def main():

    while True:
        print("\n")
        print("=" * 70)
        print("              SEMANTIC SEARCH ENGINE")
        print("=" * 70)

        print("\n1. Index Documents")
        print("2. Search")
        print("3. Evaluate Search Engine")
        print("4. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            print("\nStarting document indexing...")
            try:
                index_documents()

            except Exception as error:
                print("\nIndexing error:")
                print(error)

        elif choice == "2":
            search_menu()

        elif choice == "3":
            print("\nStarting search evaluation...")
            try:
                evaluate()

            except Exception as error:
                print("\nEvaluation error:")
                print(error)

        elif choice == "4":
            print("\nThank you for using Semantic Search Engine!")
            break

        else:
            print("\nInvalid option. Please choose 1-4.")

if __name__ == "__main__":
    main()
