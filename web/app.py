from flask import Flask, render_template, request, stream_with_context, Response
import json
import requests
import time
import pandas as pd

app = Flask(__name__)

class GoogleSearcher:
    def __init__(self, api_key):
        self.api_key = api_key

    def search_google(self, query, journal_info):
        search_query = f"{query} site:{journal_info['link']} filetype:pdf"
        params = {
            "engine": "google",
            "q": search_query,
            "hl": "id",
            "num": 20,
            "api_key": self.api_key
        }
        try:
            response = requests.get("https://serpapi.com/search", params=params)
            response.raise_for_status()
            results = response.json()
            articles = []
            if "organic_results" in results:
                for result in results["organic_results"]:
                    link = result.get('link', '')
                    if not link.lower().endswith('.pdf'):
                        continue
                    article = {
                        'judul': result.get('title', ''),
                        'link': link,
                        'snippet': result.get('snippet', ''),
                        'jurnal': journal_info['nama_jurnal'],
                        'peringkat_sinta': journal_info.get('sinta_rank', ''),
                        'website_jurnal': journal_info['link']
                    }
                    articles.append(article)
            return articles
        except Exception as e:
            print(f"Error saat mencari di {journal_info['nama_jurnal']}: {str(e)}")
            return []

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    @stream_with_context
    def generate():
        topic = request.form.get('topic')
        sinta_rank = request.form.get('sinta_rank')

        api_key = "d3d775e783819ad347d88e1f236ff3a8a6e883e171e836525df0bd7607bfe995"
        searcher = GoogleSearcher(api_key)

        with open('list_journal.json', 'r', encoding='utf-8') as f:
            journals_data = json.load(f)

        all_results = []
        for rank in journals_data:
            if rank.startswith("SINTA_"):
                if sinta_rank and rank != f"SINTA_{sinta_rank}":
                    continue
                for journal in journals_data[rank]:
                    journal['sinta_rank'] = rank
                    yield f"data: Mencari di {journal['nama_jurnal']}...\n\n"
                    results = searcher.search_google(topic, journal)
                    all_results.extend(results)
                    time.sleep(1)

        df = pd.DataFrame(all_results)
        if len(df) > 0:
            articles = df.to_dict(orient='records')
            yield f"data: {json.dumps(articles)}\n\n"
        else:
            yield "data: DONE\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
