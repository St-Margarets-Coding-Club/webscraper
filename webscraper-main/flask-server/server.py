from flask import Flask, Response, request
import os
from llm import ContentProcessor

app = Flask(__name__)

# Single processor instance to preserve conversation history between requests
processor = ContentProcessor()
# Keep the last fetched context in memory so follow-up questions can be asked
last_content = None


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "client", "public"))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)

        return open(src, mode="rb").read()
    except IOError as exc:
        return str(exc)


@app.route('/', methods=['GET'])
def metrics():
    content = get_file('index.html')
    return Response(content, mimetype="text/html")




def setup_content(url):
    """Fetch and validate scraped content via webscraper.get_content()."""
    try:
        import webscraper
        content = webscraper.get_content(url)
        if not content or len(content.strip()) < 10:
            print("Invalid content returned by webscraper.get_content()")
            return None
        return content
    except Exception as e:
        print(f"webscraper.get_content() failed: {e}")
        return None
    

@app.route('/scrap', methods=['GET'])
def scrap():
    # The frontend sends everything to /scrap?url=...; to support chat flow
    # we accept either a real URL (starts with http:// or https://) or
    # a follow-up question. If the input is a URL we scrape and summarize;
    # otherwise we treat it as a question and answer using last_content.
    raw = request.args.get('url', '')
    if not raw:
        return {"error": "No URL/question provided"}, 400

    # simple URL detection
    import re
    is_url = re.match(r"^https?://", raw.strip(), re.I) is not None

    if is_url:
        content = setup_content(raw)
        if not content:
            return {"error": "Failed to fetch or parse content from the URL"}, 400

        # persist the last fetched content for follow-up questions
        global last_content
        last_content = content

        # use the shared processor to keep a running conversation history
        summary = processor.summarize_content(content)

        return {"data": summary, "context": content}
    else:
        # treat raw as a follow-up question
        question = raw.strip()
        if not last_content:
            return {"error": "No context available. Please send a URL first to scrape."}, 400
        try:
            answer = processor.answer_question(question, last_content)
            return {"data": answer}
        except Exception as e:
            return {"error": f"Failed to answer question: {e}"}, 500


@app.route('/ask', methods=['GET', 'POST'])
def ask():
    """Answer a follow-up question using the last fetched context.
    Accepts `question` as query param (GET) or JSON body (POST).
    If no last context is available, returns an error.
    """
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        question = data.get('question', '')
    else:
        question = request.args.get('question', '')

    if not question:
        return {"error": "No question provided"}, 400

    if not last_content:
        return {"error": "No context available. Please scrape a URL first."}, 400

    try:
        answer = processor.answer_question(question, last_content)
        return {"data": answer}
    except Exception as e:
        return {"error": f"Failed to answer question: {e}"}, 500
    


@app.route('/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
        ".png": "image/png"
    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(path)
    return Response(content, mimetype=mimetype)


if __name__=="__main__":
    app.run(debug=False)
