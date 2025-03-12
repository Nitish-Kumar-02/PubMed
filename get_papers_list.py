import argparse
from pubmed_fetcher.fetcher import fetch_pubmed_papers
from pubmed_fetcher.utils import save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Filename to save the output CSV")
    args = parser.parse_args()
    
    papers = fetch_pubmed_papers(args.query)
    if args.file:
        save_to_csv(papers, args.file)
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()
