--dim_country
CREATE TABLE postal_delivery_system_dwh.dim_country (
	country_key serial4 NOT NULL,
	country_name varchar(100) NULL,
	CONSTRAINT dim_country_pkey PRIMARY KEY (country_key)
);

--dim_state
CREATE TABLE postal_delivery_system_dwh.dim_state (
	state_key serial4 NOT NULL,
	state_name varchar(100) NULL,
	country_key int4 NULL,
	CONSTRAINT dim_state_pkey PRIMARY KEY (state_key),
	CONSTRAINT fk_state_country FOREIGN KEY (country_key) REFERENCES postal_delivery_system_dwh.dim_country(country_key) ON DELETE CASCADE ON UPDATE CASCADE
);

--dim_city
CREATE TABLE postal_delivery_system_dwh.dim_city (
	city_key serial4 NOT NULL,
	city_name varchar(100) NULL,
	state_key int4 NULL,
	CONSTRAINT dim_city_pkey PRIMARY KEY (city_key),
	CONSTRAINT dim_city_state_key_fkey FOREIGN KEY (state_key) REFERENCES postal_delivery_system_dwh.dim_state(state_key) ON DELETE CASCADE ON UPDATE CASCADE
);

--dim_location
CREATE TABLE postal_delivery_system_dwh.dim_location (
	location_key serial4 NOT NULL,
	location_complete text NOT NULL,
	zipcode varchar(20) NOT NULL,
	city_key int4 NOT NULL,
	CONSTRAINT dim_location_pkey PRIMARY KEY (location_key),
	CONSTRAINT dim_location_city_key_fkey FOREIGN KEY (city_key) REFERENCES postal_delivery_system_dwh.dim_city(city_key) ON DELETE CASCADE ON UPDATE CASCADE
);

--dim_year
CREATE TABLE postal_delivery_system_dwh.dim_year (
	year_key serial4 NOT NULL,
	year_number int4 NULL,
	CONSTRAINT dim_year_pkey PRIMARY KEY (year_key)
);

--dim_quarter
CREATE TABLE postal_delivery_system_dwh.dim_quarter (
	quarter_key serial4 NOT NULL,
	quarter_number int4 NULL,
	year_key int4 NULL,
	CONSTRAINT dim_quarter_pkey PRIMARY KEY (quarter_key),
	CONSTRAINT dim_quarter_year_key_fkey FOREIGN KEY (year_key) REFERENCES postal_delivery_system_dwh.dim_year(year_key) ON DELETE CASCADE ON UPDATE CASCADE
);

--dim_month
CREATE TABLE postal_delivery_system_dwh.dim_month (
	month_key serial4 NOT NULL,
	month_name varchar(20) NULL,
	quarter_key int4 NULL,
	CONSTRAINT dim_month_pkey PRIMARY KEY (month_key),
	CONSTRAINT dim_month_quarter_key_fkey FOREIGN KEY (quarter_key) REFERENCES postal_delivery_system_dwh.dim_quarter(quarter_key) ON DELETE CASCADE ON UPDATE CASCADE
);

--dim_date
CREATE TABLE postal_delivery_system_dwh.dim_date (
	date_key int4 NOT NULL,
	full_date date NULL,
	day_of_the_week varchar(20) NULL,
	week_no int4 NULL,
	month_key int4 NULL,
	CONSTRAINT dim_date_pkey PRIMARY KEY (date_key),
	CONSTRAINT dim_date_month_key_fkey FOREIGN KEY (month_key) REFERENCES postal_delivery_system_dwh.dim_month(month_key) ON DELETE CASCADE ON UPDATE CASCADE
);

--dim_client
CREATE TABLE postal_delivery_system_dwh.dim_client (
	client_key int4 NOT NULL,
	business_client_id varchar(50) NULL,
	client_name varchar(255) NULL,
	client_phone varchar(20) NULL,
	client_datejoined_key int4 NULL,
	client_location_key int4 NULL,
	c_start_date date NOT NULL,
	c_end_date date NULL,
	c_is_current bool DEFAULT true NOT NULL,
	c_version_number int4 NOT NULL,
	CONSTRAINT dim_client_pkey PRIMARY KEY (client_key),
	CONSTRAINT fk_client_location FOREIGN KEY (client_location_key) REFERENCES postal_delivery_system_dwh.dim_location(location_key) ON DELETE CASCADE ON UPDATE CASCADE
);

--dim_personalclient
CREATE TABLE postal_delivery_system_dwh.dim_personalclient (
	client_key int4 NOT NULL,
	pc_joindate_key int4 NULL,
	CONSTRAINT dim_personalclient_pkey PRIMARY KEY (client_key),
	CONSTRAINT fk_personalclient_client FOREIGN KEY (client_key) REFERENCES postal_delivery_system_dwh.dim_client(client_key) ON DELETE CASCADE ON UPDATE CASCADE
);

--dim_storeclient
CREATE TABLE postal_delivery_system_dwh.dim_storeclient (
	client_key int4 NOT NULL,
	client_has_warehouse bool NULL,
	CONSTRAINT dim_storeclient_pkey PRIMARY KEY (client_key),
	CONSTRAINT fk_storeclient_client FOREIGN KEY (client_key) REFERENCES postal_delivery_system_dwh.dim_client(client_key) ON DELETE CASCADE ON UPDATE CASCADE
);

--dim_storewarehouse
CREATE TABLE postal_delivery_system_dwh.dim_storewarehouse (
	warehouse_key int4 NOT NULL,
	wh_id varchar(15) NULL,
	store_key int4 NULL,
	wh_capacity int4 NULL,
	wh_worker_count int4 NULL,
	supervisor_id varchar(30) NULL,
	supervisor_name varchar(255) NULL,
	previous_wh_capacity int4, 
    previous_wh_worker_count int4, 
    previous_supervisor_id varchar(30), 
    previous_supervisor_name varchar(30), 
	CONSTRAINT dim_storewarehouse_pkey PRIMARY KEY (warehouse_key),
	CONSTRAINT dim_storewarehouse_store_key_fkey FOREIGN KEY (store_key) REFERENCES postal_delivery_system_dwh.dim_storeclient(client_key) ON DELETE CASCADE ON UPDATE CASCADE
);

--dim_deliveryperson
CREATE TABLE postal_delivery_system_dwh.dim_deliveryperson (
	delivery_person_key int4 NOT NULL,
	employee_id varchar(50) NULL,
	license_no varchar(50) NULL,
	can_drive_heavy_truck bool NULL,
	can_drive_out_state bool NULL,
	join_date_key int4 NULL,
	base_salary numeric NULL,
	d_start_date date NOT NULL,
	d_end_date date NULL,
	d_is_current bool DEFAULT true NOT NULL,
	d_version_number int4 NOT NULL,
	CONSTRAINT dim_deliveryperson_pkey PRIMARY KEY (delivery_person_key),
	CONSTRAINT dim_deliveryperson_join_date_key_fkey FOREIGN KEY (join_date_key) REFERENCES postal_delivery_system_dwh.dim_date(date_key) ON DELETE CASCADE ON UPDATE CASCADE
);

--dim_deliverytruck
CREATE TABLE postal_delivery_system_dwh.dim_deliverytruck (
	truck_key int4 NOT NULL,
	truck_id varchar(50) NULL,
	truck_type varchar(100) NULL,
	max_wt_in_lbs numeric NULL,
	license_plate varchar(50) NULL,
	t_start_date date NOT NULL,
	t_end_date date NULL,
	t_is_current bool DEFAULT true NOT NULL,
	t_version_number int4 NOT NULL,
	CONSTRAINT dim_deliverytruck_pkey PRIMARY KEY (truck_key)
);

--dim_order
CREATE TABLE postal_delivery_system_dwh.dim_order (
	order_key int4 NOT NULL,
	order_id varchar(15) NULL,
	order_date_key int4 NULL,
	order_location_key int4 NULL,
	order_deliveryphone varchar(20) NULL,
	order_clientpayment numeric NULL,
	order_weight_in_lbs numeric NULL,
	order_tracking_no varchar(50) NULL,
	delivery_code varchar(50) NULL,
	order_status varchar(50) NULL,
	dtrip_id varchar(30) NULL,
	CONSTRAINT dim_order_pkey PRIMARY KEY (order_key),
	CONSTRAINT dim_order_order_date_key_fkey FOREIGN KEY (order_date_key) REFERENCES postal_delivery_system_dwh.dim_date(date_key) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT dim_order_order_location_key_fkey FOREIGN KEY (order_location_key) REFERENCES postal_delivery_system_dwh.dim_location(location_key) ON DELETE CASCADE ON UPDATE CASCADE
);

--fact_deliverycomplaints
CREATE TABLE postal_delivery_system_dwh.fact_deliverycomplaints (
	complaint_key serial4 NOT NULL,
	complaint_id varchar(15) NOT NULL,
	order_key int4 NOT NULL,
	client_key int4 NOT NULL,
	complaint_reason text NULL,
	complaint_status varchar(50) NULL,
	CONSTRAINT fact_deliverycomplaints_complaint_key_key UNIQUE (complaint_key),
	CONSTRAINT fact_deliverycomplaints_pkey PRIMARY KEY (complaint_key, order_key, client_key),
	CONSTRAINT fact_deliverycomplaints_order_key_fkey FOREIGN KEY (order_key) REFERENCES postal_delivery_system_dwh.dim_order(order_key) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT fk_deliverycomplaints_client FOREIGN KEY (client_key) REFERENCES postal_delivery_system_dwh.dim_client(client_key) ON DELETE CASCADE ON UPDATE CASCADE
);

--fact_deliverytrip
CREATE TABLE postal_delivery_system_dwh.fact_deliverytrip (
	trip_key serial4 NOT NULL,
	trip_id varchar(15) NOT NULL,
	truck_key int4 NOT NULL,
	dperson_key int4 NOT NULL,
	gas_cost_per_mile numeric NULL,
	trip_start_date_key int4 NULL,
	trip_end_date_key int4 NULL,
	total_deliveries numeric NULL,
	total_distance_in_miles numeric NULL,
	total_weight_in_lbs numeric NULL,
	total_pay_for_dp numeric NULL,
	total_gas_cost numeric NULL,
	total_cost_of_trip numeric NULL,
	CONSTRAINT fact_deliverytrip_pkey PRIMARY KEY (trip_key, truck_key, dperson_key),
	CONSTRAINT fact_deliverytrip_trip_key_key UNIQUE (trip_key),
	CONSTRAINT fact_deliverytrip_dperson_key_fkey FOREIGN KEY (dperson_key) REFERENCES postal_delivery_system_dwh.dim_deliveryperson(delivery_person_key) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT fact_deliverytrip_trip_end_date_key_fkey FOREIGN KEY (trip_end_date_key) REFERENCES postal_delivery_system_dwh.dim_date(date_key) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT fact_deliverytrip_trip_start_date_key_fkey FOREIGN KEY (trip_start_date_key) REFERENCES postal_delivery_system_dwh.dim_date(date_key) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT fact_deliverytrip_truck_key_fkey FOREIGN KEY (truck_key) REFERENCES postal_delivery_system_dwh.dim_deliverytruck(truck_key) ON DELETE CASCADE ON UPDATE CASCADE
);

--fact_orderdeliveries
CREATE TABLE postal_delivery_system_dwh.fact_orderdeliveries (
	deliveryorder_key serial4 NOT NULL,
	order_key int4 NOT NULL,
	client_key int4 NOT NULL,
	return_location_key int4 NULL,
	dtrip_id varchar(30) NULL,
	delivery_type varchar(10) NULL,
	delta_days numeric NULL,
	delivery_base_cost numeric NULL,
	delivery_total_cost numeric NULL,
	delivery_profit_margin numeric NULL,
	CONSTRAINT fact_orderdeliveries_deliveryorder_key_key UNIQUE (deliveryorder_key),
	CONSTRAINT fact_orderdeliveries_pkey PRIMARY KEY (deliveryorder_key, order_key, client_key),
	CONSTRAINT fact_orderdeliveries_order_key_fkey FOREIGN KEY (order_key) REFERENCES postal_delivery_system_dwh.dim_order(order_key) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT fact_orderdeliveries_return_location_key_fkey FOREIGN KEY (return_location_key) REFERENCES postal_delivery_system_dwh.dim_location(location_key) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT fk_orderdeliveries_client FOREIGN KEY (client_key) REFERENCES postal_delivery_system_dwh.dim_client(client_key) ON DELETE CASCADE ON UPDATE CASCADE
);
