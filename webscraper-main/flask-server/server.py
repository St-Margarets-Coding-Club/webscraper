from flask import Flask, Response, request
import os
from llm import ContentProcessor

app = Flask(__name__)


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname("./client/public/"))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route('/', methods=['GET'])
def metrics():  # pragma: no cover
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
    url = request.args.get('url', '')
    content = setup_content(url)
    processor = ContentProcessor()
    summary = processor.summarize_content(content)

    return {"data": summary}
    


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
    app.run(debug=True)