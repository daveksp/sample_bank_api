# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.32)
# Database: bank
# Generation Time: 2021-01-12 01:31:07 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table contas
# ------------------------------------------------------------

DROP TABLE IF EXISTS `contas`;

CREATE TABLE `contas` (
  `idConta` int(11) NOT NULL AUTO_INCREMENT,
  `idPessoa` int(11) NOT NULL,
  `saldo` decimal(10,2) DEFAULT NULL,
  `limiteSaqueDiario` decimal(10,2) DEFAULT NULL,
  `flagAtivo` tinyint(1) DEFAULT NULL,
  `dataCriacao` datetime NOT NULL,
  `tipoConta` enum('individual','company') NOT NULL,
  PRIMARY KEY (`idConta`),
  KEY `idPessoa` (`idPessoa`),
  CONSTRAINT `contas_ibfk_1` FOREIGN KEY (`idPessoa`) REFERENCES `pessoas` (`idPessoa`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table pessoas
# ------------------------------------------------------------

DROP TABLE IF EXISTS `pessoas`;

CREATE TABLE `pessoas` (
  `idPessoa` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(60) NOT NULL,
  `cpf` varchar(14) NOT NULL,
  `dataNascimento` datetime NOT NULL,
  `email` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`idPessoa`),
  UNIQUE KEY `cpf` (`cpf`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table transacoes
# ------------------------------------------------------------

DROP TABLE IF EXISTS `transacoes`;

CREATE TABLE `transacoes` (
  `idTransacao` int(11) NOT NULL AUTO_INCREMENT,
  `idConta` int(11) DEFAULT NULL,
  `valor` decimal(10,2) DEFAULT NULL,
  `dataTransacao` datetime NOT NULL,
  `tipoTransacao` enum('deposit','withdraw') NOT NULL,
  `descricao` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`idTransacao`),
  KEY `idConta` (`idConta`),
  CONSTRAINT `transacoes_ibfk_1` FOREIGN KEY (`idConta`) REFERENCES `contas` (`idConta`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
