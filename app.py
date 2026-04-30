import os
import csv
import io
import json
from urllib.parse import quote

from flask import Flask, request, jsonify, Response, render_template, stream_with_context
from scraper import scrape_noon
from queue import Queue
from threading import Thread

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query_raw = request.args.get('q', '').strip()
    pages = max(1, min(int(request.args.get('pages', 2)), 7))
    country = request.args.get('country', 'saudi').strip()

    if not query_raw:
        return jsonify({'error': 'No query provided'}), 400

    safe_query = quote(query_raw)

    def generate():
        q = Queue()

        def progress_callback(payload):
            if isinstance(payload, dict):
                payload_json = payload
                if 'type' not in payload_json:
                    payload_json['type'] = 'progress'
                q.put(json.dumps(payload_json) + "\n")
            else:
                q.put(json.dumps({"type": "progress", "message": str(payload)}) + "\n")

        def worker():
            try:
                products = scrape_noon(safe_query, pages, country, progress_callback=progress_callback)
                q.put(json.dumps({"type": "complete", "products": products}) + "\n")
            except Exception as e:
                q.put(json.dumps({"type": "error", "message": str(e)}) + "\n")
            finally:
                q.put(None)

        thread = Thread(target=worker, daemon=True)
        thread.start()

        while True:
            item = q.get()
            if item is None:
                break
            yield item

        thread.join()

    return Response(stream_with_context(generate()), mimetype='application/x-ndjson')

@app.route('/export')
def export():
    data = request.args.get('data', '[]')
    try:
        products = json.loads(data)
    except Exception:
        return 'Bad data', 400

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=['name', 'price', 'link', 'express'])
    writer.writeheader()
    for product in products:
        writer.writerow({
            'name': product.get('name', ''),
            'price': product.get('price', ''),
            'link': product.get('link', ''),
            'express': product.get('express', False),
        })
    buf.seek(0)

    return Response(
        buf.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=noon_results.csv'}
    )

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', 'false').lower() in ('1', 'true', 'yes')
    )