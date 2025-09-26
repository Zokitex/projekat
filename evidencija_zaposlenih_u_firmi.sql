CREATE DATABASE  IF NOT EXISTS `evidencija_zaposlenih_u_firmi` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `evidencija_zaposlenih_u_firmi`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: evidencija_zaposlenih_u_firmi
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `korisnici`
--

DROP TABLE IF EXISTS `korisnici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `korisnici` (
  `korisnik_id` int NOT NULL AUTO_INCREMENT,
  `korisnicko_ime` varchar(50) NOT NULL,
  `lozinka` varchar(255) NOT NULL,
  `uloga` enum('HR','Zaposleni') NOT NULL,
  PRIMARY KEY (`korisnik_id`),
  UNIQUE KEY `korisnicko_ime` (`korisnicko_ime`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `korisnici`
--

LOCK TABLES `korisnici` WRITE;
/*!40000 ALTER TABLE `korisnici` DISABLE KEYS */;
INSERT INTO `korisnici` VALUES (1,'admin_hr','scrypt:32768:8:1$Svn6Tz483FfQSBNX$2b828ce0c3994cca31faaee03b53bb8744b4cd56b7064e7854e70f4adce771bae468405d3a2897d2e5965d9f37afba5e8334bea81fcc823bb5f17f70086407b5','HR'),(2,'m.radovanovic','scrypt:32768:8:1$XnzE1WvekFRwnEj2$82ae03b5bd6c86d20e8bb26f026c7386fc29396e568a87717e6dd0491a36f4d964227a4affe5a3811ccb3540bc02edaed1ee5a3ea420ec41957a2424197e5bb6','Zaposleni'),(3,'a.jovanovic','scrypt:32768:8:1$5gvESj8Akig54GIa$b1d1fc6d2fb1307660b4fd6924a141df40f8e9db2cfb470a16241a2e1726c0efe658f1be882dbeb553f39a8da73574d9f534ab1850c935e5d3db9fa75fa2a0da','Zaposleni'),(4,'da','scrypt:32768:8:1$3FS44uRfPxRhNu9L$9839ffec061515531c1d117d49f0f8445ae52be28aa046c066a9319f70720c99e68ffaca27454672d8295b25d4b60b5ceb861d5e67d66ff9cb8a71e85eea4e4a','Zaposleni');
/*!40000 ALTER TABLE `korisnici` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prisustvo`
--

DROP TABLE IF EXISTS `prisustvo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prisustvo` (
  `prisustvo_id` int NOT NULL AUTO_INCREMENT,
  `zaposleni_id` int DEFAULT NULL,
  `datum` date NOT NULL,
  `vreme_dolaska` time DEFAULT NULL,
  `vreme_odlaska` time DEFAULT NULL,
  `status` enum('Prisutan','Odsutan','Opravdano') DEFAULT 'Prisutan',
  PRIMARY KEY (`prisustvo_id`),
  KEY `zaposleni_id` (`zaposleni_id`),
  CONSTRAINT `prisustvo_ibfk_1` FOREIGN KEY (`zaposleni_id`) REFERENCES `zaposleni` (`zaposleni_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prisustvo`
--

LOCK TABLES `prisustvo` WRITE;
/*!40000 ALTER TABLE `prisustvo` DISABLE KEYS */;
INSERT INTO `prisustvo` VALUES (1,2,'2025-09-12','08:00:00','16:00:00','Prisutan'),(2,3,'2025-09-12','08:15:00','15:45:00','Prisutan'),(3,2,'2025-09-13',NULL,NULL,'Odsutan');
/*!40000 ALTER TABLE `prisustvo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zahtevi_za_odmor`
--

DROP TABLE IF EXISTS `zahtevi_za_odmor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zahtevi_za_odmor` (
  `zahtev_id` int NOT NULL AUTO_INCREMENT,
  `zaposleni_id` int DEFAULT NULL,
  `datum_od` date NOT NULL,
  `datum_do` date NOT NULL,
  `razlog` text,
  `status` enum('Na čekanju','Odobreno','Odbijeno','Otkazano') DEFAULT 'Na čekanju',
  `rok_za_otkazivanje` date DEFAULT NULL,
  `datum_podnosenja` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`zahtev_id`),
  KEY `zaposleni_id` (`zaposleni_id`),
  CONSTRAINT `zahtevi_za_odmor_ibfk_1` FOREIGN KEY (`zaposleni_id`) REFERENCES `zaposleni` (`zaposleni_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zahtevi_za_odmor`
--

LOCK TABLES `zahtevi_za_odmor` WRITE;
/*!40000 ALTER TABLE `zahtevi_za_odmor` DISABLE KEYS */;
INSERT INTO `zahtevi_za_odmor` VALUES (1,2,'2025-09-20','2025-09-25','Porodični odmor','Na čekanju','2025-09-18','2025-09-26 14:01:43'),(2,3,'2025-10-05','2025-10-10','Privatni razlozi','Odobreno','2025-10-03','2025-09-26 14:01:43'),(3,2,'2025-11-01','2025-11-03','Zdravstveni razlozi','Otkazano','2025-10-30','2025-09-26 14:01:43');
/*!40000 ALTER TABLE `zahtevi_za_odmor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zaposleni`
--

DROP TABLE IF EXISTS `zaposleni`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zaposleni` (
  `zaposleni_id` int NOT NULL AUTO_INCREMENT,
  `korisnik_id` int DEFAULT NULL,
  `ime` varchar(50) DEFAULT NULL,
  `prezime` varchar(50) DEFAULT NULL,
  `pozicija` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `datum_zaposlenja` date DEFAULT NULL,
  PRIMARY KEY (`zaposleni_id`),
  UNIQUE KEY `email` (`email`),
  KEY `korisnik_id` (`korisnik_id`),
  CONSTRAINT `zaposleni_ibfk_1` FOREIGN KEY (`korisnik_id`) REFERENCES `korisnici` (`korisnik_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zaposleni`
--

LOCK TABLES `zaposleni` WRITE;
/*!40000 ALTER TABLE `zaposleni` DISABLE KEYS */;
INSERT INTO `zaposleni` VALUES (1,1,'Jovana','Marković','HR Menadžer','jovana.markovic@firma.rs','2023-06-15'),(2,2,'Milan','Radovanović','Programer','milan.radovanovic@firma.rs','2024-01-10'),(3,3,'Ana','Jovanović','Dizajner','ana.jovanovic@firma.rs','2022-09-01'),(4,4,'fgdf','gdf','fdsf','dfs@fdsgf.com','2025-09-26');
/*!40000 ALTER TABLE `zaposleni` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-26 16:18:20
