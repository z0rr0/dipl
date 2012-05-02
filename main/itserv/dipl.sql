-- phpMyAdmin SQL Dump
-- version 3.5.0
-- http://www.phpmyadmin.net
--
-- Хост: localhost
-- Время создания: Май 02 2012 г., 17:54
-- Версия сервера: 5.1.61-0+squeeze1-log
-- Версия PHP: 5.3.3-7+squeeze8

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- База данных: `dipl`
--

-- --------------------------------------------------------

--
-- Структура таблицы `itserv_client`
--

DROP TABLE IF EXISTS `itserv_client`;
CREATE TABLE IF NOT EXISTS `itserv_client` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(127) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `address` longtext,
  `discont` double NOT NULL DEFAULT '0',
  `comment` longtext,
  `modified` datetime NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `itserv_client_52094d6e` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Структура таблицы `itserv_contract`
--

DROP TABLE IF EXISTS `itserv_contract`;
CREATE TABLE IF NOT EXISTS `itserv_contract` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `discont` double NOT NULL DEFAULT '0',
  `total_all` double NOT NULL DEFAULT '0',
  `total_disc` double NOT NULL DEFAULT '0',
  `number` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `comment` longtext,
  `modified` datetime NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `number` (`number`),
  KEY `itserv_contract_403f60f` (`user_id`),
  KEY `itserv_contract_679343db` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Структура таблицы `itserv_product`
--

DROP TABLE IF EXISTS `itserv_product`;
CREATE TABLE IF NOT EXISTS `itserv_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider_id` int(11) DEFAULT NULL,
  `name` varchar(127) NOT NULL,
  `service` tinyint(1) NOT NULL DEFAULT '0',
  `price` double NOT NULL DEFAULT '0',
  `rest` int(10) unsigned NOT NULL DEFAULT '0',
  `comment` longtext,
  `modified` datetime NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `itserv_product_261a2069` (`provider_id`),
  KEY `itserv_product_52c5ef6b` (`service`),
  KEY `itserv_product_5f59f023` (`rest`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Структура таблицы `itserv_provider`
--

DROP TABLE IF EXISTS `itserv_provider`;
CREATE TABLE IF NOT EXISTS `itserv_provider` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(127) NOT NULL,
  `address` longtext,
  `phone` varchar(15) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `site` varchar(255) DEFAULT NULL,
  `comment` longtext,
  `modified` datetime NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `itserv_provider_52094d6e` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Структура таблицы `itserv_reqlist`
--

DROP TABLE IF EXISTS `itserv_reqlist`;
CREATE TABLE IF NOT EXISTS `itserv_reqlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `contract_id` int(11) DEFAULT NULL,
  `product_id` int(11) NOT NULL,
  `number` int(10) unsigned NOT NULL DEFAULT '1',
  `price` double DEFAULT NULL,
  `modified` datetime NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `itserv_reqlist_4a4e8ffb` (`client_id`),
  KEY `itserv_reqlist_4f844952` (`contract_id`),
  KEY `itserv_reqlist_44bdf3ee` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;


-- create additional backup tables
-- --------------------------------------------------------

--
-- Структура таблицы `wbackup_itserv_client`
--

DROP TABLE IF EXISTS `wbackup_itserv_client`;
CREATE TABLE IF NOT EXISTS `wbackup_itserv_client` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(127) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `address` longtext,
  `discont` double NOT NULL DEFAULT '0',
  `comment` longtext,
  `modified` datetime NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `itserv_client_52094d6e` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Структура таблицы `wbackup_itserv_contract`
--

DROP TABLE IF EXISTS `wbackup_itserv_contract`;
CREATE TABLE IF NOT EXISTS `wbackup_itserv_contract` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `discont` double NOT NULL DEFAULT '0',
  `total_all` double NOT NULL DEFAULT '0',
  `total_disc` double NOT NULL DEFAULT '0',
  `number` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `comment` longtext,
  `modified` datetime NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `number` (`number`),
  KEY `itserv_contract_403f60f` (`user_id`),
  KEY `itserv_contract_679343db` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Структура таблицы `wbackup_itserv_product`
--

DROP TABLE IF EXISTS `wbackup_itserv_product`;
CREATE TABLE IF NOT EXISTS `wbackup_itserv_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider_id` int(11) DEFAULT NULL,
  `name` varchar(127) NOT NULL,
  `service` tinyint(1) NOT NULL DEFAULT '0',
  `price` double NOT NULL DEFAULT '0',
  `rest` int(10) unsigned NOT NULL DEFAULT '0',
  `comment` longtext,
  `modified` datetime NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `itserv_product_261a2069` (`provider_id`),
  KEY `itserv_product_52c5ef6b` (`service`),
  KEY `itserv_product_5f59f023` (`rest`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Структура таблицы `wbackup_itserv_provider`
--

DROP TABLE IF EXISTS `wbackup_itserv_provider`;
CREATE TABLE IF NOT EXISTS `wbackup_itserv_provider` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(127) NOT NULL,
  `address` longtext,
  `phone` varchar(15) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `site` varchar(255) DEFAULT NULL,
  `comment` longtext,
  `modified` datetime NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `itserv_provider_52094d6e` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Структура таблицы `wbackup_itserv_reqlist`
--

DROP TABLE IF EXISTS `wbackup_itserv_reqlist`;
CREATE TABLE IF NOT EXISTS `wbackup_itserv_reqlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `contract_id` int(11) DEFAULT NULL,
  `product_id` int(11) NOT NULL,
  `number` int(10) unsigned NOT NULL DEFAULT '1',
  `price` double DEFAULT NULL,
  `modified` datetime NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `itserv_reqlist_4a4e8ffb` (`client_id`),
  KEY `itserv_reqlist_4f844952` (`contract_id`),
  KEY `itserv_reqlist_44bdf3ee` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- триггеры на удаление данных

-- client
DROP TRIGGER IF EXISTS `del_itserv_client`;
DELIMITER //
CREATE TRIGGER `del_itserv_client` BEFORE DELETE ON `itserv_client`
 FOR EACH ROW BEGIN
  INSERT INTO `wbackup_itserv_client` SET id=OLD.id, name=OLD.name, phone=OLD.phone, email=OLD.email, address=OLD.address, 
  discont=OLD.discont, comment=OLD.comment, created=OLD.created, modified=NOW();
END
//
DELIMITER ;

-- contract
DROP TRIGGER IF EXISTS `del_itserv_contract`;
DELIMITER //
CREATE TRIGGER `del_itserv_contract` BEFORE DELETE ON `itserv_contract`
 FOR EACH ROW BEGIN
  INSERT INTO `wbackup_itserv_contract` SET id=OLD.id, user_id=OLD.user_id, discont=OLD.discont, total_all=OLD.total_all, total_disc=OLD.total_disc, 
  number=OLD.number, date=OLD.date, comment=OLD.comment, created=OLD.created, modified=NOW();
END
//
DELIMITER ;

-- product
DROP TRIGGER IF EXISTS `del_itserv_product`;
DELIMITER //
CREATE TRIGGER `del_itserv_product` BEFORE DELETE ON `itserv_product`
 FOR EACH ROW BEGIN
  INSERT INTO `wbackup_itserv_product` SET id=OLD.id, provider_id=OLD.provider_id, name=OLD.name, service=OLD.service, price=OLD.price, 
  rest=OLD.rest, comment=OLD.comment, created=OLD.created, modified=NOW();
END
//
DELIMITER ;

-- provider
DROP TRIGGER IF EXISTS `del_itserv_provider`;
DELIMITER //
CREATE TRIGGER `del_itserv_provider` BEFORE DELETE ON `itserv_provider`
 FOR EACH ROW BEGIN
  INSERT INTO `wbackup_itserv_provider` SET id=OLD.id, name=OLD.name, phone=OLD.phone, email=OLD.email, address=OLD.address, 
  site=OLD.site, comment=OLD.comment, created=OLD.created, modified=NOW();
END
//
DELIMITER ;

-- reqlist
DROP TRIGGER IF EXISTS `del_itserv_reqlist`;
DELIMITER //
CREATE TRIGGER `del_itserv_reqlist` BEFORE DELETE ON `itserv_reqlist`
 FOR EACH ROW BEGIN
  INSERT INTO `wbackup_itserv_reqlist` SET id=OLD.id, client_id=OLD.client_id, contract_id=OLD.contract_id, product_id=OLD.product_id, price=OLD.price, 
  created=OLD.created, modified=NOW();
END
//
DELIMITER ;



