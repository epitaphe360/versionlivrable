import React from 'react';
import { Helmet } from 'react-helmet-async';

/**
 * Composant SEOHead - Gère les meta tags et structured data
 * Optimisé pour les moteurs de recherche (SEO)
 */
const SEOHead = ({
  title = 'GetYourShare - Plateforme d\'affiliation B2B',
  description = 'Plateforme d\'affiliation B2B connectant entreprises, commerciaux et influenceurs',
  keywords = 'affiliation, B2B, marketing digital, commissions, tracking',
  image = 'https://getyourshare.com/og-image.jpg',
  type = 'website',
  url = 'https://getyourshare.com',
  structuredData = null,
  author = 'GetYourShare'
}) => {
  return (
    <Helmet>
      {/* Titre de la page */}
      <title>{title} | GetYourShare</title>

      {/* Meta tags essentiels */}
      <meta name="description" content={description} />
      <meta name="keywords" content={keywords} />
      <meta name="author" content={author} />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta charSet="utf-8" />

      {/* Open Graph (Facebook, LinkedIn) */}
      <meta property="og:type" content={type} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={image} />
      <meta property="og:url" content={url} />
      <meta property="og:site_name" content="GetYourShare" />

      {/* Twitter Card */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={image} />

      {/* Canonical URL */}
      <link rel="canonical" href={url} />

      {/* Robots meta */}
      <meta name="robots" content="index, follow" />
      <meta name="language" content="French" />
      <meta name="revisit-after" content="7 days" />

      {/* JSON-LD Structured Data */}
      {structuredData && (
        <script type="application/ld+json">
          {JSON.stringify(structuredData)}
        </script>
      )}
    </Helmet>
  );
};

export default SEOHead;
