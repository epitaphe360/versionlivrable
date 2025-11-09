import React, { memo } from 'react';
import { Star } from 'lucide-react';

/**
 * ProductDetailReviews - Reviews list and review form
 * React.memo for performance optimization
 */
const ProductDetailReviews = memo(({
  reviews = [],
  user,
  showReviewForm,
  reviewData,
  onToggleReviewForm,
  onUpdateReviewData,
  onSubmitReview
}) => {
  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900">⭐ Avis Clients</h2>
        {user && (
          <button
            onClick={onToggleReviewForm}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            {showReviewForm ? 'Annuler' : 'Laisser un avis'}
          </button>
        )}
      </div>

      {/* Review Form */}
      {showReviewForm && (
        <form onSubmit={onSubmitReview} className="mb-6 p-4 bg-gray-50 rounded-lg">
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Note
            </label>
            <div className="flex space-x-2">
              {[1, 2, 3, 4, 5].map((rating) => (
                <button
                  key={rating}
                  type="button"
                  onClick={() => onUpdateReviewData({ rating })}
                  className="focus:outline-none"
                  aria-label={`Rate ${rating} stars`}
                >
                  <Star
                    className={`w-8 h-8 transition-colors ${
                      rating <= reviewData.rating
                        ? 'text-yellow-400 fill-yellow-400'
                        : 'text-gray-300'
                    }`}
                  />
                </button>
              ))}
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Titre (optionnel)
            </label>
            <input
              type="text"
              value={reviewData.title}
              onChange={(e) => onUpdateReviewData({ title: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="Résumez votre expérience"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Commentaire
            </label>
            <textarea
              value={reviewData.comment}
              onChange={(e) => onUpdateReviewData({ comment: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              rows="4"
              placeholder="Partagez votre avis..."
              required
            />
          </div>

          <div className="flex space-x-2">
            <button
              type="submit"
              className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
            >
              Publier
            </button>
            <button
              type="button"
              onClick={onToggleReviewForm}
              className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
            >
              Annuler
            </button>
          </div>
        </form>
      )}

      {/* Reviews List */}
      {reviews.length === 0 ? (
        <p className="text-gray-600 text-center py-8">
          Soyez le premier à laisser un avis!
        </p>
      ) : (
        <div className="space-y-4">
          {reviews.map((review) => (
            <div key={review.id} className="border-b border-gray-200 pb-4 last:border-b-0">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <div className="flex items-center mb-1">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`w-4 h-4 ${
                          i < review.rating
                            ? 'text-yellow-400 fill-yellow-400'
                            : 'text-gray-300'
                        }`}
                      />
                    ))}
                  </div>
                  {review.title && (
                    <h4 className="font-semibold text-gray-900">{review.title}</h4>
                  )}
                  <p className="text-sm text-gray-500">
                    Par {review.user?.first_name || 'Anonyme'} le{' '}
                    {new Date(review.created_at).toLocaleDateString('fr-FR')}
                  </p>
                </div>
                {review.is_verified_purchase && (
                  <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                    ✓ Achat vérifié
                  </span>
                )}
              </div>
              <p className="text-gray-700">{review.comment}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
});

ProductDetailReviews.displayName = 'ProductDetailReviews';

export default ProductDetailReviews;
