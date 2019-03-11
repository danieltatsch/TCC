-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: TCC
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.18.04.2

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cenario`
--

LOCK TABLES `Cenario` WRITE;
/*!40000 ALTER TABLE `Cenario` DISABLE KEYS */;
INSERT INTO `Cenario` VALUES (1,'Sala'),(2,'teste');
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
INSERT INTO `CenarioSetor` VALUES (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9);
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Gateway`
--

LOCK TABLES `Gateway` WRITE;
/*!40000 ALTER TABLE `Gateway` DISABLE KEYS */;
INSERT INTO `Gateway` VALUES (1,'mac1','cristaleira'),(2,'mac2','sofa'),(3,'mac3','telefone'),(4,'mac4','xablau');
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8 COMMENT='\n';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `GerMedicao`
--

LOCK TABLES `GerMedicao` WRITE;
/*!40000 ALTER TABLE `GerMedicao` DISABLE KEYS */;
INSERT INTO `GerMedicao` VALUES (15,'2019-03-10 21:23:03',NULL,1,9);
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
  PRIMARY KEY (`idMedicao`),
  KEY `fk_Medicao_Gateway1_idx` (`idGateway`),
  KEY `fk_Medicao_Nodo1_idx` (`idNodo`),
  KEY `fk_Medicao_GerMedicao1_idx` (`idGerMedicao`),
  CONSTRAINT `fk_Medicao_Gateway1` FOREIGN KEY (`idGateway`) REFERENCES `Gateway` (`idGateway`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Medicao_GerMedicao1` FOREIGN KEY (`idGerMedicao`) REFERENCES `GerMedicao` (`idGerMedicao`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Medicao_Nodo1` FOREIGN KEY (`idNodo`) REFERENCES `Nodo` (`idNodo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Medicao`
--

LOCK TABLES `Medicao` WRITE;
/*!40000 ALTER TABLE `Medicao` DISABLE KEYS */;
INSERT INTO `Medicao` VALUES (1,-80,'2019-03-10 21:24:23',1,1,15),(2,-85,'2019-03-10 21:24:47',1,1,15),(3,-85,'2019-03-10 21:24:48',1,1,15),(4,-85,'2019-03-10 21:24:49',1,1,15),(5,-85,'2019-03-10 21:24:49',1,1,15),(6,-82,'2019-03-10 21:24:54',1,1,15),(7,-82,'2019-03-10 21:24:54',1,1,15),(8,-82,'2019-03-10 21:24:55',1,1,15),(9,-82,'2019-03-10 21:24:55',1,1,15);
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Nodo`
--

LOCK TABLES `Nodo` WRITE;
/*!40000 ALTER TABLE `Nodo` DISABLE KEYS */;
INSERT INTO `Nodo` VALUES (1,'macNodo1'),(2,'macNodo2'),(3,'macNodo3'),(5,'macNodo4');
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Setor`
--

LOCK TABLES `Setor` WRITE;
/*!40000 ALTER TABLE `Setor` DISABLE KEYS */;
INSERT INTO `Setor` VALUES (1,'Telefone'),(2,'mesa'),(3,'cristaleira'),(4,'poltrona1'),(5,'poltrona2'),(6,'corredor'),(7,'televisao'),(8,'centro'),(9,'sofa');
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

-- Dump completed on 2019-03-10 21:32:21
