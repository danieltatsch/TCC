-- MySQL dump 10.13  Distrib 5.7.26, for Linux (x86_64)
--
-- Host: localhost    Database: TCC
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.18.04.1

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
-- Table structure for table `Cenario`
--

DROP TABLE IF EXISTS `Cenario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Cenario` (
  `idCenario` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) NOT NULL,
  PRIMARY KEY (`idCenario`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cenario`
--

LOCK TABLES `Cenario` WRITE;
/*!40000 ALTER TABLE `Cenario` DISABLE KEYS */;
INSERT INTO `Cenario` VALUES (1,'Sala'),(2,'teste'),(3,'auditorio'),(4,'sala11');
/*!40000 ALTER TABLE `Cenario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CenarioSetor`
--

DROP TABLE IF EXISTS `CenarioSetor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CenarioSetor` (
  `idCenario` int(11) NOT NULL,
  `idSetor` int(11) NOT NULL,
  PRIMARY KEY (`idCenario`,`idSetor`),
  KEY `fk_Cenario_has_Setor_Setor1_idx` (`idSetor`),
  CONSTRAINT `fk_Cenario_has_Setor_Cenario1` FOREIGN KEY (`idCenario`) REFERENCES `Cenario` (`idCenario`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Cenario_has_Setor_Setor1` FOREIGN KEY (`idSetor`) REFERENCES `Setor` (`idSetor`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CenarioSetor`
--

LOCK TABLES `CenarioSetor` WRITE;
/*!40000 ALTER TABLE `CenarioSetor` DISABLE KEYS */;
INSERT INTO `CenarioSetor` VALUES (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(3,10),(3,11),(3,12),(3,13),(4,14),(4,15),(4,16),(4,17),(3,18),(3,19),(3,20),(3,21),(3,22),(3,23),(3,24),(3,25),(3,26),(3,27),(3,28),(3,29),(3,30),(3,31),(3,32),(3,33),(3,34),(3,35),(3,36),(3,37),(3,38),(3,39),(3,40),(3,41);
/*!40000 ALTER TABLE `CenarioSetor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Gateway`
--

DROP TABLE IF EXISTS `Gateway`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Gateway` (
  `idGateway` int(11) NOT NULL AUTO_INCREMENT,
  `mac` varchar(45) NOT NULL,
  `lugar` varchar(45) NOT NULL,
  PRIMARY KEY (`idGateway`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Gateway`
--

LOCK TABLES `Gateway` WRITE;
/*!40000 ALTER TABLE `Gateway` DISABLE KEYS */;
INSERT INTO `Gateway` VALUES (1,'mac1','cristaleira'),(2,'mac2','sofa'),(3,'mac3','telefone'),(4,'mac4','xablau'),(5,'30:AE:A4:8B:D6:6C','mesa'),(7,'24:0A:C4:30:D9:00','televisao'),(8,'24:0A:C4:32:02:D4','pc');
/*!40000 ALTER TABLE `Gateway` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `GerMedicao`
--

DROP TABLE IF EXISTS `GerMedicao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GerMedicao` (
  `idGerMedicao` int(11) NOT NULL AUTO_INCREMENT,
  `inicio` datetime NOT NULL,
  `fim` datetime DEFAULT NULL,
  `idCenario` int(11) NOT NULL,
  `idSetor` int(11) NOT NULL,
  PRIMARY KEY (`idGerMedicao`),
  KEY `fk_GerMedicao_Cenario1_idx` (`idCenario`),
  KEY `fk_GerMedicao_Setor1_idx` (`idSetor`),
  CONSTRAINT `fk_GerMedicao_Cenario1` FOREIGN KEY (`idCenario`) REFERENCES `Cenario` (`idCenario`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_GerMedicao_Setor1` FOREIGN KEY (`idSetor`) REFERENCES `Setor` (`idSetor`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=utf8 COMMENT='\n';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `GerMedicao`
--

LOCK TABLES `GerMedicao` WRITE;
/*!40000 ALTER TABLE `GerMedicao` DISABLE KEYS */;
INSERT INTO `GerMedicao` VALUES (15,'2019-03-10 21:23:03','2019-03-13 21:21:43',1,9),(16,'2019-03-16 15:16:34','2019-03-16 15:22:30',1,2),(17,'2019-03-18 22:04:02','2019-03-18 22:05:53',1,9),(18,'2019-03-23 16:14:43','2019-03-23 19:34:33',1,2),(22,'2019-03-30 21:30:53','2019-05-22 12:24:57',1,2),(23,'2019-05-22 15:50:42','2019-05-22 18:00:00',3,10),(24,'2019-05-22 18:13:50','2019-05-22 19:00:53',3,10),(25,'2019-05-22 19:45:27','2019-05-22 20:17:23',3,10),(26,'2019-05-23 16:36:03','2019-05-23 17:10:07',3,10),(27,'2019-05-23 17:21:00','2019-05-23 17:50:37',3,10),(28,'2019-05-23 18:01:35','2019-05-23 18:41:49',3,11),(29,'2019-05-23 18:45:47','2019-05-23 19:19:33',3,11),(30,'2019-05-23 19:27:06','2019-05-23 20:03:06',3,11),(31,'2019-05-23 20:07:30','2019-05-23 20:41:56',3,11),(32,'2019-05-25 09:36:06','2019-05-25 11:32:36',4,14),(33,'2019-05-25 12:51:18','2019-05-25 13:35:48',3,11),(34,'2019-05-25 13:57:15','2019-05-25 15:28:01',3,11),(35,'2019-05-25 15:34:18','2019-05-25 17:05:06',3,12),(36,'2019-05-25 18:33:12','2019-05-25 19:48:29',3,12),(37,'2019-05-29 08:13:13','2019-05-29 12:18:09',3,11),(38,'2019-05-29 12:22:07','2019-05-29 12:48:00',3,11),(39,'2019-05-29 12:49:53','2019-05-29 13:15:06',3,10),(40,'2019-05-29 15:52:40','2019-05-29 17:12:38',3,10),(41,'2019-05-29 17:23:34','2019-05-29 17:51:44',3,12),(42,'2019-05-29 17:53:21','2019-05-29 20:57:30',3,12),(43,'2019-05-29 20:58:14','2019-05-29 21:46:57',3,12),(44,'2019-05-29 21:55:01','2019-05-29 22:16:15',3,12),(45,'2019-05-29 22:19:17','2019-05-30 10:44:06',3,13),(46,'2019-05-30 10:45:29','2019-05-30 11:26:41',3,13),(47,'2019-05-30 11:31:28','2019-05-30 11:57:10',3,13),(48,'2019-05-30 15:12:21','2019-05-30 15:36:05',3,18),(49,'2019-05-30 15:40:27','2019-05-30 16:44:55',3,19),(50,'2019-05-30 16:46:29','2019-05-30 17:24:36',3,19),(51,'2019-05-30 17:25:51','2019-05-30 17:57:07',3,19),(52,'2019-05-30 17:57:47','2019-05-30 18:59:21',3,19),(53,'2019-05-30 19:04:45','2019-05-30 19:24:51',3,19),(54,'2019-05-30 19:34:13','2019-06-01 12:28:01',3,20),(55,'2019-06-01 12:30:37','2019-06-01 12:56:34',3,20),(56,'2019-06-01 12:57:26','2019-06-01 13:18:45',3,20),(57,'2019-06-01 13:19:49','2019-06-01 14:39:00',3,20),(58,'2019-06-01 14:39:18','2019-06-01 15:56:35',3,21),(59,'2019-06-01 16:00:50','2019-06-01 16:48:56',3,21),(60,'2019-06-01 16:49:18','2019-06-01 17:21:36',3,38),(61,'2019-06-01 17:27:03','2019-06-01 17:52:40',3,38),(62,'2019-06-01 18:02:31','2019-06-01 18:28:54',3,39),(63,'2019-06-01 18:31:39','2019-06-02 11:18:55',3,40),(64,'2019-06-02 11:20:30','2019-06-02 12:01:21',3,40),(65,'2019-06-02 12:11:00','2019-06-02 13:43:16',3,41),(66,'2019-06-02 13:44:11','2019-06-02 14:06:25',3,41),(67,'2019-06-02 14:09:01','2019-06-02 14:30:39',3,41),(68,'2019-06-02 14:53:01','2019-06-02 15:16:32',3,37),(69,'2019-06-02 15:19:21','2019-06-02 16:52:31',3,36),(70,'2019-06-02 17:10:15','2019-06-02 17:54:56',3,35),(71,'2019-06-02 17:57:00','2019-06-02 18:19:25',3,35),(72,'2019-06-02 18:27:06','2019-06-02 18:46:31',3,35),(73,'2019-06-02 19:00:40','2019-06-02 19:48:37',3,34),(74,'2019-06-02 19:50:32','2019-06-02 20:12:59',3,34),(75,'2019-06-02 20:14:36','2019-06-05 08:43:10',3,34),(76,'2019-06-05 08:46:03','2019-06-05 09:20:32',3,33),(77,'2019-06-05 09:22:11','2019-06-05 09:48:14',3,32),(78,'2019-06-05 09:51:06','2019-06-05 10:16:14',3,31),(79,'2019-06-05 10:16:57','2019-06-05 10:40:48',3,31),(80,'2019-06-05 10:45:19','2019-06-05 11:40:36',3,30),(81,'2019-06-05 11:41:19','2019-06-05 12:44:53',3,30),(82,'2019-06-05 12:47:55','2019-06-05 13:33:47',3,30),(84,'2019-06-05 13:44:03','2019-06-05 14:05:29',3,26),(85,'2019-06-05 14:07:58','2019-06-05 14:35:43',3,27),(86,'2019-06-05 14:36:36','2019-06-05 16:14:23',3,27),(87,'2019-06-05 16:15:36','2019-06-05 16:35:30',3,27),(88,'2019-06-05 16:37:06','2019-06-05 17:57:52',3,27),(89,'2019-06-05 18:00:56','2019-06-05 18:26:12',3,28),(91,'2019-06-05 19:47:53','2019-06-05 20:12:03',3,29),(92,'2019-06-05 20:13:03','2019-06-05 20:32:29',3,29),(93,'2019-06-05 20:34:10','2019-06-05 21:35:23',3,25),(94,'2019-06-06 08:39:23','2019-06-06 10:03:26',3,25),(96,'2019-06-06 10:46:16','2019-06-06 11:31:41',3,24),(97,'2019-06-06 11:39:56','2019-06-06 12:52:08',3,23),(98,'2019-06-06 12:54:54','2019-06-06 14:10:18',3,23),(99,'2019-06-06 14:10:35','2019-06-06 14:27:32',3,23),(100,'2019-06-06 14:39:28','2019-06-06 15:06:23',3,22),(101,'2019-06-06 15:22:49','2019-06-06 15:58:50',3,35),(102,'2019-06-06 16:00:13','2019-06-06 17:10:36',3,36),(103,'2019-06-06 17:11:17','2019-06-06 17:35:32',3,37),(104,'2019-06-06 17:38:41','2019-06-08 12:03:16',3,38),(105,'2019-06-08 12:09:01','2019-06-08 12:29:01',3,38),(106,'2019-06-08 12:34:08','2019-06-08 12:56:00',3,38),(107,'2019-06-08 12:57:20',NULL,3,38);
/*!40000 ALTER TABLE `GerMedicao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Medicao`
--

DROP TABLE IF EXISTS `Medicao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Medicao` (
  `idMedicao` int(11) NOT NULL AUTO_INCREMENT,
  `rssi` int(11) NOT NULL,
  `data` datetime NOT NULL,
  `idGateway` int(11) NOT NULL,
  `idNodo` int(11) NOT NULL,
  `idGerMedicao` int(11) NOT NULL,
  `count` int(11) NOT NULL,
  PRIMARY KEY (`idMedicao`),
  KEY `fk_Medicao_Gateway1_idx` (`idGateway`),
  KEY `fk_Medicao_Nodo1_idx` (`idNodo`),
  KEY `fk_Medicao_GerMedicao1_idx` (`idGerMedicao`),
  CONSTRAINT `fk_Medicao_Gateway1` FOREIGN KEY (`idGateway`) REFERENCES `Gateway` (`idGateway`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Medicao_GerMedicao1` FOREIGN KEY (`idGerMedicao`) REFERENCES `GerMedicao` (`idGerMedicao`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Medicao_Nodo1` FOREIGN KEY (`idNodo`) REFERENCES `Nodo` (`idNodo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Medicao`
--

LOCK TABLES `Medicao` WRITE;
/*!40000 ALTER TABLE `Medicao` DISABLE KEYS */;
/*!40000 ALTER TABLE `Medicao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Nodo`
--

DROP TABLE IF EXISTS `Nodo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Nodo` (
  `idNodo` int(11) NOT NULL AUTO_INCREMENT,
  `mac` varchar(45) NOT NULL,
  PRIMARY KEY (`idNodo`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Nodo`
--

LOCK TABLES `Nodo` WRITE;
/*!40000 ALTER TABLE `Nodo` DISABLE KEYS */;
INSERT INTO `Nodo` VALUES (1,'macNodo1'),(2,'macNodo2'),(3,'macNodo3'),(5,'macNodo4'),(6,'00:15:85:14:9c:09'),(7,'C8:FD:19:07:F2:29');
/*!40000 ALTER TABLE `Nodo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Setor`
--

DROP TABLE IF EXISTS `Setor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Setor` (
  `idSetor` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) NOT NULL,
  PRIMARY KEY (`idSetor`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Setor`
--

LOCK TABLES `Setor` WRITE;
/*!40000 ALTER TABLE `Setor` DISABLE KEYS */;
INSERT INTO `Setor` VALUES (1,'Telefone'),(2,'mesa'),(3,'cristaleira'),(4,'poltrona1'),(5,'poltrona2'),(6,'corredor'),(7,'televisao'),(8,'centro'),(9,'sofa'),(10,'c1_s1'),(11,'c1_s2'),(12,'c1_s3'),(13,'c1_s4'),(14,'sala11_c1_s1'),(15,'sala11_c1_s2'),(16,'sala11_c1_s3'),(17,'sala11_c1_s4'),(18,'c2_s21'),(19,'c2_s22'),(20,'c2_s23'),(21,'c2_s24'),(22,'c2_s1'),(23,'c2_s2'),(24,'c2_s3'),(25,'c2_s4'),(26,'c2_s5'),(27,'c2_s6'),(28,'c2_s7'),(29,'c2_s8'),(30,'c2_s9'),(31,'c2_s10'),(32,'c2_s11'),(33,'c2_s12'),(34,'c2_s13'),(35,'c2_s14'),(36,'c2_s15'),(37,'c2_s16'),(38,'c2_s17'),(39,'c2_s18'),(40,'c2_s19'),(41,'c2_s20');
/*!40000 ALTER TABLE `Setor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-07-11 20:01:39
