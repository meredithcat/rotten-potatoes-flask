from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.exceptions import NotFound
import os

app = Flask(__name__)

host = os.environ.get('MONGODB_URL', 'localhost:27017')
client = MongoClient(host=host)
db = client.rotten_potatoes
reviews = db.reviews

@app.route('/')
def reviews_index():
    """Show all reviews."""
    return render_template("reviews_index.html", reviews=reviews.find())

@app.route('/reviews/new')
def reviews_new():
    """Create a new review."""
    return render_template("reviews_new.html", review={}, title='New Review')

@app.route('/reviews', methods=['POST'])
def reviews_submit():
    """Submit a new review."""
    review = {
        'title': request.form.get('title'),
        'movieTitle': request.form.get('movieTitle'),
        'description': request.form.get('description')
    }
    review_id = reviews.insert_one(review).inserted_id
    return redirect(url_for('reviews_show', review_id=review_id))

@app.route('/reviews/<review_id>')
def reviews_show(review_id):
  review = reviews.find_one({'_id': ObjectId(review_id)})
  return render_template('reviews_show.html', review=review)


@app.route('/reviews/<review_id>', methods=['POST'])
def reviews_update(review_id):
  if request.form.get('_method') == 'PUT':
    updated_review = {
      'title': request.form.get('title'),
      'movieTitle': request.form.get('movieTitle'),
      'description': request.form.get('description')
    }
    reviews.update_one(
      {'_id': ObjectId(review_id)},
      {'$set': updated_review})
    return redirect(url_for('reviews_show', review_id=review_id))
  else:
    raise NotFound()
    
@app.route('/reviews/<review_id>/edit')
def reviews_edit(review_id):
    review = reviews.find_one({'_id': ObjectId(review_id)})
    return render_template('reviews_edit.html', review=review)

@app.route('/reviews/<review_id>/delete', methods=['POST'])
def reviews_delete(review_id):
  if request.form.get('_method') == 'DELETE':
    reviews.delete_one({'_id': ObjectId(review_id)})
    return redirect(url_for('reviews_index'))
  else:
    raise NotFound()

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')