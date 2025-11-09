/**
 * Configuration SEO pour toutes les pages
 * Chaque page a ses meta tags et structured data spécifiques
 */

const SEO_CONFIG = {
  homepage: {
    title: 'GetYourShare - Plateforme d\'affiliation B2B',
    description: 'Plateforme d\'affiliation B2B qui connecte entreprises, commerciaux et influenceurs. Chaque partage devient une vente avec tracking en temps réel et commissions automatiques.',
    keywords: 'affiliation B2B, marketing digital, influenceurs, commissions, tracking, leads',
    image: 'https://getyourshare.com/og-homepage.jpg',
    type: 'website',
    url: 'https://getyourshare.com',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'WebSite',
      name: 'GetYourShare',
      description: 'Plateforme d\'affiliation B2B',
      url: 'https://getyourshare.com',
      logo: 'https://getyourshare.com/logo.png',
      sameAs: [
        'https://www.facebook.com/getyourshare',
        'https://www.linkedin.com/company/getyourshare',
        'https://twitter.com/getyourshare'
      ]
    }
  },

  marketplace: {
    title: 'Marketplace - Trouvez des Opportunités d\'Affiliation',
    description: 'Découvrez et explorez les meilleures opportunités d\'affiliation B2B. Connectez-vous avec des marques et des produits premium adaptés à votre audience.',
    keywords: 'marketplace affiliation, opportunités marketing, partenaires B2B, produits premium',
    image: 'https://getyourshare.com/og-marketplace.jpg',
    type: 'website',
    url: 'https://getyourshare.com/marketplace',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'CollectionPage',
      name: 'Marketplace GetYourShare',
      description: 'Opportunités d\'affiliation B2B'
    }
  },

  pricing: {
    title: 'Tarification - Plans d\'Affiliation Transparents',
    description: 'Découvrez nos plans de tarification transparents pour les affiliés et les marques. Commissions compétitives, pas de frais cachés.',
    keywords: 'tarification affiliation, commissions, plans pricing, frais transparents',
    image: 'https://getyourshare.com/og-pricing.jpg',
    type: 'website',
    url: 'https://getyourshare.com/pricing',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'PriceSpecification',
      name: 'Plans de Tarification',
      description: 'Plans d\'affiliation avec commissions compétitives'
    }
  },

  about: {
    title: 'À Propos - Notre Mission de Transformation Digitale',
    description: 'Découvrez l\'histoire de GetYourShare, notre mission de transformer le marketing B2B et notre équipe passionnée.',
    keywords: 'à propos, mission, équipe, histoire, transformation digitale',
    image: 'https://getyourshare.com/og-about.jpg',
    type: 'website',
    url: 'https://getyourshare.com/about',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'Organization',
      name: 'GetYourShare',
      description: 'Plateforme d\'affiliation B2B',
      url: 'https://getyourshare.com',
      contactPoint: {
        '@type': 'ContactPoint',
        contactType: 'Customer Service',
        email: 'support@getyourshare.com'
      }
    }
  },

  contact: {
    title: 'Contact - Parlons de Votre Stratégie d\'Affiliation',
    description: 'Contactez notre équipe pour discuter de vos besoins en affiliation B2B. Nous sommes là pour vous aider à réussir.',
    keywords: 'contact, support, aide, questions, affiliation',
    image: 'https://getyourshare.com/og-contact.jpg',
    type: 'website',
    url: 'https://getyourshare.com/contact',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'ContactPage',
      name: 'Contactez GetYourShare',
      description: 'Page de contact pour partenariats B2B'
    }
  },

  productDetail: {
    title: 'Détails du Produit - Opportunité d\'Affiliation Premium',
    description: 'Explorez les détails de ce produit d\'affiliation premium, les commissions, les conditions et les moyens de promotion.',
    keywords: 'produit affiliation, détails, commissions, promotion, marketing',
    image: 'https://getyourshare.com/og-product.jpg',
    type: 'product',
    url: 'https://getyourshare.com/product',
    structuredData: {
      '@context': 'https://schema.org',
      '@type': 'Product',
      name: 'Produit d\'Affiliation',
      description: 'Produit affilié avec opportunité de commission',
      image: 'https://getyourshare.com/product-image.jpg',
      brand: {
        '@type': 'Brand',
        name: 'GetYourShare'
      },
      offers: {
        '@type': 'AggregateOffer',
        availability: 'https://schema.org/InStock',
        priceCurrency: 'EUR',
        price: '0'
      }
    }
  },

  login: {
    title: 'Connexion - Accédez à Votre Compte GetYourShare',
    description: 'Connectez-vous à votre compte GetYourShare pour gérer vos affiliations, commissions et performances.',
    keywords: 'connexion, login, compte, affiliation',
    image: 'https://getyourshare.com/og-login.jpg',
    type: 'website',
    url: 'https://getyourshare.com/login',
    structuredData: null
  },

  register: {
    title: 'Inscription - Rejoignez la Communauté GetYourShare',
    description: 'Créez votre compte GetYourShare en quelques minutes et commencez à monétiser votre audience dès aujourd\'hui.',
    keywords: 'inscription, register, compte, affiliation, gratuit',
    image: 'https://getyourshare.com/og-register.jpg',
    type: 'website',
    url: 'https://getyourshare.com/register',
    structuredData: null
  }
};

export default SEO_CONFIG;
