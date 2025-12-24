CREATE DATABASE IF NOT EXISTS price_comparator CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE price_comparator;
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(255),
    prix DECIMAL(10,2),
    image VARCHAR(500),
    lien VARCHAR(500),
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY ux_lien (lien(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
