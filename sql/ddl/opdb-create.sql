--client
CREATE TABLE postal_delivery_system_opdb.client (
	client_id varchar(15) NOT NULL,
	client_zipcode varchar(10) NOT NULL,
	client_name varchar(255) NULL,
	client_phone varchar(100) NULL,
	client_location varchar(255) NULL,
	client_city varchar(255) NULL,
	client_datejoined varchar(255) NULL,
	CONSTRAINT client_pkey PRIMARY KEY (client_id)
);

--client_personal
CREATE TABLE postal_delivery_system_opdb.client_personal (
	client_id varchar(15) NOT NULL,
	CONSTRAINT client_personal_pkey PRIMARY KEY (client_id)
    CONSTRAINT client_personal_client_id_fkey FOREIGN KEY (client_id) REFERENCES postal_delivery_system_opdb.client(client_id) ON DELETE CASCADE
);

--client_store
CREATE TABLE postal_delivery_system_opdb.client_store (
	client_id varchar(100) NOT NULL,
	client_haswarehouse varchar(10) NULL,
	CONSTRAINT client_store_pkey PRIMARY KEY (client_id),
	CONSTRAINT client_storewarehouse_client_id_fkey FOREIGN KEY (client_id) REFERENCES postal_delivery_system_opdb.client(client_id) ON DELETE CASCADE
);

--client_storewarehouse
CREATE TABLE postal_delivery_system_opdb.client_storewarehouse (
	client_id varchar(100) NULL,
	sw_id varchar(100) NOT NULL,
	sw_capacity int4 NULL,
	sw_noofworkers int4 NULL,
	sw_supervisorid varchar(100) NULL,
	sw_supervisorname varchar(255) NULL,
	client_haswarehouse varchar(50) NULL,
	CONSTRAINT client_storewarehouse_pkey PRIMARY KEY (sw_id),
	CONSTRAINT client_storewarehouse_client_id_fkey FOREIGN KEY (client_id) REFERENCES postal_delivery_system_opdb.client_store(client_id) ON DELETE CASCADE
);

--deliverycomplaint
CREATE TABLE postal_delivery_system_opdb.deliverycomplaint (
	dc_id varchar(100) NOT NULL,
	dorder_id varchar(100) NOT NULL,
	dc_desc varchar(255) NULL,
	dc_status varchar(255) NULL,
	CONSTRAINT deliverycomplaint_pkey PRIMARY KEY (dc_id),
	CONSTRAINT deliverycomplaint_dorder_id_fkey FOREIGN KEY (dorder_id) REFERENCES postal_delivery_system_opdb.deliveryorder(do_id) ON DELETE CASCADE
);

--deliveryorder
CREATE TABLE postal_delivery_system_opdb.deliveryorder (
	do_id varchar(100) NOT NULL,
	do_date date NULL,
	do_deliverylocation varchar(100) NULL,
	do_deliverycity varchar(100) NULL,
	do_deliveryzipcode varchar(10) NULL,
	do_deliveryphone varchar(20) NULL,
	do_clientpaymentcost varchar(100) NULL,
	do_orderstatus varchar(255) NULL,
	do_weightinlbsrounded int4 NULL,
	do_clientid varchar(100) NULL,
	client_tracking_no varchar(255) NULL,
	delivery_code int4 NULL,
	dtrip_id varchar(100) NULL,
	do_completiondate date NULL,
	do_est_completiondate date NULL,
	CONSTRAINT deliveryorder_pkey PRIMARY KEY (do_id),
	CONSTRAINT deliveryorder_do_clientid_fkey FOREIGN KEY (do_clientid) REFERENCES postal_delivery_system_opdb.client(client_id),
	CONSTRAINT fk_deliveryorder_deliverytrip FOREIGN KEY (dtrip_id) REFERENCES postal_delivery_system_opdb.deliverytrip(dtrip_id)
);

--deliveryperson
CREATE TABLE postal_delivery_system_opdb.deliveryperson (
	dp_empid varchar(100) NOT NULL,
	dp_managerid varchar(100) NULL,
	dp_joindate date NULL,
	dp_licenseno varchar(255) NULL,
	dp_candriveheavytruck varchar(10) NULL,
	dp_candriveoutstate varchar(10) NULL,
	dp_basesalary varchar(15) NULL,
	CONSTRAINT deliveryperson_pkey PRIMARY KEY (dp_empid)
);

--deliverytrip
CREATE TABLE postal_delivery_system_opdb.deliverytrip (
	dtrip_id varchar(100) NOT NULL,
	dtrip_trackingno varchar(100) NULL,
	dtrip_status varchar(255) NULL,
	dtrip_truckid varchar(100) NULL,
	dtrip_deliverypersonid varchar(100) NULL,
	gas_cost_per_mile varchar(20) NULL,
	CONSTRAINT deliverytrip_pkey PRIMARY KEY (dtrip_id),
	CONSTRAINT deliverytrip_dtrip_truckid_fkey FOREIGN KEY (dtrip_truckid) REFERENCES postal_delivery_system_opdb.deliverytruck(dt_id),
	CONSTRAINT fk_deliveryperson_constraint FOREIGN KEY (dtrip_deliverypersonid) REFERENCES postal_delivery_system_opdb.deliveryperson(dp_empid) ON DELETE CASCADE
);

--deliverytruck
CREATE TABLE postal_delivery_system_opdb.deliverytruck (
	dt_id varchar(15) NOT NULL,
	dt_type varchar(255) DEFAULT NULL::character varying NULL,
	dt_maximumwtinlbs int4 NULL,
	dt_licenseplate varchar(255) NULL,
	CONSTRAINT deliverytruck_pkey PRIMARY KEY (dt_id)
);