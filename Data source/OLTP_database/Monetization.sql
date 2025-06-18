CREATE TABLE payments (
    payment_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency CHAR(3) DEFAULT 'USD',
    payment_method VARCHAR(20), -- 'credit_card', 'paypal'
    status VARCHAR(20) NOT NULL, -- 'pending', 'completed', 'failed'
    invoice_id VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Index cho truy vấn lịch sử thanh toán
CREATE INDEX idx_payments_user ON payments(user_id);
CREATE INDEX idx_payments_status ON payments(status);


CREATE TABLE advertisements (
    ad_id UUID PRIMARY KEY,
    advertiser_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    target_url TEXT NOT NULL,
    budget DECIMAL(15,2) NOT NULL,
    start_date TIMESTAMPTZ,
    end_date TIMESTAMPTZ,
    target_countries VARCHAR(2)[], -- Mã quốc gia target
    target_genres VARCHAR(50)[], -- Nhạc pop, rock...
    is_active BOOLEAN DEFAULT TRUE
);

-- Bảng lưu lần hiển thị/quảng cáo
CREATE TABLE ad_impressions (
    impression_id BIGSERIAL PRIMARY KEY,
    ad_id UUID NOT NULL,
    user_id UUID NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    is_clicked BOOLEAN DEFAULT FALSE,
    click_timestamp TIMESTAMPTZ,
    earnings DECIMAL(10,4) NOT NULL, -- Tiền kiếm được mỗi lần hiển thị/click
    FOREIGN KEY (ad_id) REFERENCES advertisements(ad_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
) PARTITION BY RANGE (timestamp);

CREATE INDEX idx_ad_impressions_ad ON ad_impressions(ad_id);
CREATE INDEX idx_ad_impressions_user ON ad_impressions(user_id);