-- ============================================
-- TABLES POUR NOUVEAUX SERVICES
-- AI Assistant, Content Studio, TikTok Shop, WhatsApp
-- ============================================

-- Table pour conversations AI Assistant
CREATE TABLE IF NOT EXISTS ai_conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_id VARCHAR(100),
    message TEXT NOT NULL,
    response TEXT,
    language VARCHAR(10) DEFAULT 'fr',
    context JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT fk_ai_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_ai_conversations_user ON ai_conversations(user_id);
CREATE INDEX idx_ai_conversations_session ON ai_conversations(session_id);
CREATE INDEX idx_ai_conversations_created ON ai_conversations(created_at);

-- Table pour historique de traductions
CREATE TABLE IF NOT EXISTS ai_translations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    source_text TEXT NOT NULL,
    translated_text TEXT NOT NULL,
    source_language VARCHAR(10) NOT NULL,
    target_language VARCHAR(10) NOT NULL,
    confidence_score DECIMAL(3,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_ai_translations_user ON ai_translations(user_id);

-- Table pour pr├®dictions de ventes
CREATE TABLE IF NOT EXISTS ai_sales_predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id) ON DELETE SET NULL,
    predicted_sales INTEGER NOT NULL,
    confidence_min INTEGER,
    confidence_max INTEGER,
    trend VARCHAR(20),
    factors JSONB,
    recommendations JSONB,
    time_period VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_ai_predictions_user ON ai_sales_predictions(user_id);
CREATE INDEX idx_ai_predictions_product ON ai_sales_predictions(product_id);

-- Table pour contenus g├®n├®r├®s par Content Studio
CREATE TABLE IF NOT EXISTS content_studio_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    content_type VARCHAR(50) NOT NULL, -- post, story, reel, carousel, video
    platform VARCHAR(50) NOT NULL, -- instagram, tiktok, facebook, etc.
    media_urls JSONB, -- Array of image/video URLs
    caption TEXT,
    hashtags JSONB,
    scheduled_at TIMESTAMP WITH TIME ZONE,
    published_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'draft', -- draft, scheduled, published, failed
    analytics JSONB, -- likes, comments, shares, views
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_content_posts_user ON content_studio_posts(user_id);
CREATE INDEX idx_content_posts_status ON content_studio_posts(status);
CREATE INDEX idx_content_posts_scheduled ON content_studio_posts(scheduled_at);

-- Table pour templates Content Studio
CREATE TABLE IF NOT EXISTS content_studio_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL, -- product_showcase, promotion, review, etc.
    template_data JSONB NOT NULL, -- Design, colors, fonts, layout
    thumbnail_url TEXT,
    is_public BOOLEAN DEFAULT false,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_content_templates_category ON content_studio_templates(category);
CREATE INDEX idx_content_templates_public ON content_studio_templates(is_public);

-- Table pour A/B Testing
CREATE TABLE IF NOT EXISTS content_ab_tests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    test_name VARCHAR(255) NOT NULL,
    variant_a_post_id UUID REFERENCES content_studio_posts(id) ON DELETE CASCADE,
    variant_b_post_id UUID REFERENCES content_studio_posts(id) ON DELETE CASCADE,
    variant_a_metrics JSONB,
    variant_b_metrics JSONB,
    winner VARCHAR(10), -- 'A', 'B', or 'TIE'
    status VARCHAR(50) DEFAULT 'running', -- running, completed, stopped
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_ab_tests_user ON content_ab_tests(user_id);
CREATE INDEX idx_ab_tests_status ON content_ab_tests(status);

-- Table pour produits TikTok Shop
CREATE TABLE IF NOT EXISTS tiktok_shop_products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id) ON DELETE SET NULL,
    tiktok_product_id VARCHAR(100) UNIQUE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    inventory INTEGER DEFAULT 0,
    category VARCHAR(100),
    images JSONB,
    status VARCHAR(50) DEFAULT 'DRAFT', -- DRAFT, PENDING, APPROVED, REJECTED, LIVE, SUSPENDED
    rejection_reason TEXT,
    sync_status VARCHAR(50) DEFAULT 'pending', -- pending, synced, failed
    last_synced_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_tiktok_products_user ON tiktok_shop_products(user_id);
CREATE INDEX idx_tiktok_products_status ON tiktok_shop_products(status);
CREATE INDEX idx_tiktok_products_tiktok_id ON tiktok_shop_products(tiktok_product_id);

-- Table pour commandes TikTok Shop
CREATE TABLE IF NOT EXISTS tiktok_shop_orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tiktok_order_id VARCHAR(100) UNIQUE NOT NULL,
    tiktok_product_id VARCHAR(100),
    customer_name VARCHAR(255),
    customer_phone VARCHAR(50),
    total_amount DECIMAL(10,2) NOT NULL,
    commission_amount DECIMAL(10,2),
    status VARCHAR(50) NOT NULL, -- UNPAID, PAID, SHIPPED, DELIVERED, CANCELLED, COMPLETED
    tracking_number VARCHAR(100),
    shipping_address JSONB,
    order_items JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_tiktok_orders_user ON tiktok_shop_orders(user_id);
CREATE INDEX idx_tiktok_orders_status ON tiktok_shop_orders(status);
CREATE INDEX idx_tiktok_orders_tiktok_id ON tiktok_shop_orders(tiktok_order_id);

-- Table pour analytics TikTok
CREATE TABLE IF NOT EXISTS tiktok_shop_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tiktok_product_id VARCHAR(100),
    date DATE NOT NULL,
    views INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    add_to_cart INTEGER DEFAULT 0,
    purchases INTEGER DEFAULT 0,
    revenue DECIMAL(10,2) DEFAULT 0,
    conversion_rate DECIMAL(5,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, tiktok_product_id, date)
);

CREATE INDEX idx_tiktok_analytics_user ON tiktok_shop_analytics(user_id);
CREATE INDEX idx_tiktok_analytics_date ON tiktok_shop_analytics(date);

-- Table pour messages WhatsApp
CREATE TABLE IF NOT EXISTS whatsapp_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message_id VARCHAR(255), -- WhatsApp message ID
    from_phone VARCHAR(50) NOT NULL,
    to_phone VARCHAR(50) NOT NULL,
    message_type VARCHAR(50) NOT NULL, -- text, template, image, document, interactive
    content TEXT,
    media_url TEXT,
    template_name VARCHAR(100),
    status VARCHAR(50) DEFAULT 'sent', -- sent, delivered, read, failed
    direction VARCHAR(20) NOT NULL, -- inbound, outbound
    error_message TEXT,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_whatsapp_messages_user ON whatsapp_messages(user_id);
CREATE INDEX idx_whatsapp_messages_from ON whatsapp_messages(from_phone);
CREATE INDEX idx_whatsapp_messages_to ON whatsapp_messages(to_phone);
CREATE INDEX idx_whatsapp_messages_created ON whatsapp_messages(created_at);

-- Table pour conversations WhatsApp
CREATE TABLE IF NOT EXISTS whatsapp_conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    contact_phone VARCHAR(50) NOT NULL,
    contact_name VARCHAR(255),
    last_message TEXT,
    last_message_at TIMESTAMP WITH TIME ZONE,
    unread_count INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'active', -- active, archived, blocked
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, contact_phone)
);

CREATE INDEX idx_whatsapp_conv_user ON whatsapp_conversations(user_id);
CREATE INDEX idx_whatsapp_conv_phone ON whatsapp_conversations(contact_phone);
CREATE INDEX idx_whatsapp_conv_last_msg ON whatsapp_conversations(last_message_at);

-- Table pour templates WhatsApp
CREATE TABLE IF NOT EXISTS whatsapp_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    template_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL, -- transactional, marketing, authentication, utility
    language VARCHAR(10) NOT NULL,
    content TEXT NOT NULL,
    variables JSONB, -- {1: "nom", 2: "montant", etc.}
    status VARCHAR(50) DEFAULT 'draft', -- draft, pending, approved, rejected
    whatsapp_template_id VARCHAR(100),
    is_public BOOLEAN DEFAULT false,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_whatsapp_templates_category ON whatsapp_templates(category);
CREATE INDEX idx_whatsapp_templates_status ON whatsapp_templates(status);

-- Table pour notifications WhatsApp
CREATE TABLE IF NOT EXISTS whatsapp_notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    notification_type VARCHAR(100) NOT NULL, -- new_sale, commission_paid, low_stock, etc.
    recipient_phone VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    template_used VARCHAR(100),
    status VARCHAR(50) DEFAULT 'pending', -- pending, sent, failed
    sent_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_whatsapp_notif_user ON whatsapp_notifications(user_id);
CREATE INDEX idx_whatsapp_notif_status ON whatsapp_notifications(status);

-- ============================================
-- COMMENTAIRES ET DOCUMENTATION
-- ============================================

COMMENT ON TABLE ai_conversations IS 'Historique des conversations avec l''assistant IA multilingue';
COMMENT ON TABLE ai_translations IS 'Historique des traductions FR Ôåö AR Ôåö EN';
COMMENT ON TABLE ai_sales_predictions IS 'Pr├®dictions de ventes g├®n├®r├®es par ML';
COMMENT ON TABLE content_studio_posts IS 'Contenus cr├®├®s et planifi├®s via Content Studio';
COMMENT ON TABLE content_studio_templates IS 'Templates r├®utilisables pour cr├®ation de contenu';
COMMENT ON TABLE content_ab_tests IS 'Tests A/B pour optimiser le contenu';
COMMENT ON TABLE tiktok_shop_products IS 'Produits synchronis├®s avec TikTok Shop';
COMMENT ON TABLE tiktok_shop_orders IS 'Commandes pass├®es via TikTok Shop';
COMMENT ON TABLE tiktok_shop_analytics IS 'M├®triques de performance TikTok Shop par jour';
COMMENT ON TABLE whatsapp_messages IS 'Tous les messages WhatsApp envoy├®s/re├ºus';
COMMENT ON TABLE whatsapp_conversations IS 'Fils de conversation WhatsApp';
COMMENT ON TABLE whatsapp_templates IS 'Templates de messages WhatsApp pr├®-approuv├®s';
COMMENT ON TABLE whatsapp_notifications IS 'Notifications automatiques envoy├®es via WhatsApp';
