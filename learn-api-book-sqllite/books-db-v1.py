import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/about', methods=['GET'])
def about():
    return '''<h1>Satish Atakare</h1>'''

@app.route('/api/v2/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args
    print(request.args)

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')
    title = query_parameters.get('title')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if title:
        query += ' title=? AND'
        to_filter.append(title)
    if not (id or published or author or title):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

#---------------------------------------------------
@app.route('/api/v1/resources/books_like', methods=['GET'])
def api_filter_like():
    query_parameters = request.args
    print(request.args)

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')
    title = query_parameters.get('title')

    query = "SELECT * FROM books WHERE"
    to_filter = []

#cur.execute("select * from contacts where name like ?", ('%'+search+'%',))
#LIKE using from python is crazy

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += " published like ? AND"
        to_filter.append(published)
    if author:
        query += " author like ? AND"
        to_filter.append(author)
    if title:
        query += ' title LIKE ? AND'
        to_filter.append('%'+title+'%')
    if not (id or published or author or title):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    #print(to_filter)
    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)


###---------------------------------------------------------------------
app.run()
