from flask import Flask, Response, request, jsonify, url_for, redirect

from elasticsearch import Elasticsearch
from mongoengine import connect

from models import Todo

connect('test')

app = Flask(__name__)
app.es = Elasticsearch()


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/todo', methods=['POST'])
def create():
    title = request.form.get('title', '')
    description = request.form.get('description', '')

    Todo(title=title, description=description).save()

    return redirect(url_for('index'))


@app.route('/mongo')
def mongo():
    query = request.args.get('q', '')

    results = Todo.objects.search_text(query).order_by('$text_score').to_json()

    return Response(results, mimetype='application/json')


@app.route('/es')
def es():
    query = request.args.get('q', '')

    results = Todo.search(query)

    return jsonify(results)


if __name__ == '__main__':
    app.run()
