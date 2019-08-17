from unittest import TestCase, mock, main as unittest_main
from app import app
from bson.objectid import ObjectId

sample_review_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_review = {
  'title': 'Super Sweet Review',
  'movieTitle': 'La La Land',
  'description': 'A great review of a lovely movie.'
}

class ReviewsTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True


    def test_home(self):
      """Test homepage page."""

      result = self.client.get("/")
      self.assertEqual(result.status, '200 OK')
      self.assertIn(b'Reviews', result.data)
    
    def test_new(self):
      result = self.client.get('/reviews/new')
      self.assertEqual(result.status, '200 OK')
      self.assertIn(b'New Review', result.data)

    @mock.patch("pymongo.collection.Collection.find_one")
    def test_show_review(self, mock_find):
        mock_find.return_value = sample_review

        result = self.client.get(f'/reviews/{sample_review_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'La La Land', result.data)

    @mock.patch("pymongo.collection.Collection.find_one")
    def test_edit_review(self, mock_find):
        """Test editing a single review."""
        mock_find.return_value = sample_review

        result = self.client.get(f'/reviews/{sample_review_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'La La Land', result.data)

    @mock.patch("pymongo.collection.Collection.insert_one")
    def test_submit_review(self, mock_insert):
        result = self.client.post('/reviews', data=sample_review)
        # After submitting, should redirect to that review's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_review)

    @mock.patch("pymongo.collection.Collection.update_one")
    def test_update_review(self, mock_update):
        form_data = {'_method': 'PUT', **sample_review}
        result = self.client.post(f'/reviews/{sample_review_id}', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_review_id}, {'$set': sample_review})

    @mock.patch("pymongo.collection.Collection.delete_one")
    def test_delete_review(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/reviews/{sample_review_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_review_id})


if __name__ == '__main__':
    unittest_main()