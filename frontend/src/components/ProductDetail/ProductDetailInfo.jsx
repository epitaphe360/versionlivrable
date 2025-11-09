import React, { memo } from 'react';
import { Check, Award } from 'lucide-react';

/**
 * ProductDetailInfo - Highlights, Included items, FAQ, Conditions
 * React.memo for performance optimization
 */
const ProductDetailInfo = memo(({ product, highlights = [], faq = [] }) => {
  if (!product) return null;

  return (
    <div className="space-y-6">
      {/* Highlights - Ultra-moderne */}
      {highlights.length > 0 && (
        <div className="bg-white rounded-2xl shadow-xl p-8 hover-lift">
          <h2 className="text-3xl font-black bg-gradient-to-r from-green-500 to-emerald-600 bg-clip-text text-transparent mb-6 flex items-center gap-3">
            <div className="w-12 h-12 bg-gradient-to-br from-green-100 to-emerald-100 rounded-xl flex items-center justify-center">
              ✨
            </div>
            Points Forts
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {highlights.map((highlight, index) => (
              <div
                key={index}
                className="flex items-start gap-3 bg-gradient-to-r from-green-50 to-emerald-50 p-4 rounded-xl hover:shadow-lg transition-all duration-300"
              >
                <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <Check className="w-4 h-4 text-white" />
                </div>
                <span className="text-gray-800 font-medium leading-relaxed">{highlight}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* What's Included */}
      {product.included && product.included.length > 0 && (
        <div className="bg-white rounded-2xl shadow-xl p-8 hover-lift">
          <h2 className="text-3xl font-black bg-gradient-to-r from-purple-500 to-pink-600 bg-clip-text text-transparent mb-6 flex items-center gap-3">
            <div className="w-12 h-12 bg-gradient-to-br from-purple-100 to-pink-100 rounded-xl flex items-center justify-center">
              📦
            </div>
            Ce qui est inclus
          </h2>
          <ul className="space-y-3">
            {product.included.map((item, index) => (
              <li
                key={index}
                className="flex items-start gap-3 bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-xl hover:shadow-lg transition-all duration-300"
              >
                <Award className="w-6 h-6 text-purple-500 mt-0.5 flex-shrink-0" />
                <span className="text-gray-800 font-medium leading-relaxed">{item}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* How it Works */}
      {product.how_it_works && (
        <div className="bg-white rounded-xl shadow-sm p-6 hover-lift">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">🔄 Comment ça marche</h2>
          <div className="prose max-w-none">
            <p className="text-gray-700 whitespace-pre-line">{product.how_it_works}</p>
          </div>
        </div>
      )}

      {/* Conditions */}
      {product.conditions && (
        <div className="bg-white rounded-xl shadow-sm p-6 hover-lift">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">📋 Conditions</h2>
          <div className="prose max-w-none">
            <p className="text-gray-700 whitespace-pre-line">{product.conditions}</p>
          </div>
        </div>
      )}

      {/* FAQ */}
      {faq.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm p-6 hover-lift">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">❓ Questions Fréquentes</h2>
          <div className="space-y-4">
            {faq.map((item, index) => (
              <div key={index} className="border-b border-gray-200 pb-4 last:border-b-0">
                <h3 className="font-semibold text-gray-900 mb-2">{item.question}</h3>
                <p className="text-gray-700">{item.answer}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
});

ProductDetailInfo.displayName = 'ProductDetailInfo';

export default ProductDetailInfo;
