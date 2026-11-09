-- ====================================================================
-- AI BASED FAKE NEWS DETECTION SYSTEM - DATABASE SCHEMA (MySQL 8.0+)
-- Database: fake_news_detection
-- ====================================================================

CREATE DATABASE IF NOT EXISTS `fake_news_detection`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE `fake_news_detection`;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `admin_logs`;
DROP TABLE IF EXISTS `training_logs`;
DROP TABLE IF EXISTS `model_versions`;
DROP TABLE IF EXISTS `gemini_verification`;
DROP TABLE IF EXISTS `datasets`;
DROP TABLE IF EXISTS `uploaded_files`;
DROP TABLE IF EXISTS `saved_news`;
DROP TABLE IF EXISTS `prediction_history`;
DROP TABLE IF EXISTS `news`;
DROP TABLE IF EXISTS `admins`;
DROP TABLE IF EXISTS `users`;

SET FOREIGN_KEY_CHECKS = 1;

-- 1. Users table
CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `full_name` VARCHAR(150) NOT NULL,
  `email` VARCHAR(150) NOT NULL UNIQUE,
  `username` VARCHAR(100) UNIQUE NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `role` VARCHAR(20) NOT NULL DEFAULT 'user',
  `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_users_email` (`email`),
  INDEX `idx_users_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Admins reference table
CREATE TABLE `admins` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL UNIQUE,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_admins_user` FOREIGN KEY (`user_id`)
    REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. News table
CREATE TABLE `news` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(500) NOT NULL,
  `article` LONGTEXT NOT NULL,
  `category` VARCHAR(100) DEFAULT 'General',
  `source` VARCHAR(255) DEFAULT 'User Input',
  `content_hash` VARCHAR(64) UNIQUE NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_news_content_hash` (`content_hash`),
  INDEX `idx_news_category` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Prediction History table
CREATE TABLE `prediction_history` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NULL,
  `news_id` INT NOT NULL,
  `prediction_label` VARCHAR(20) NOT NULL, -- 'FAKE', 'REAL', 'INCONCLUSIVE'
  `confidence_score` FLOAT NOT NULL,
  `model_version` VARCHAR(50) NOT NULL DEFAULT 'v1.0.0',
  `analysis_type` VARCHAR(50) NOT NULL, -- 'ml_previous', 'gemini_latest', 'file_batch'
  `prediction_source` VARCHAR(50) NOT NULL DEFAULT 'web_ui',
  `result_status` VARCHAR(50) NOT NULL DEFAULT 'COMPLETED',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_pred_user` FOREIGN KEY (`user_id`)
    REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_pred_news` FOREIGN KEY (`news_id`)
    REFERENCES `news` (`id`) ON DELETE CASCADE,
  INDEX `idx_pred_user` (`user_id`),
  INDEX `idx_pred_label` (`prediction_label`),
  INDEX `idx_pred_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Saved News bookmarks
CREATE TABLE `saved_news` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `news_id` INT NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_saved_user` FOREIGN KEY (`user_id`)
    REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_saved_news` FOREIGN KEY (`news_id`)
    REFERENCES `news` (`id`) ON DELETE CASCADE,
  UNIQUE KEY `uq_user_news_saved` (`user_id`, `news_id`),
  INDEX `idx_saved_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Uploaded Files table
CREATE TABLE `uploaded_files` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NULL,
  `original_filename` VARCHAR(255) NOT NULL,
  `stored_filename` VARCHAR(255) NOT NULL,
  `file_type` VARCHAR(20) NOT NULL, -- 'pdf', 'docx', 'txt', 'csv'
  `analysis_mode` VARCHAR(50) NOT NULL, -- 'ml_previous', 'gemini_latest'
  `processing_status` VARCHAR(50) NOT NULL DEFAULT 'COMPLETED',
  `records_count` INT NOT NULL DEFAULT 1,
  `uploaded_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_upload_user` FOREIGN KEY (`user_id`)
    REFERENCES `users` (`id`) ON DELETE SET NULL,
  INDEX `idx_upload_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Datasets registry table
CREATE TABLE `datasets` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `dataset_name` VARCHAR(150) NOT NULL,
  `dataset_type` VARCHAR(50) NOT NULL, -- 'self_generated', 'kaggle', 'hybrid'
  `file_path` VARCHAR(255) NOT NULL,
  `record_count` INT NOT NULL DEFAULT 0,
  `dataset_version` VARCHAR(50) NOT NULL DEFAULT 'v1.0.0',
  `status` VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_dataset_type` (`dataset_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Gemini Verification table
CREATE TABLE `gemini_verification` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `prediction_history_id` INT NOT NULL UNIQUE,
  `assessment` VARCHAR(50) NOT NULL, -- 'FAKE', 'REAL', 'UNVERIFIED', 'INCONCLUSIVE'
  `confidence_score` FLOAT NULL,
  `evidence_summary` MEDIUMTEXT NULL,
  `sources_json` JSON NULL,
  `agreement_status` VARCHAR(50) NOT NULL, -- 'AGREE', 'DISAGREE', 'INCONCLUSIVE'
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_gemini_pred` FOREIGN KEY (`prediction_history_id`)
    REFERENCES `prediction_history` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. Model Versions table
CREATE TABLE `model_versions` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `version_name` VARCHAR(100) NOT NULL UNIQUE,
  `model_path` VARCHAR(255) NOT NULL,
  `vectorizer_path` VARCHAR(255) NOT NULL,
  `training_dataset_version` VARCHAR(50) NOT NULL,
  `evaluation_metrics_json` JSON NOT NULL,
  `is_active` BOOLEAN NOT NULL DEFAULT FALSE,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. Training Logs table
CREATE TABLE `training_logs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `dataset_version` VARCHAR(50) NOT NULL,
  `model_version` VARCHAR(100) NOT NULL,
  `training_status` VARCHAR(50) NOT NULL, -- 'RUNNING', 'COMPLETED', 'FAILED'
  `metrics_json` JSON NULL,
  `error_message` TEXT NULL,
  `started_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `completed_at` TIMESTAMP NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 11. Admin Logs table
CREATE TABLE `admin_logs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `admin_id` INT NOT NULL,
  `action` VARCHAR(150) NOT NULL,
  `target_type` VARCHAR(50) NOT NULL,
  `target_id` INT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_admin_logs_admin` FOREIGN KEY (`admin_id`)
    REFERENCES `users` (`id`) ON DELETE CASCADE,
  INDEX `idx_admin_logs_admin` (`admin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
