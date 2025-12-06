/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.13-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: projectr_db
-- ------------------------------------------------------
-- Server version	10.11.13-MariaDB-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_profile`
--

DROP TABLE IF EXISTS `account_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_profile` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `profile_picture` varchar(100) DEFAULT NULL,
  `cover_picture` varchar(100) DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `headline` varchar(80) DEFAULT NULL,
  `bio` longtext DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `account_profile_user_id_bdd52018_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_profile`
--

LOCK TABLES `account_profile` WRITE;
/*!40000 ALTER TABLE `account_profile` DISABLE KEYS */;
INSERT INTO `account_profile` VALUES
(1,'Account/profile_images/default.jpg','Account/cover_images/_default.jpg',NULL,NULL,NULL,1),
(2,'Account/profile_images/default.jpg','Account/cover_images/_default.jpg',NULL,NULL,NULL,2),
(3,'Account/profile_images/default.jpg','Account/cover_images/_default.jpg',NULL,NULL,NULL,3),
(4,'Account/profile_images/default.jpg','Account/cover_images/_default.jpg',NULL,NULL,NULL,4),
(5,'Account/profile_images/default.jpg','Account/cover_images/_default.jpg',NULL,NULL,NULL,5),
(6,'Account/profile_images/default.jpg','Account/cover_images/_default.jpg',NULL,NULL,NULL,6);
/*!40000 ALTER TABLE `account_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_useractivitylog`
--

DROP TABLE IF EXISTS `account_useractivitylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_useractivitylog` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `session_key` varchar(40) DEFAULT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `login_time` datetime(6) NOT NULL,
  `last_activity` datetime(6) NOT NULL,
  `logout_time` datetime(6) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_useractivitylog_user_id_4250e034_fk_auth_user_id` (`user_id`),
  CONSTRAINT `account_useractivitylog_user_id_4250e034_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_useractivitylog`
--

LOCK TABLES `account_useractivitylog` WRITE;
/*!40000 ALTER TABLE `account_useractivitylog` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_useractivitylog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES
(2,'Manager'),
(3,'PlusUUser'),
(1,'User');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',3,'add_permission'),
(6,'Can change permission',3,'change_permission'),
(7,'Can delete permission',3,'delete_permission'),
(8,'Can view permission',3,'view_permission'),
(9,'Can add group',2,'add_group'),
(10,'Can change group',2,'change_group'),
(11,'Can delete group',2,'delete_group'),
(12,'Can view group',2,'view_group'),
(13,'Can add user',4,'add_user'),
(14,'Can change user',4,'change_user'),
(15,'Can delete user',4,'delete_user'),
(16,'Can view user',4,'view_user'),
(17,'Can add content type',5,'add_contenttype'),
(18,'Can change content type',5,'change_contenttype'),
(19,'Can delete content type',5,'delete_contenttype'),
(20,'Can view content type',5,'view_contenttype'),
(21,'Can add session',6,'add_session'),
(22,'Can change session',6,'change_session'),
(23,'Can delete session',6,'delete_session'),
(24,'Can view session',6,'view_session'),
(25,'Can add profile',7,'add_profile'),
(26,'Can change profile',7,'change_profile'),
(27,'Can delete profile',7,'delete_profile'),
(28,'Can view profile',7,'view_profile'),
(29,'Can add user activity log',8,'add_useractivitylog'),
(30,'Can change user activity log',8,'change_useractivitylog'),
(31,'Can delete user activity log',8,'delete_useractivitylog'),
(32,'Can view user activity log',8,'view_useractivitylog'),
(33,'Can add Dashboard Link',9,'add_dashboardlink'),
(34,'Can change Dashboard Link',9,'change_dashboardlink'),
(35,'Can delete Dashboard Link',9,'delete_dashboardlink'),
(36,'Can view Dashboard Link',9,'view_dashboardlink'),
(37,'Can add notification',10,'add_notification'),
(38,'Can change notification',10,'change_notification'),
(39,'Can delete notification',10,'delete_notification'),
(40,'Can view notification',10,'view_notification'),
(41,'Can add thread',12,'add_thread'),
(42,'Can change thread',12,'change_thread'),
(43,'Can delete thread',12,'delete_thread'),
(44,'Can view thread',12,'view_thread'),
(45,'Can add chat message',11,'add_chatmessage'),
(46,'Can change chat message',11,'change_chatmessage'),
(47,'Can delete chat message',11,'delete_chatmessage'),
(48,'Can view chat message',11,'view_chatmessage'),
(49,'Can add Error Code',13,'add_errorcode'),
(50,'Can change Error Code',13,'change_errorcode'),
(51,'Can delete Error Code',13,'delete_errorcode'),
(52,'Can view Error Code',13,'view_errorcode'),
(53,'Can add Folder',14,'add_folder'),
(54,'Can change Folder',14,'change_folder'),
(55,'Can delete Folder',14,'delete_folder'),
(56,'Can view Folder',14,'view_folder'),
(57,'Can add Media File',15,'add_mediafile'),
(58,'Can change Media File',15,'change_mediafile'),
(59,'Can delete Media File',15,'delete_mediafile'),
(60,'Can view Media File',15,'view_mediafile'),
(61,'Can add Model Name',17,'add_modelname'),
(62,'Can change Model Name',17,'change_modelname'),
(63,'Can delete Model Name',17,'delete_modelname'),
(64,'Can view Model Name',17,'view_modelname'),
(65,'Can add Subreddit',19,'add_subredditlist'),
(66,'Can change Subreddit',19,'change_subredditlist'),
(67,'Can delete Subreddit',19,'delete_subredditlist'),
(68,'Can view Subreddit',19,'view_subredditlist'),
(69,'Can add Video Category',20,'add_videocategory'),
(70,'Can change Video Category',20,'change_videocategory'),
(71,'Can delete Video Category',20,'delete_videocategory'),
(72,'Can view Video Category',20,'view_videocategory'),
(73,'Can add Media Stat',16,'add_mediastat'),
(74,'Can change Media Stat',16,'change_mediastat'),
(75,'Can delete Media Stat',16,'delete_mediastat'),
(76,'Can view Media Stat',16,'view_mediastat'),
(77,'Can add Model Record',18,'add_modelrecord'),
(78,'Can change Model Record',18,'change_modelrecord'),
(79,'Can delete Model Record',18,'delete_modelrecord'),
(80,'Can view Model Record',18,'view_modelrecord'),
(81,'Can add Video Link',21,'add_videolink'),
(82,'Can change Video Link',21,'change_videolink'),
(83,'Can delete Video Link',21,'delete_videolink'),
(84,'Can view Video Link',21,'view_videolink'),
(85,'Can add Token',22,'add_token'),
(86,'Can change Token',22,'change_token'),
(87,'Can delete Token',22,'delete_token'),
(88,'Can view Token',22,'view_token'),
(89,'Can add Token',23,'add_tokenproxy'),
(90,'Can change Token',23,'change_tokenproxy'),
(91,'Can delete Token',23,'delete_tokenproxy'),
(92,'Can view Token',23,'view_tokenproxy'),
(93,'Can add tag',24,'add_tag'),
(94,'Can change tag',24,'change_tag'),
(95,'Can delete tag',24,'delete_tag'),
(96,'Can view tag',24,'view_tag'),
(97,'Can add tagged item',25,'add_taggeditem'),
(98,'Can change tagged item',25,'change_taggeditem'),
(99,'Can delete tagged item',25,'delete_taggeditem'),
(100,'Can view tagged item',25,'view_taggeditem');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES
(1,'pbkdf2_sha256$1200000$qk5pCHAJXd8Agt3Gsfg2rn$xImcrizW9arokHKsdtcC7K03Kc2IMeiWVjtrw19tplg=',NULL,1,'admin','Admin','User','admin@projectr.local',1,1,'2025-12-06 15:31:53.568471'),
(2,'pbkdf2_sha256$1200000$wp1nT5GZpZHT0GhSxEr5fz$D+zaWwlYYvpcX0R4Wsmb0baVmtcCA+HZEN+gkOanQmQ=',NULL,0,'user726','User','726','user726@example.com',0,1,'2025-12-06 15:31:54.288723'),
(3,'pbkdf2_sha256$1200000$kHqe1wemee9kjZA6yB4XLe$QWQ+JSON6OJLhdgBaTyOUs01i8zPOLC1MsxlLeK6ZVU=',NULL,0,'user980','User','980','user980@example.com',0,1,'2025-12-06 15:31:54.998364'),
(4,'pbkdf2_sha256$1200000$gzMP8VV2Wmf6DiTyxKxtd7$lR4GayP7lJBLJhbbhzofB4R0EInIBmYlsPnKsBeXC7g=',NULL,0,'user630','User','630','user630@example.com',0,1,'2025-12-06 15:31:55.719444'),
(5,'pbkdf2_sha256$1200000$pDqj12hdhOplOpapryDEg8$i84N9tHX3G+trzmQM5+xOXsZcbIHdcwuG29Z7irDRlM=',NULL,0,'user643','User','643','user643@example.com',0,1,'2025-12-06 15:31:56.434600'),
(6,'pbkdf2_sha256$1200000$qKNOxVnCXn3bhQozgc0fwY$rjQm8RIvpYvacSiUy8eFv5VEkyfNoVehFyKkRCyz4Dc=',NULL,0,'user282','User','282','user282@example.com',0,1,'2025-12-06 15:31:57.232289');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES
(1,2,1),
(2,3,1),
(3,4,1),
(4,5,1),
(5,6,1);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_chatmessage`
--

DROP TABLE IF EXISTS `chat_chatmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_chatmessage` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `message` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  `thread_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `chat_chatmessage_user_id_fa615e65_fk_auth_user_id` (`user_id`),
  KEY `chat_chatmessage_thread_id_0986d8f2_fk_chat_thread_id` (`thread_id`),
  CONSTRAINT `chat_chatmessage_thread_id_0986d8f2_fk_chat_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `chat_thread` (`id`),
  CONSTRAINT `chat_chatmessage_user_id_fa615e65_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_chatmessage`
--

LOCK TABLES `chat_chatmessage` WRITE;
/*!40000 ALTER TABLE `chat_chatmessage` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_chatmessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_thread`
--

DROP TABLE IF EXISTS `chat_thread`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_thread` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `updated` datetime(6) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `receiver_id` int(11) DEFAULT NULL,
  `sender_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `chat_thread_sender_id_receiver_id_25be7632_uniq` (`sender_id`,`receiver_id`),
  KEY `chat_thread_receiver_id_4fd75b0e_fk_auth_user_id` (`receiver_id`),
  CONSTRAINT `chat_thread_receiver_id_4fd75b0e_fk_auth_user_id` FOREIGN KEY (`receiver_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `chat_thread_sender_id_a945ba53_fk_auth_user_id` FOREIGN KEY (`sender_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_thread`
--

LOCK TABLES `chat_thread` WRITE;
/*!40000 ALTER TABLE `chat_thread` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_thread` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `common_notification`
--

DROP TABLE IF EXISTS `common_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `common_notification` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `message` varchar(255) NOT NULL,
  `notification_type` varchar(20) NOT NULL,
  `link` varchar(255) DEFAULT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `recipient_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `common_notification_recipient_id_18cd2d72_fk_auth_user_id` (`recipient_id`),
  CONSTRAINT `common_notification_recipient_id_18cd2d72_fk_auth_user_id` FOREIGN KEY (`recipient_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `common_notification`
--

LOCK TABLES `common_notification` WRITE;
/*!40000 ALTER TABLE `common_notification` DISABLE KEYS */;
INSERT INTO `common_notification` VALUES
(1,'Welcome to ProjectR, admin! We are excited to have you on board.','success',NULL,0,'2025-12-06 15:31:54.255069',1),
(2,'Don\'t forget to complete your profile (add a photo and bio)!','info','/account/settings/',0,'2025-12-06 15:31:54.276861',1),
(3,'Welcome to ProjectR, user726! We are excited to have you on board.','success',NULL,0,'2025-12-06 15:31:54.984661',2),
(4,'Don\'t forget to complete your profile (add a photo and bio)!','info','/account/settings/',0,'2025-12-06 15:31:54.987333',2),
(5,'Welcome to ProjectR, user980! We are excited to have you on board.','success',NULL,0,'2025-12-06 15:31:55.699867',3),
(6,'Don\'t forget to complete your profile (add a photo and bio)!','info','/account/settings/',0,'2025-12-06 15:31:55.703464',3),
(7,'Welcome to ProjectR, user630! We are excited to have you on board.','success',NULL,0,'2025-12-06 15:31:56.418213',4),
(8,'Don\'t forget to complete your profile (add a photo and bio)!','info','/account/settings/',0,'2025-12-06 15:31:56.421420',4),
(9,'Welcome to ProjectR, user643! We are excited to have you on board.','success',NULL,0,'2025-12-06 15:31:57.217417',5),
(10,'Don\'t forget to complete your profile (add a photo and bio)!','info','/account/settings/',0,'2025-12-06 15:31:57.220410',5),
(11,'Welcome to ProjectR, user282! We are excited to have you on board.','success',NULL,0,'2025-12-06 15:31:58.004606',6),
(12,'Don\'t forget to complete your profile (add a photo and bio)!','info','/account/settings/',0,'2025-12-06 15:31:58.007728',6);
/*!40000 ALTER TABLE `common_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_dashboardlink`
--

DROP TABLE IF EXISTS `dashboard_dashboardlink`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashboard_dashboardlink` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `url` varchar(200) NOT NULL,
  `icon` varchar(50) NOT NULL,
  `order` int(10) unsigned NOT NULL CHECK (`order` >= 0),
  `open_in_new_tab` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_dashboardlink`
--

LOCK TABLES `dashboard_dashboardlink` WRITE;
/*!40000 ALTER TABLE `dashboard_dashboardlink` DISABLE KEYS */;
/*!40000 ALTER TABLE `dashboard_dashboardlink` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_dashboardlink_groups`
--

DROP TABLE IF EXISTS `dashboard_dashboardlink_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashboard_dashboardlink_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `dashboardlink_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dashboard_dashboardlink__dashboardlink_id_group_i_ca6ea171_uniq` (`dashboardlink_id`,`group_id`),
  KEY `dashboard_dashboardl_group_id_a297f783_fk_auth_grou` (`group_id`),
  CONSTRAINT `dashboard_dashboardl_dashboardlink_id_69769f91_fk_dashboard` FOREIGN KEY (`dashboardlink_id`) REFERENCES `dashboard_dashboardlink` (`id`),
  CONSTRAINT `dashboard_dashboardl_group_id_a297f783_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_dashboardlink_groups`
--

LOCK TABLES `dashboard_dashboardlink_groups` WRITE;
/*!40000 ALTER TABLE `dashboard_dashboardlink_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `dashboard_dashboardlink_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES
(7,'account','profile'),
(8,'account','useractivitylog'),
(1,'admin','logentry'),
(2,'auth','group'),
(3,'auth','permission'),
(4,'auth','user'),
(22,'authtoken','token'),
(23,'authtoken','tokenproxy'),
(11,'chat','chatmessage'),
(12,'chat','thread'),
(10,'common','notification'),
(5,'contenttypes','contenttype'),
(9,'dashboard','dashboardlink'),
(13,'media_manager','errorcode'),
(14,'media_manager','folder'),
(15,'media_manager','mediafile'),
(16,'media_manager','mediastat'),
(17,'media_manager','modelname'),
(18,'media_manager','modelrecord'),
(19,'media_manager','subredditlist'),
(20,'media_manager','videocategory'),
(21,'media_manager','videolink'),
(6,'sessions','session'),
(24,'taggit','tag'),
(25,'taggit','taggeditem');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2025-12-06 15:24:31.912134'),
(2,'auth','0001_initial','2025-12-06 15:24:32.435184'),
(3,'account','0001_initial','2025-12-06 15:24:32.552695'),
(4,'admin','0001_initial','2025-12-06 15:24:32.651023'),
(5,'admin','0002_logentry_remove_auto_add','2025-12-06 15:24:32.665156'),
(6,'admin','0003_logentry_add_action_flag_choices','2025-12-06 15:24:32.681202'),
(7,'contenttypes','0002_remove_content_type_name','2025-12-06 15:24:32.771139'),
(8,'auth','0002_alter_permission_name_max_length','2025-12-06 15:24:32.815832'),
(9,'auth','0003_alter_user_email_max_length','2025-12-06 15:24:32.847888'),
(10,'auth','0004_alter_user_username_opts','2025-12-06 15:24:32.858660'),
(11,'auth','0005_alter_user_last_login_null','2025-12-06 15:24:32.907288'),
(12,'auth','0006_require_contenttypes_0002','2025-12-06 15:24:32.909865'),
(13,'auth','0007_alter_validators_add_error_messages','2025-12-06 15:24:32.922032'),
(14,'auth','0008_alter_user_username_max_length','2025-12-06 15:24:32.957686'),
(15,'auth','0009_alter_user_last_name_max_length','2025-12-06 15:24:32.990949'),
(16,'auth','0010_alter_group_name_max_length','2025-12-06 15:24:33.022312'),
(17,'auth','0011_update_proxy_permissions','2025-12-06 15:24:33.033093'),
(18,'auth','0012_alter_user_first_name_max_length','2025-12-06 15:24:33.067495'),
(19,'authtoken','0001_initial','2025-12-06 15:24:33.132322'),
(20,'authtoken','0002_auto_20160226_1747','2025-12-06 15:24:33.169289'),
(21,'authtoken','0003_tokenproxy','2025-12-06 15:24:33.173390'),
(22,'authtoken','0004_alter_tokenproxy_options','2025-12-06 15:24:33.180277'),
(23,'chat','0001_initial','2025-12-06 15:24:33.412692'),
(24,'common','0001_initial','2025-12-06 15:24:33.482978'),
(25,'dashboard','0001_initial','2025-12-06 15:24:33.633780'),
(26,'taggit','0001_initial','2025-12-06 15:24:33.791082'),
(27,'taggit','0002_auto_20150616_2121','2025-12-06 15:24:33.832051'),
(28,'taggit','0003_taggeditem_add_unique_index','2025-12-06 15:24:33.871528'),
(29,'taggit','0004_alter_taggeditem_content_type_alter_taggeditem_tag','2025-12-06 15:24:33.913676'),
(30,'taggit','0005_auto_20220424_2025','2025-12-06 15:24:33.919905'),
(31,'taggit','0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx','2025-12-06 15:24:34.039862'),
(32,'media_manager','0001_initial','2025-12-06 15:24:34.650204'),
(33,'sessions','0001_initial','2025-12-06 15:24:34.698562');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mm_error_codes`
--

DROP TABLE IF EXISTS `mm_error_codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `mm_error_codes` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `description` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `last_updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mm_error_codes`
--

LOCK TABLES `mm_error_codes` WRITE;
/*!40000 ALTER TABLE `mm_error_codes` DISABLE KEYS */;
/*!40000 ALTER TABLE `mm_error_codes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mm_folders`
--

DROP TABLE IF EXISTS `mm_folders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `mm_folders` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `parent` int(11) DEFAULT NULL,
  `files_count` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `last_updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mm_folders`
--

LOCK TABLES `mm_folders` WRITE;
/*!40000 ALTER TABLE `mm_folders` DISABLE KEYS */;
/*!40000 ALTER TABLE `mm_folders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mm_media_files`
--

DROP TABLE IF EXISTS `mm_media_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `mm_media_files` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(255) DEFAULT NULL,
  `original_url` varchar(1200) NOT NULL,
  `secondary_url` varchar(2500) DEFAULT NULL,
  `thumbnail_url` varchar(500) DEFAULT NULL,
  `thumbnail_drive` varchar(500) DEFAULT NULL,
  `media_type` varchar(255) DEFAULT NULL,
  `post_url` varchar(255) DEFAULT NULL,
  `filesize_bytes` bigint(20) DEFAULT NULL,
  `filesize` varchar(50) DEFAULT NULL,
  `post_title` varchar(255) DEFAULT NULL,
  `post_id` varchar(20) DEFAULT NULL,
  `description` longtext DEFAULT NULL,
  `downloaded` tinyint(1) NOT NULL,
  `synced` tinyint(1) NOT NULL,
  `error_code` int(11) NOT NULL,
  `starred` tinyint(1) NOT NULL,
  `drive_file_id` varchar(255) DEFAULT NULL,
  `drive_id` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `last_updated_at` datetime(6) NOT NULL,
  `folder_id` bigint(20) NOT NULL,
  `model_id` bigint(20) DEFAULT NULL,
  `subreddit_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `original_url` (`original_url`) USING HASH,
  KEY `mm_media_files_model_id_85642abc_fk_mm_model_names_id` (`model_id`),
  KEY `mm_media_files_subreddit_id_75f7db50_fk_mm_subreddits_list_id` (`subreddit_id`),
  KEY `mm_media_files_folder_id_81753b82_fk_mm_folders_id` (`folder_id`),
  CONSTRAINT `mm_media_files_folder_id_81753b82_fk_mm_folders_id` FOREIGN KEY (`folder_id`) REFERENCES `mm_folders` (`id`),
  CONSTRAINT `mm_media_files_model_id_85642abc_fk_mm_model_names_id` FOREIGN KEY (`model_id`) REFERENCES `mm_model_names` (`id`),
  CONSTRAINT `mm_media_files_subreddit_id_75f7db50_fk_mm_subreddits_list_id` FOREIGN KEY (`subreddit_id`) REFERENCES `mm_subreddits_list` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mm_media_files`
--

LOCK TABLES `mm_media_files` WRITE;
/*!40000 ALTER TABLE `mm_media_files` DISABLE KEYS */;
/*!40000 ALTER TABLE `mm_media_files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mm_media_stats`
--

DROP TABLE IF EXISTS `mm_media_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `mm_media_stats` (
  `media_file_id` bigint(20) NOT NULL,
  `total_views` int(11) NOT NULL,
  `duration` int(11) NOT NULL,
  `last_visited` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`media_file_id`),
  CONSTRAINT `mm_media_stats_media_file_id_8a155b2b_fk_mm_media_files_id` FOREIGN KEY (`media_file_id`) REFERENCES `mm_media_files` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mm_media_stats`
--

LOCK TABLES `mm_media_stats` WRITE;
/*!40000 ALTER TABLE `mm_media_stats` DISABLE KEYS */;
/*!40000 ALTER TABLE `mm_media_stats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mm_model_names`
--

DROP TABLE IF EXISTS `mm_model_names`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `mm_model_names` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `suffix` varchar(255) DEFAULT NULL,
  `description` longtext DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `picture` varchar(512) DEFAULT NULL,
  `search_text` varchar(255) DEFAULT NULL,
  `folder` int(11) DEFAULT NULL,
  `uploads_folder` int(11) DEFAULT NULL,
  `files_count` int(11) DEFAULT NULL,
  `drive_no` int(11) NOT NULL,
  `drive_folder_id` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `last_updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mm_model_names`
--

LOCK TABLES `mm_model_names` WRITE;
/*!40000 ALTER TABLE `mm_model_names` DISABLE KEYS */;
/*!40000 ALTER TABLE `mm_model_names` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mm_model_records`
--

DROP TABLE IF EXISTS `mm_model_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `mm_model_records` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `story` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mm_model_records`
--

LOCK TABLES `mm_model_records` WRITE;
/*!40000 ALTER TABLE `mm_model_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `mm_model_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mm_model_records_associated_models`
--

DROP TABLE IF EXISTS `mm_model_records_associated_models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `mm_model_records_associated_models` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `modelrecord_id` bigint(20) NOT NULL,
  `modelname_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mm_model_records_associa_modelrecord_id_modelname_edafcf66_uniq` (`modelrecord_id`,`modelname_id`),
  KEY `mm_model_records_ass_modelname_id_2f99ad95_fk_mm_model_` (`modelname_id`),
  CONSTRAINT `mm_model_records_ass_modelname_id_2f99ad95_fk_mm_model_` FOREIGN KEY (`modelname_id`) REFERENCES `mm_model_names` (`id`),
  CONSTRAINT `mm_model_records_ass_modelrecord_id_ca5eeeeb_fk_mm_model_` FOREIGN KEY (`modelrecord_id`) REFERENCES `mm_model_records` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mm_model_records_associated_models`
--

LOCK TABLES `mm_model_records_associated_models` WRITE;
/*!40000 ALTER TABLE `mm_model_records_associated_models` DISABLE KEYS */;
/*!40000 ALTER TABLE `mm_model_records_associated_models` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mm_subreddits_list`
--

DROP TABLE IF EXISTS `mm_subreddits_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `mm_subreddits_list` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `subreddit_name` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `subreddit_url` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `last_updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mm_subreddits_list`
--

LOCK TABLES `mm_subreddits_list` WRITE;
/*!40000 ALTER TABLE `mm_subreddits_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `mm_subreddits_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mm_video_categories`
--

DROP TABLE IF EXISTS `mm_video_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `mm_video_categories` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mm_video_categories`
--

LOCK TABLES `mm_video_categories` WRITE;
/*!40000 ALTER TABLE `mm_video_categories` DISABLE KEYS */;
/*!40000 ALTER TABLE `mm_video_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mm_video_links`
--

DROP TABLE IF EXISTS `mm_video_links`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `mm_video_links` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(500) DEFAULT NULL,
  `original_url` varchar(2000) NOT NULL,
  `thumbnail_url` varchar(1200) DEFAULT NULL,
  `comment` longtext DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `last_updated_at` datetime(6) NOT NULL,
  `category_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `original_url` (`original_url`) USING HASH,
  KEY `mm_video_links_category_id_0d4f97e0_fk_mm_video_categories_id` (`category_id`),
  CONSTRAINT `mm_video_links_category_id_0d4f97e0_fk_mm_video_categories_id` FOREIGN KEY (`category_id`) REFERENCES `mm_video_categories` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mm_video_links`
--

LOCK TABLES `mm_video_links` WRITE;
/*!40000 ALTER TABLE `mm_video_links` DISABLE KEYS */;
/*!40000 ALTER TABLE `mm_video_links` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `taggit_tag`
--

DROP TABLE IF EXISTS `taggit_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `taggit_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `slug` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taggit_tag`
--

LOCK TABLES `taggit_tag` WRITE;
/*!40000 ALTER TABLE `taggit_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `taggit_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `taggit_taggeditem`
--

DROP TABLE IF EXISTS `taggit_taggeditem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `taggit_taggeditem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `taggit_taggeditem_content_type_id_object_id_tag_id_4bb97a8e_uniq` (`content_type_id`,`object_id`,`tag_id`),
  KEY `taggit_taggeditem_tag_id_f4f5b767_fk_taggit_tag_id` (`tag_id`),
  KEY `taggit_taggeditem_object_id_e2d7d1df` (`object_id`),
  KEY `taggit_tagg_content_8fc721_idx` (`content_type_id`,`object_id`),
  CONSTRAINT `taggit_taggeditem_content_type_id_9957a03c_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `taggit_taggeditem_tag_id_f4f5b767_fk_taggit_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `taggit_tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taggit_taggeditem`
--

LOCK TABLES `taggit_taggeditem` WRITE;
/*!40000 ALTER TABLE `taggit_taggeditem` DISABLE KEYS */;
/*!40000 ALTER TABLE `taggit_taggeditem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'projectr_db'
--

--
-- Dumping routines for database 'projectr_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-06 15:33:49
