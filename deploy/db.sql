-- MySQL dump 10.13  Distrib 5.1.49, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: w3fu
-- ------------------------------------------------------
-- Server version	5.1.49-1ubuntu8.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `assocs`
--

DROP TABLE IF EXISTS `assocs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assocs` (
  `url` varchar(255) NOT NULL,
  `handle` varchar(255) NOT NULL,
  `secret` varbinary(255) NOT NULL,
  `issued` int(10) unsigned NOT NULL,
  `lifetime` int(10) unsigned NOT NULL,
  `type` varchar(64) NOT NULL,
  PRIMARY KEY (`url`,`handle`)
) ENGINE=MEMORY DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assocs`
--

LOCK TABLES `assocs` WRITE;
/*!40000 ALTER TABLE `assocs` DISABLE KEYS */;
/*!40000 ALTER TABLE `assocs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firm`
--

DROP TABLE IF EXISTS `firm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firm` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `data` blob NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firm`
--

LOCK TABLES `firm` WRITE;
/*!40000 ALTER TABLE `firm` DISABLE KEYS */;
INSERT INTO `firm` VALUES (5,'{\"type\": 10, \"name\": \"Yandex\"}'),(7,'{\"type\": 10, \"name\": \"Apple\"}'),(8,'{\"type\": 10, \"name\": \"Yandex\"}'),(9,'{\"type\": 10, \"name\": \"Google\"}');
/*!40000 ALTER TABLE `firm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firm_generic`
--

DROP TABLE IF EXISTS `firm_generic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firm_generic` (
  `id` int(10) unsigned NOT NULL,
  `f1` int(10) unsigned NOT NULL,
  `f2` int(10) unsigned NOT NULL,
  `f3` int(10) unsigned NOT NULL,
  KEY `id` (`id`),
  KEY `f1` (`f1`),
  KEY `f2` (`f2`),
  KEY `f3` (`f3`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firm_generic`
--

LOCK TABLES `firm_generic` WRITE;
/*!40000 ALTER TABLE `firm_generic` DISABLE KEYS */;
INSERT INTO `firm_generic` VALUES (8,1,2,3),(9,1,2,3),(7,1,2,3);
/*!40000 ALTER TABLE `firm_generic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firm_special`
--

DROP TABLE IF EXISTS `firm_special`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firm_special` (
  `id` int(11) NOT NULL,
  `f4` varchar(255) NOT NULL,
  KEY `id` (`id`),
  KEY `f4` (`f4`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firm_special`
--

LOCK TABLES `firm_special` WRITE;
/*!40000 ALTER TABLE `firm_special` DISABLE KEYS */;
INSERT INTO `firm_special` VALUES (8,'Yandex'),(8,'Yandex'),(8,'Yandex'),(8,'Yandex'),(9,'Google'),(9,'Google'),(9,'Google'),(9,'Google'),(7,'Apple'),(7,'Apple'),(7,'Apple'),(7,'Apple');
/*!40000 ALTER TABLE `firm_special` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nonces`
--

DROP TABLE IF EXISTS `nonces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonces` (
  `url` varchar(255) NOT NULL,
  `timestamp` int(10) unsigned NOT NULL,
  `salt` char(40) NOT NULL,
  PRIMARY KEY (`url`,`timestamp`,`salt`)
) ENGINE=MEMORY DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nonces`
--

LOCK TABLES `nonces` WRITE;
/*!40000 ALTER TABLE `nonces` DISABLE KEYS */;
/*!40000 ALTER TABLE `nonces` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `session`
--

DROP TABLE IF EXISTS `session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `session` (
  `id` char(22) NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `expires` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `expires` (`expires`)
) ENGINE=MEMORY DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `session`
--

LOCK TABLES `session` WRITE;
/*!40000 ALTER TABLE `session` DISABLE KEYS */;
/*!40000 ALTER TABLE `session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `login` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'testuser','1234VfqPs7QDdc7FX1beaKKGLOtwLkE');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-04-01 18:16:59
