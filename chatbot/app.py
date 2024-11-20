from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, static_folder='static')

# Confluence API credentials
CONFLUENCE_BASE_URL = "https://your-confluence-instance.atlassian.net/wiki/rest/api/content/"
CONFLUENCE_API_TOKEN = "your_api_token"
CONFLUENCE_USER_EMAIL = "your_email@example.com"


def query_confluence(query):
    headers = {
        "Authorization": f"Basic {CONFLUENCE_USER_EMAIL}:{CONFLUENCE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    search_url = f"{CONFLUENCE_BASE_URL}search"
    params = {"cql": f"text ~ \"{query}\""}
    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            # Return the title and a link to the first result
            first_result = results[0]
            return f"{first_result['title']}: https://your-confluence-instance.atlassian.net/wiki{first_result['_links']['webui']}"
        else:
            return "No results found for your query."
    else:
        return "Error querying Confluence."


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('query')
    if not user_query:
        return jsonify({"status": "error", "message": "Query cannot be empty."})

    answer = query_confluence(user_query)
    return jsonify({"status": "success", "answer": answer})


if __name__ == '__main__':
    app.run(debug=True)
