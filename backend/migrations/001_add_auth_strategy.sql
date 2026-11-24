-- Міграція: додавання підтримки типів автентифікації (password_2fa / sso_link)
-- Дата: 2026-11-23
-- Додає колонку auth_type до таблиці services та totp_secret до таблиці credentials

-- Додаємо колонку auth_type до таблиці services
-- Значення за замовчуванням: 'password_2fa'
ALTER TABLE services
    ADD COLUMN auth_type ENUM('password_2fa', 'sso_link') NOT NULL DEFAULT 'password_2fa'
    COMMENT 'Тип автентифікації: password_2fa або sso_link';

-- Додаємо колонку totp_secret до таблиці credentials
-- Зберігає Base32 секрет TOTP (наприклад, JBSWY3DPEHPK3PXP)
ALTER TABLE credentials
    ADD COLUMN totp_secret VARCHAR(64) NULL
    COMMENT 'Base32 секрет TOTP (наприклад, JBSWY3DPEHPK3PXP)';
