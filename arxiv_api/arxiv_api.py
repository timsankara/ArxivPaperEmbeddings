import requests
import xml.etree.ElementTree as ET

class ArxivAPI:
    def __init__(self, category, max_results):
        """
        Initializes the ArxivAPI class with the specified category and max results.
        Constructs the query URL for the arXiv API to retrieve the latest papers.
        """
        self.base_url = 'https://export.arxiv.org/api/query'
        self.category = category
        self.max_results = max_results
        self.url = f"{self.base_url}?search_query=cat:{self.category}&max_results={self.max_results}&sortBy=submittedDate&sortOrder=descending"
        self.namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }

    def fetch_data(self):
        """
        Fetches data from the arXiv API using the constructed URL.
        Returns the raw XML data if the request is successful.
        Raises an exception if the request fails.
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Request failed with status code {response.status_code}")

    def parse_data(self, data):
        """
        Parses the XML data returned from the arXiv API.
        Extracts the title, summary, published date, link, and authors for each paper.
        Returns a list of dictionaries, each containing information about a paper.
        """
        root = ET.fromstring(data)
        papers = []
        for entry in root.findall('atom:entry', self.namespaces):
            title = entry.find('atom:title', self.namespaces).text
            summary = entry.find('atom:summary', self.namespaces).text
            published_date = entry.find('atom:published', self.namespaces).text
            link = entry.find('atom:link[@title="pdf"]', self.namespaces).get('href')

            authors = []
            for author in entry.findall('atom:author', self.namespaces):
                author_name = author.find('atom:name', self.namespaces).text
                authors.append(author_name)

            paper = {
                'title': title,
                'authors': ', '.join(authors),
                'summary': summary,
                'published_date': published_date,
                'link': link
            }
            papers.append(paper)
        return papers

    def display_papers(self, papers):
        """
        Displays the details of each paper in a readable format.
        """
        for paper in papers:
            print(f"Title: {paper['title']}")
            print(f"Authors: {paper['authors']}")
            print(f"Summary: {paper['summary']}")
            print(f"Published Date: {paper['published_date']}")
            print(f"Link: {paper['link']}")
            print('----------------------------------------')

    def run(self):
        """
        Orchestrates the process of fetching, parsing, and displaying papers.
        """
        data = self.fetch_data()
        papers = self.parse_data(data)
        self.display_papers(papers)


if __name__ == "__main__":
    # Prompt the user to enter the arXiv category and the number of items
    category = input("Enter the arXiv category (e.g., cs.AI): ")
    max_results = int(input("Enter the number of latest items you want to retrieve: "))

    # Create an instance of the ArxivAPI class with the specified parameters and run the process
    arxiv_api = ArxivAPI(category, max_results)
    arxiv_api.run()
