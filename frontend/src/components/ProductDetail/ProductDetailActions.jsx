import React, { memo } from 'react';
import { Sparkles, Clock, X, Users, Phone, Mail } from 'lucide-react';

/**
 * ProductDetailActions - Purchase card with price, stock, affiliation
 * React.memo for performance optimization
 */
const ProductDetailActions = memo(({ product, user, onRequestAffiliation, hasDiscount }) => {
  if (!product) return null;

  return (
    <div className="lg:col-span-1">
      <div className="bg-white rounded-2xl shadow-2xl p-8 sticky top-6 hover-lift border-2 border-blue-100">
        {/* Price - Ultra-moderne */}
        <div className="mb-8">
          {hasDiscount ? (
            <>
              <div className="flex items-baseline space-x-3 mb-3">
                <span className="text-5xl font-black bg-gradient-to-r from-red-500 to-pink-600 bg-clip-text text-transparent">
                  {product.discounted_price?.toLocaleString()}
                </span>
                <span className="text-2xl font-bold text-gray-900">DH</span>
              </div>
              <div className="flex items-baseline space-x-2 mb-4">
                <span className="text-xl text-gray-400 line-through">
                  {product.original_price?.toLocaleString()} DH
                </span>
              </div>
              <div className="inline-block bg-gradient-to-r from-red-500 to-pink-500 text-white px-4 py-2 rounded-xl text-sm font-black shadow-lg animate-pulse mb-3">
                🔥 -{product.discount_percentage}% DE RÉDUCTION
              </div>
              <div className="text-base font-bold bg-gradient-to-r from-green-500 to-emerald-600 bg-clip-text text-transparent">
                💰 Économisez{' '}
                {(product.original_price - product.discounted_price).toLocaleString()} DH
              </div>
            </>
          ) : (
            <div className="flex items-baseline space-x-3">
              <span className="text-5xl font-black bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
                {product.discounted_price?.toLocaleString() ||
                  product.original_price?.toLocaleString()}
              </span>
              <span className="text-2xl font-bold text-gray-900">DH</span>
            </div>
          )}
        </div>

        {/* Expiry */}
        {product.expiry_date && (
          <div className="flex items-center gap-3 text-orange-700 mb-6 p-4 bg-gradient-to-r from-orange-50 to-red-50 rounded-xl border-2 border-orange-200">
            <div className="w-10 h-10 bg-orange-500 rounded-xl flex items-center justify-center">
              <Clock className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="text-xs font-semibold text-orange-600 uppercase">Expire le</div>
              <div className="text-sm font-bold">
                {new Date(product.expiry_date).toLocaleDateString('fr-FR')}
              </div>
            </div>
          </div>
        )}

        {/* Stock */}
        {product.stock_quantity !== null && (
          <div className="mb-6">
            {product.stock_quantity > 0 ? (
              <div className="flex items-center gap-2 bg-gradient-to-r from-green-50 to-emerald-50 px-4 py-3 rounded-xl border-2 border-green-200">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-green-700 font-bold text-sm">
                  ✓ En stock ({product.stock_quantity} disponibles)
                </span>
              </div>
            ) : (
              <div className="flex items-center gap-2 bg-gradient-to-r from-red-50 to-pink-50 px-4 py-3 rounded-xl border-2 border-red-200">
                <X className="w-5 h-5 text-red-500" />
                <span className="text-red-700 font-bold text-sm">Rupture de stock</span>
              </div>
            )}
          </div>
        )}

        {/* Sold Count */}
        {product.sold_count > 0 && (
          <div className="flex items-center gap-3 text-gray-700 mb-6 bg-gradient-to-r from-blue-50 to-cyan-50 px-4 py-3 rounded-xl">
            <div className="w-10 h-10 bg-blue-500 rounded-xl flex items-center justify-center">
              <Users className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="text-xs font-semibold text-blue-600 uppercase">Popularité</div>
              <div className="text-sm font-bold">{product.sold_count} personnes ont acheté</div>
            </div>
          </div>
        )}

        {/* Request Affiliation Button - Principal */}
        <button
          onClick={onRequestAffiliation}
          className="w-full bg-gradient-to-r from-green-500 via-emerald-500 to-teal-500 text-white py-5 rounded-xl font-black text-lg hover:from-green-600 hover:via-emerald-600 hover:to-teal-600 transition-all duration-300 flex items-center justify-center shadow-2xl mb-6 transform hover:scale-105 animate-gradient"
        >
          <Sparkles className="inline-block w-7 h-7 mr-2 animate-pulse" />
          {user ? 'Devenir Affilié' : 'Connexion Affilié'}
        </button>

        {/* Commission Info - Ultra-moderne */}
        <div className="p-6 bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 rounded-2xl border-2 border-green-200 shadow-inner mb-6">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm font-bold text-green-800 uppercase tracking-wide">
              💰 Commission
            </span>
            <span className="text-4xl font-black bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
              {product.commission_rate || 15}%
            </span>
          </div>
          <p className="text-xs text-green-700 font-semibold leading-relaxed">
            Gagnez des revenus passifs en partageant ce produit avec votre audience
          </p>
        </div>

        {/* Merchant Info - Ultra-moderne */}
        {product.merchant && (
          <div className="mt-6 pt-6 border-t border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-3">Vendu par</h3>
            <div className="space-y-2">
              <p className="font-medium text-gray-900">{product.merchant.name}</p>
              {product.merchant.phone && (
                <div className="flex items-center text-sm text-gray-600">
                  <Phone className="w-4 h-4 mr-2" />
                  {product.merchant.phone}
                </div>
              )}
              {product.merchant.email && (
                <div className="flex items-center text-sm text-gray-600">
                  <Mail className="w-4 h-4 mr-2" />
                  {product.merchant.email}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
});

ProductDetailActions.displayName = 'ProductDetailActions';

export default ProductDetailActions;
