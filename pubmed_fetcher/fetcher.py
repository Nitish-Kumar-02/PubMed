import requests
from typing import List, Dict, Any

PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def fetch_pubmed_papers(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """Fetch paper IDs from PubMed based on a query and retrieve details."""
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": max_results}
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    response.raise_for_status()
    data = response.json()
    paper_ids = data.get("esearchresult", {}).get("idlist", [])
    
    if not paper_ids:
        return []

    details_params = {"db": "pubmed", "id": ",".join(paper_ids), "retmode": "json"}
    details_response = requests.get(PUBMED_SUMMARY_URL, params=details_params)
    details_response.raise_for_status()
    details_data = details_response.json()
    
    return parse_paper_details(details_data)

def parse_paper_details(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract relevant details from PubMed API response."""
    papers = []
    for paper_id, details in data.get("result", {}).items():
        if paper_id == "uids":
            continue

        title = details.get("title", "N/A")
        pub_date = details.get("pubdate", "N/A")
        authors = details.get("authors", [])
        non_academic_authors, company_affiliations = extract_non_academic_authors(authors)

        papers.append({
            "PubmedID": paper_id,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": ", ".join(non_academic_authors) if non_academic_authors else "N/A",
            "Company Affiliation(s)": ", ".join(company_affiliations) if company_affiliations else "N/A",
            "Corresponding Author Email": "N/A"
        })
    return papers

def extract_non_academic_authors(authors: List[Dict[str, Any]]) -> (List[str], List[str]):
    """Identify non-academic authors and their company affiliations."""
    non_academic_authors = []
    company_affiliations = []

    for author in authors:
        affiliation = author.get("affiliation", "").lower()
        if affiliation and ("inc" in affiliation or "pharma" in affiliation or "biotech" in affiliation):
            non_academic_authors.append(author.get("name", "Unknown"))
            company_affiliations.append(affiliation)

    return non_academic_authors, company_affiliations
