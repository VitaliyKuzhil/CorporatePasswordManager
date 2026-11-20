CREATE TABLE `users` (
  `user_id` integer PRIMARY KEY AUTO_INCREMENT,
  `full_name` varchar(100),
  `login` varchar(50) UNIQUE,
  `protected_password` varchar(255) COMMENT 'AES-зашифрований пароль',
  `phone` varchar(20),
  `avatar_url` varchar(255) COMMENT 'Зберігаємо посилання (S3/сервер)',
  `role` varchar(20) DEFAULT 'user' COMMENT '''admin'' або ''user''',
  `status` varchar(20) DEFAULT 'active' COMMENT '''active'' або ''blocked''',
  `created_at` datetime DEFAULT (now())
);

CREATE TABLE `services` (
  `service_id` integer PRIMARY KEY AUTO_INCREMENT,
  `service_name` varchar(100),
  `service_url` varchar(255) COMMENT 'Посилання для швидкого переходу на сайт',
  `service_logo_url` varchar(255)
);

CREATE TABLE `credentials` (
  `credential_id` integer PRIMARY KEY AUTO_INCREMENT,
  `service_id` integer NOT NULL,
  `login` varchar(100),
  `protected_password` varchar(255) COMMENT 'AES-зашифрований пароль',
  `comment` text
);

CREATE TABLE `user_credential_access` (
  `user_id` integer,
  `credential_id` integer,
  `is_active` boolean DEFAULT true COMMENT 'Можливість тимчасово забрати доступ без видалення запису',
  `granted_at` datetime DEFAULT (now()),
  PRIMARY KEY (`user_id`, `credential_id`)
);

ALTER TABLE `credentials` ADD FOREIGN KEY (`service_id`) REFERENCES `services` (`service_id`) ON DELETE CASCADE;

ALTER TABLE `user_credential_access` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

ALTER TABLE `user_credential_access` ADD FOREIGN KEY (`credential_id`) REFERENCES `credentials` (`credential_id`) ON DELETE CASCADE;
