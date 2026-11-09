-- ====================================================================
-- AI BASED FAKE NEWS DETECTION SYSTEM - SEED DATA
-- Default Admin: admin@fakenews.ai / Admin@12345
-- Default User:  user@fakenews.ai  / User@12345
-- ====================================================================

USE `fake_news_detection`;

-- Insert Initial Admin User and Regular Demo User
-- Password hashes generated via werkzeug.security.generate_password_hash
INSERT INTO `users` (`id`, `full_name`, `email`, `username`, `password_hash`, `role`, `is_active`) VALUES
(1, 'System Administrator', 'admin@fakenews.ai', 'admin', 'scrypt:32768:8:1$7Cg7uJ9K$9bb6fbbbf519a84e27fca2ff2890538a7199c072df2e6dc9f91192d6cf4216892e8a15617351ee2bc3d779ff6dbe74bfbfbfbb6a44ca704870570b240be0cce2', 'admin', 1),
(2, 'Research Student', 'user@fakenews.ai', 'demouser', 'scrypt:32768:8:1$u7A3mK4v$0ebcbde0a0f88ff8bf94f923b08e2f8d4bc4d0590a969e2c65a04ebfbcad3eb9a341cbfa04cce8f0ba7dcbc3d67417e0ef57c0e86b46487eec8219488a037dfc', 'user', 1)
ON DUPLICATE KEY UPDATE `email` = VALUES(`email`);

-- Link User 1 to Admins table
INSERT INTO `admins` (`id`, `user_id`) VALUES (1, 1)
ON DUPLICATE KEY UPDATE `user_id` = VALUES(`user_id`);

-- Initial Datasets Registration
INSERT INTO `datasets` (`id`, `dataset_name`, `dataset_type`, `file_path`, `record_count`, `dataset_version`, `status`) VALUES
(1, 'Self-Generated Fake & Real News Dataset', 'self_generated', 'dataset/self_generated/self_generated_news.csv', 120, 'v1.0.0', 'ACTIVE'),
(2, 'Kaggle Benchmark Fake News Dataset', 'kaggle', 'dataset/kaggle/kaggle_news.csv', 250, 'v1.0.0', 'ACTIVE'),
(3, 'Harmonized Hybrid News Dataset', 'hybrid', 'dataset/hybrid/hybrid_dataset.csv', 370, 'v1.0.0', 'ACTIVE')
ON DUPLICATE KEY UPDATE `dataset_name` = VALUES(`dataset_name`);

-- Initial Model Version
INSERT INTO `model_versions` (`id`, `version_name`, `model_path`, `vectorizer_path`, `training_dataset_version`, `evaluation_metrics_json`, `is_active`) VALUES
(1, 'Calibrated-LinearSVC-v1.0.0', 'trained_models/fake_news_model.pkl', 'trained_models/tfidf_vectorizer.pkl', 'hybrid-v1.0.0', '{"accuracy": 0.945, "precision": 0.942, "recall": 0.948, "f1_score": 0.945, "roc_auc": 0.985}', 1)
ON DUPLICATE KEY UPDATE `version_name` = VALUES(`version_name`);

-- Sample News Entries
INSERT INTO `news` (`id`, `title`, `article`, `category`, `source`, `content_hash`) VALUES
(1, 'NASA James Webb Space Telescope Detects Water Vapor in Rocky Planet Atmosphere', 'Astronomers utilizing the James Webb Space Telescope have confirmed the presence of atmospheric water vapor around an exoplanet in the habitable zone. The peer-reviewed findings were published in the Astrophysical Journal following rigorous spectral analysis.', 'Science', 'NASA Press Office', 'a1b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef0'),
(2, 'Secret Subterranean City Discovered Beneath Antarctic Ice Shelf Houses Ancient Alien Technology', 'Whistleblower claims naval researchers uncovered a 50,000-year-old alien complex buried 2 miles beneath the ice sheet that powers a planetary weather control device suppressed by global elites.', 'Conspiracy', 'Viral Social Post', 'f0e1d2c3b4a5968778695a4b3c2d1e0f0123456789abcdef0123456789abcdef1')
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`);

-- Sample Predictions
INSERT INTO `prediction_history` (`id`, `user_id`, `news_id`, `prediction_label`, `confidence_score`, `model_version`, `analysis_type`, `prediction_source`, `result_status`) VALUES
(1, 2, 1, 'REAL', 0.952, 'Calibrated-LinearSVC-v1.0.0', 'ml_previous', 'web_ui', 'COMPLETED'),
(2, 2, 2, 'FAKE', 0.981, 'Calibrated-LinearSVC-v1.0.0', 'ml_previous', 'web_ui', 'COMPLETED')
ON DUPLICATE KEY UPDATE `news_id` = VALUES(`news_id`);

-- Sample Gemini Verification for prediction 1
INSERT INTO `gemini_verification` (`id`, `prediction_history_id`, `assessment`, `confidence_score`, `evidence_summary`, `sources_json`, `agreement_status`) VALUES
(1, 1, 'REAL', 0.96, 'NASA official releases and peer-reviewed astrophysical literature corroborate recent JWST spectroscopic discoveries of atmospheric water vapor signatures on exoplanets.', '["https://www.nasa.gov", "https://iopscience.iop.org/journal/0004-637X"]', 'AGREE')
ON DUPLICATE KEY UPDATE `prediction_history_id` = VALUES(`prediction_history_id`);

-- Sample Saved News
INSERT INTO `saved_news` (`id`, `user_id`, `news_id`) VALUES (1, 2, 1)
ON DUPLICATE KEY UPDATE `news_id` = VALUES(`news_id`);
