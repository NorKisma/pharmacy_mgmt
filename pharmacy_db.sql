-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: Nov 25, 2025 at 02:39 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pharmacy_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('0c70e0177022');

-- --------------------------------------------------------

--
-- Table structure for table `audit_logs`
--

CREATE TABLE `audit_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `action` varchar(255) NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `object_type` varchar(50) DEFAULT NULL,
  `object_id` int(11) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `audit_logs`
--

INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `ip_address`, `object_type`, `object_id`, `is_deleted`, `deleted_at`, `created_at`, `updated_at`) VALUES
(3, NULL, 'Created new user account', '127.0.0.1', 'User', 13, 0, NULL, '2025-11-23 14:07:02', '2025-11-23 14:07:02'),
(4, NULL, 'Created new user account', '127.0.0.1', 'User', 14, 0, NULL, '2025-11-23 14:28:21', '2025-11-23 14:28:21'),
(5, NULL, 'User logged out', '127.0.0.1', 'User', 16, 0, NULL, '2025-11-23 14:45:19', '2025-11-23 14:45:19'),
(6, NULL, 'User logged out', '127.0.0.1', 'User', 16, 0, NULL, '2025-11-23 14:45:30', '2025-11-23 14:45:30'),
(7, NULL, 'User logged out', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-23 14:51:28', '2025-11-23 14:51:28'),
(8, NULL, 'User logged out', '127.0.0.1', 'User', 16, 0, NULL, '2025-11-24 12:17:57', '2025-11-24 12:17:57'),
(9, NULL, 'User logged out', '127.0.0.1', 'User', 16, 0, NULL, '2025-11-24 12:20:46', '2025-11-24 12:20:46'),
(10, NULL, 'User logged out', '127.0.0.1', 'User', 16, 0, NULL, '2025-11-24 12:20:52', '2025-11-24 12:20:52'),
(11, NULL, 'User logged out', '127.0.0.1', 'User', 16, 0, NULL, '2025-11-24 12:20:59', '2025-11-24 12:20:59'),
(12, NULL, 'User logged out', '127.0.0.1', 'User', 16, 0, NULL, '2025-11-24 13:57:55', '2025-11-24 13:57:55'),
(13, 17, 'User logged in', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-24 13:58:15', '2025-11-24 13:58:15'),
(14, NULL, 'User logged out', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-24 14:11:41', '2025-11-24 14:11:41'),
(15, 17, 'User logged in', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-24 14:11:46', '2025-11-24 14:11:46'),
(16, NULL, 'User logged out', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-24 15:00:07', '2025-11-24 15:00:07'),
(17, NULL, 'New user registered', '127.0.0.1', 'User', 18, 0, NULL, '2025-11-24 15:01:20', '2025-11-24 15:01:20'),
(18, 17, 'User logged in', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-24 15:01:33', '2025-11-24 15:01:33'),
(19, NULL, 'User logged out', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 10:10:19', '2025-11-25 10:10:19'),
(20, 17, 'User logged in', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 10:10:25', '2025-11-25 10:10:25'),
(21, NULL, 'User logged out', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 10:43:39', '2025-11-25 10:43:39'),
(22, 17, 'User logged in', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 10:51:03', '2025-11-25 10:51:03'),
(23, NULL, 'User logged out', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 10:51:13', '2025-11-25 10:51:13'),
(24, 17, 'User logged in', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 11:13:46', '2025-11-25 11:13:46'),
(25, NULL, 'User logged out', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 11:25:31', '2025-11-25 11:25:31'),
(26, 17, 'User logged in', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 11:25:43', '2025-11-25 11:25:43'),
(27, 17, 'New user registered', '127.0.0.1', 'User', 21, 0, NULL, '2025-11-25 11:36:43', '2025-11-25 11:36:43'),
(28, 17, 'User deleted', '127.0.0.1', 'User', 21, 0, NULL, '2025-11-25 11:38:38', '2025-11-25 11:38:38'),
(29, 17, 'User profile edited by nor Mohamed', '127.0.0.1', 'User', 16, 0, NULL, '2025-11-25 13:09:15', '2025-11-25 13:09:15'),
(30, 17, 'User profile edited by nor Mohamed', '127.0.0.1', 'User', 16, 0, NULL, '2025-11-25 13:09:52', '2025-11-25 13:09:52'),
(31, NULL, 'User logged out', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:10:11', '2025-11-25 13:10:11'),
(32, 17, 'User logged in', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:10:16', '2025-11-25 13:10:16'),
(33, 17, 'User profile edited by nor Mohamed', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:10:30', '2025-11-25 13:10:30'),
(34, 17, 'User profile edited by nor Mohamed', '127.0.0.1', 'User', 16, 0, NULL, '2025-11-25 13:12:17', '2025-11-25 13:12:17'),
(35, NULL, 'User logged out', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:12:21', '2025-11-25 13:12:21'),
(36, 17, 'User logged in', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:12:38', '2025-11-25 13:12:38'),
(37, NULL, 'User logged out', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:12:40', '2025-11-25 13:12:40'),
(38, 17, 'User logged in', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:14:20', '2025-11-25 13:14:20'),
(39, 17, 'User profile edited by nor Mohamed', '127.0.0.1', 'User', 16, 0, NULL, '2025-11-25 13:15:02', '2025-11-25 13:15:02'),
(40, NULL, 'User logged out', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:15:05', '2025-11-25 13:15:05'),
(41, 17, 'User logged in', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:15:24', '2025-11-25 13:15:24'),
(42, NULL, 'User logged out', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:15:41', '2025-11-25 13:15:41'),
(43, 17, 'User logged in', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:18:17', '2025-11-25 13:18:17'),
(44, NULL, 'User logged out', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:32:09', '2025-11-25 13:32:09'),
(45, 17, 'User logged in', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:36:09', '2025-11-25 13:36:09'),
(46, NULL, 'User logged out', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:36:13', '2025-11-25 13:36:13'),
(47, 17, 'User logged in', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:37:02', '2025-11-25 13:37:02'),
(48, NULL, 'User logged out', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:37:04', '2025-11-25 13:37:04'),
(49, 17, 'User logged in', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:37:39', '2025-11-25 13:37:39'),
(50, NULL, 'User logged out', '127.0.0.1', 'User', 17, 0, NULL, '2025-11-25 13:37:46', '2025-11-25 13:37:46');

-- --------------------------------------------------------

--
-- Table structure for table `company_settings`
--

CREATE TABLE `company_settings` (
  `id` int(11) NOT NULL,
  `name` varchar(120) NOT NULL,
  `short_name` varchar(50) DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `website` varchar(120) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `permissions`
--

CREATE TABLE `permissions` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `name`, `description`, `created_at`, `updated_at`, `is_deleted`, `deleted_at`) VALUES
(1, 'admin', NULL, '2025-11-23 11:32:27', '2025-11-23 11:32:27', 0, NULL),
(2, 'staff', NULL, '2025-11-23 11:32:27', '2025-11-23 11:32:27', 0, NULL),
(3, 'user', NULL, '2025-11-23 11:32:27', '2025-11-23 11:32:27', 0, NULL),
(4, 'manager', NULL, '2025-11-23 11:41:17', '2025-11-23 11:41:17', 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `role_permissions`
--

CREATE TABLE `role_permissions` (
  `role_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `role_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `name` varchar(150) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `password_hash`, `active`, `role_id`, `created_at`, `updated_at`, `created_by`, `name`, `is_deleted`, `deleted_at`) VALUES
(16, 'admin@pharmacy.com', 'pbkdf2:sha256:1000000$NYQZJ8Z0aTluhxTw$a87c7e36169549ee2ed670c2442849f2adb93c31f5920dac43c5c4fa17a525e9', 1, 4, '2025-11-23 14:44:37', '2025-11-25 13:15:02', NULL, 'Mohamed Ali', 0, NULL),
(17, 'nor.jws@gmail.com', 'pbkdf2:sha256:1000000$4Yb4GH2BKAAEtDhX$9cfa29259187a4a72f406e83c0dda57deb89acc414254719b335efc946b8193a', 1, 1, '2025-11-23 14:46:20', '2025-11-23 14:46:20', NULL, 'nor Mohamed', 0, NULL),
(18, 'muuse@gmail.com', 'pbkdf2:sha256:1000000$8l3SWEsze9I4wuXY$ea9f17215ef7eab558a02c094b9523baf9fb9d3163c619a30911a133d649f4af', 1, 3, '2025-11-24 15:01:20', '2025-11-24 15:01:20', NULL, 'Muuse Ahmed Ali', 0, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `audit_logs`
--
ALTER TABLE `audit_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `company_settings`
--
ALTER TABLE `company_settings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `permissions`
--
ALTER TABLE `permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `role_permissions`
--
ALTER TABLE `role_permissions`
  ADD PRIMARY KEY (`role_id`,`permission_id`),
  ADD KEY `permission_id` (`permission_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `audit_logs`
--
ALTER TABLE `audit_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `company_settings`
--
ALTER TABLE `company_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `permissions`
--
ALTER TABLE `permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `audit_logs`
--
ALTER TABLE `audit_logs`
  ADD CONSTRAINT `audit_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `role_permissions`
--
ALTER TABLE `role_permissions`
  ADD CONSTRAINT `role_permissions_ibfk_1` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`),
  ADD CONSTRAINT `role_permissions_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `users_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
