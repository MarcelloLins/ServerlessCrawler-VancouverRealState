CREATE TABLE `real_state`.`rew_ca` (  `id` int(11) NOT NULL AUTO_INCREMENT,  `url` varchar(100) DEFAULT NULL,  `capture_date` timestamp NULL DEFAULT NULL,  
`address` varchar(100) DEFAULT NULL,  `locality` varchar(100) DEFAULT NULL,  `region` varchar(100) DEFAULT NULL,  `postal_code` varchar(10) DEFAULT NULL,  
`price` int(11) DEFAULT NULL,  `bedrooms` int(11) DEFAULT NULL,  `bathrooms` int(11) DEFAULT NULL,  
`sqft` int(11) DEFAULT NULL,  `kind` varchar(30) DEFAULT NULL,  `description` varchar(5000) DEFAULT NULL,  
`features` varchar(200) DEFAULT NULL,  `amenities` varchar(100) DEFAULT NULL,  `fireplaces` int(11) DEFAULT NULL,  
`age` int(11) DEFAULT NULL,  `yearly_taxes` int(11) DEFAULT NULL,  `strata_maintenance_fees` int(11) DEFAULT NULL,  
`area` varchar(100) DEFAULT NULL,  `sub_area` varchar(100) DEFAULT NULL,  `title` varchar(100) DEFAULT NULL,  
`listing_id` varchar(30) DEFAULT NULL,  `primary_agent` varchar(100) DEFAULT NULL,  `primary_broker` varchar(100) DEFAULT NULL,  
`secondary_agent` varchar(100) DEFAULT NULL,  `secondary_broker` varchar(100) DEFAULT NULL,  
PRIMARY KEY (`id`),  KEY `capture_date` (`capture_date`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
