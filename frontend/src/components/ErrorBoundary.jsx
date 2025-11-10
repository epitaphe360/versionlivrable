import React from 'react';

/**
 * ErrorBoundary - Composant pour gérer les erreurs React
 * Capture les erreurs JavaScript dans les composants enfants
 * Affiche un UI de secours au lieu d'un écran blanc
 *
 * P0 CRITIQUE: Évite les crashes silencieux de l'application
 */
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    };
  }

  static getDerivedStateFromError(error) {
    // Met à jour le state pour afficher l'UI de secours
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Log l'erreur vers un service de monitoring
    console.error('ErrorBoundary caught an error:', error, errorInfo);

    // Stocker les détails de l'erreur
    this.setState({
      error,
      errorInfo
    });

    // Si Sentry est disponible, envoyer l'erreur
    if (window.Sentry) {
      window.Sentry.captureException(error, {
        contexts: {
          react: {
            componentStack: errorInfo.componentStack
          }
        }
      });
    }
  }

  handleReload = () => {
    window.location.reload();
  };

  handleGoHome = () => {
    window.location.href = '/';
  };

  render() {
    if (this.state.hasError) {
      // UI de secours personnalisé
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
          <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-8">
            <div className="flex items-center justify-center w-16 h-16 mx-auto bg-red-100 rounded-full mb-4">
              <svg
                className="w-8 h-8 text-red-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
            </div>

            <h1 className="text-2xl font-bold text-gray-900 text-center mb-2">
              Une erreur est survenue
            </h1>

            <p className="text-gray-600 text-center mb-6">
              Nous sommes désolés, quelque chose s'est mal passé. Veuillez réessayer.
            </p>

            {process.env.NODE_ENV === 'development' && this.state.error && (
              <details className="mb-6 p-4 bg-gray-100 rounded-lg overflow-auto max-h-48">
                <summary className="cursor-pointer font-semibold text-gray-700 mb-2">
                  Détails techniques (développement uniquement)
                </summary>
                <div className="text-sm text-gray-600 font-mono">
                  <p className="font-bold text-red-600 mb-2">
                    {this.state.error.toString()}
                  </p>
                  {this.state.errorInfo && (
                    <pre className="whitespace-pre-wrap text-xs">
                      {this.state.errorInfo.componentStack}
                    </pre>
                  )}
                </div>
              </details>
            )}

            <div className="flex flex-col sm:flex-row gap-3">
              <button
                onClick={this.handleReload}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                aria-label="Recharger la page"
              >
                Recharger la page
              </button>

              <button
                onClick={this.handleGoHome}
                className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded-lg transition-colors"
                aria-label="Retour à l'accueil"
              >
                Retour à l'accueil
              </button>
            </div>

            <p className="mt-6 text-sm text-gray-500 text-center">
              Si le problème persiste, contactez{' '}
              <a
                href="mailto:support@shareyoursales.ma"
                className="text-blue-600 hover:underline"
              >
                le support
              </a>
            </p>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
