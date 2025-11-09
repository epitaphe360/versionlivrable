import React from 'react';

/**
 * LoadingFallback - Composant de chargement pour React.lazy() et Suspense
 *
 * Affiche un spinner élégant pendant le chargement des composants lazy
 * Optimisé pour l'expérience utilisateur avec animations fluides
 */
const LoadingFallback = ({ message = 'Chargement...' }) => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="text-center">
        {/* Spinner animé */}
        <div className="relative inline-block">
          {/* Cercle extérieur */}
          <div className="w-16 h-16 border-4 border-indigo-200 rounded-full"></div>
          {/* Cercle animé */}
          <div className="absolute top-0 left-0 w-16 h-16 border-4 border-indigo-600 rounded-full border-t-transparent animate-spin"></div>
        </div>

        {/* Message de chargement */}
        <div className="mt-6">
          <p className="text-lg font-semibold text-gray-700 animate-pulse">
            {message}
          </p>
          <div className="mt-2 flex justify-center space-x-1">
            <span className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
            <span className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
            <span className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingFallback;
