import os
import csv
import io
import json
from urllib.parse import quote

from flask import Flask, request, jsonify, Response, render_template
from scraper import scrape_noon

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query_raw = request.args.get('q', '').strip()
    pages = min(int(request.args.get('pages', 2)), 8)
    country = request.args.get('country', 'saudi').strip()

    if not query_raw:
        return jsonify({'error': 'No query provided'}), 400

    safe_query = quote(query_raw)
    products = scrape_noon(safe_query, pages, country)

    return jsonify({'products': products, 'count': len(products), 'query': query_raw})

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