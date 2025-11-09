-- ============================================
-- PHASE 1: MIGRATION SÉCURITÉ CRITIQUE
-- Enable RLS + Indexes Essentiels
-- Durée estimée: 15 minutes
-- ============================================

-- ============================================
-- PARTIE 1: ENABLE ROW LEVEL SECURITY (RLS)
-- ============================================

-- Users table
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
    ON users FOR SELECT
    USING (auth.uid() = id OR auth.jwt()->>'role' = 'admin');

CREATE POLICY "Users can update own profile"
    ON users FOR UPDATE
    USING (auth.uid() = id);

CREATE POLICY "Admins can do anything"
    ON users FOR ALL
    USING (auth.jwt()->>'role' = 'admin');

-- Products table
ALTER TABLE products ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view published products"
    ON products FOR SELECT
    USING (status = 'active' OR merchant_id = auth.uid() OR auth.jwt()->>'role' = 'admin');

CREATE POLICY "Merchants can create products"
    ON products FOR INSERT
    WITH CHECK (merchant_id = auth.uid() AND auth.jwt()->>'role' = 'merchant');

CREATE POLICY "Merchants can update own products"
    ON products FOR UPDATE
    USING (merchant_id = auth.uid());

CREATE POLICY "Merchants can delete own products"
    ON products FOR DELETE
    USING (merchant_id = auth.uid());

-- Sales table
ALTER TABLE sales ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own sales"
    ON sales FOR SELECT
    USING (
        influencer_id = auth.uid()
        OR merchant_id = auth.uid()
        OR auth.jwt()->>'role' = 'admin'
    );

CREATE POLICY "System can create sales"
    ON sales FOR INSERT
    WITH CHECK (true); -- Créées par le système

-- Leads table
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own leads"
    ON leads FOR SELECT
    USING (
        influencer_id = auth.uid()
        OR merchant_id = auth.uid()
        OR auth.jwt()->>'role' = 'admin'
    );

CREATE POLICY "Influencers can create leads"
    ON leads FOR INSERT
    WITH CHECK (influencer_id = auth.uid() AND auth.jwt()->>'role' = 'influencer');

-- Transactions table
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own transactions"
    ON transactions FOR SELECT
    USING (user_id = auth.uid() OR auth.jwt()->>'role' = 'admin');

-- Deposits table
ALTER TABLE deposits ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own deposits"
    ON deposits FOR SELECT
    USING (user_id = auth.uid() OR auth.jwt()->>'role' = 'admin');

-- Withdrawals table
ALTER TABLE withdrawals ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own withdrawals"
    ON withdrawals FOR SELECT
    USING (user_id = auth.uid() OR auth.jwt()->>'role' = 'admin');

CREATE POLICY "Users can request withdrawals"
    ON withdrawals FOR INSERT
    WITH CHECK (user_id = auth.uid());

-- Subscriptions table
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own subscription"
    ON subscriptions FOR SELECT
    USING (user_id = auth.uid() OR auth.jwt()->>'role' = 'admin');

-- ============================================
-- PARTIE 2: INDEXES CRITIQUES (FOREIGN KEYS)
-- ============================================

-- Products indexes
CREATE INDEX IF NOT EXISTS idx_products_merchant_id ON products(merchant_id);
CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);
CREATE INDEX IF NOT EXISTS idx_products_created_at ON products(created_at DESC);

-- Sales indexes
CREATE INDEX IF NOT EXISTS idx_sales_influencer_id ON sales(influencer_id);
CREATE INDEX IF NOT EXISTS idx_sales_merchant_id ON sales(merchant_id);
CREATE INDEX IF NOT EXISTS idx_sales_product_id ON sales(product_id);
CREATE INDEX IF NOT EXISTS idx_sales_created_at ON sales(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_sales_status ON sales(status);

-- Leads indexes
CREATE INDEX IF NOT EXISTS idx_leads_influencer_id ON leads(influencer_id);
CREATE INDEX IF NOT EXISTS idx_leads_merchant_id ON leads(merchant_id);
CREATE INDEX IF NOT EXISTS idx_leads_product_id ON leads(product_id);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at DESC);

-- Transactions indexes
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type);
CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions(created_at DESC);

-- Deposits indexes
CREATE INDEX IF NOT EXISTS idx_deposits_user_id ON deposits(user_id);
CREATE INDEX IF NOT EXISTS idx_deposits_status ON deposits(status);
CREATE INDEX IF NOT EXISTS idx_deposits_created_at ON deposits(created_at DESC);

-- Withdrawals indexes
CREATE INDEX IF NOT EXISTS idx_withdrawals_user_id ON withdrawals(user_id);
CREATE INDEX IF NOT EXISTS idx_withdrawals_status ON withdrawals(status);
CREATE INDEX IF NOT EXISTS idx_withdrawals_created_at ON withdrawals(created_at DESC);

-- Subscriptions indexes
CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_plan ON subscriptions(plan);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status);

-- ============================================
-- PARTIE 3: INDEXES JSONB (GIN)
-- ============================================

-- Products metadata
CREATE INDEX IF NOT EXISTS idx_products_metadata_gin ON products USING GIN (metadata);

-- Users preferences
CREATE INDEX IF NOT EXISTS idx_users_preferences_gin ON users USING GIN (preferences);

-- Leads data
CREATE INDEX IF NOT EXISTS idx_leads_data_gin ON leads USING GIN (data);

-- ============================================
-- PARTIE 4: AUDIT LOGGING
-- ============================================

-- Table d'audit
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name TEXT NOT NULL,
    operation TEXT NOT NULL, -- INSERT, UPDATE, DELETE
    user_id UUID,
    old_data JSONB,
    new_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour recherche
CREATE INDEX IF NOT EXISTS idx_audit_logs_table_name ON audit_logs(table_name);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at DESC);

-- Fonction générique d'audit
CREATE OR REPLACE FUNCTION audit_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_logs (table_name, operation, user_id, new_data)
        VALUES (TG_TABLE_NAME, TG_OP, auth.uid(), row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_logs (table_name, operation, user_id, old_data, new_data)
        VALUES (TG_TABLE_NAME, TG_OP, auth.uid(), row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_logs (table_name, operation, user_id, old_data)
        VALUES (TG_TABLE_NAME, TG_OP, auth.uid(), row_to_json(OLD));
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Triggers d'audit sur tables critiques
CREATE TRIGGER users_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();

CREATE TRIGGER products_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON products
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();

CREATE TRIGGER sales_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON sales
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();

CREATE TRIGGER transactions_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON transactions
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();

-- ============================================
-- PARTIE 5: VALIDATION & VÉRIFICATION
-- ============================================

-- Vérifier RLS activée
SELECT
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

-- Vérifier indexes
SELECT
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- Statistiques
SELECT
    'RLS Enabled' as check_type,
    COUNT(*) as count
FROM pg_tables
WHERE schemaname = 'public' AND rowsecurity = true
UNION ALL
SELECT
    'Indexes Created',
    COUNT(*)
FROM pg_indexes
WHERE schemaname = 'public';

COMMENT ON TABLE audit_logs IS 'Audit trail pour toutes les opérations critiques (RGPD compliant)';
