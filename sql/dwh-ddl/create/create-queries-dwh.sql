-- Time dimension tables
CREATE TABLE postal_delivery_system_dwh.Dim_Year (
    year_key INT PRIMARY KEY,
    year_number INT
);

CREATE TABLE postal_delivery_system_dwh.Dim_Quarter (
    quarter_key INT PRIMARY KEY,
    quarter_number INT,
    year_key INT REFERENCES postal_delivery_system_dwh.Dim_Year(year_key)
);

CREATE TABLE postal_delivery_system_dwh.Dim_Month (
    month_key INT PRIMARY KEY,
    month_name VARCHAR(20),
    quarter_key INT REFERENCES postal_delivery_system_dwh.Dim_Quarter(quarter_key)
);

CREATE TABLE postal_delivery_system_dwh.Dim_Date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day_of_the_week VARCHAR(20),
    week_no INT,
    month_key INT REFERENCES postal_delivery_system_dwh.Dim_Month(month_key)
);



-- Location dimension tables
CREATE TABLE postal_delivery_system_dwh.Dim_Country (
    country_key VARCHAR(10) PRIMARY KEY,
    country_name VARCHAR(100)
);

CREATE TABLE postal_delivery_system_dwh.Dim_State (
    state_key VARCHAR(10) PRIMARY KEY,
    state_name VARCHAR(100),
    country_key VARCHAR(10) REFERENCES postal_delivery_system_dwh.Dim_Country(country_key)
);

CREATE TABLE postal_delivery_system_dwh.Dim_City (
    city_key varchar(10) PRIMARY KEY,
    city_name VARCHAR(100),
    state_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_State(state_key)
);

CREATE TABLE postal_delivery_system_dwh.Dim_Location (
    location_key varchar(10) PRIMARY KEY,
    location_complete TEXT,
    zipcode VARCHAR(20),
    city_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_City(city_key)
);





-- Client dimension tables with SCD Type 2
CREATE TABLE postal_delivery_system_dwh.Dim_Client (
    client_key varchar(10),                                    -- Surrogate key
    business_client_id VARCHAR(50),                       -- Natural/business key
    client_name VARCHAR(255),                             -- SCD tracked
    client_phone VARCHAR(20),                             -- SCD tracked
    client_email VARCHAR(255),                            -- SCD tracked
    client_location_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_Location(location_key), -- SCD tracked
    -- SCD Type 2 tracking columns
    c_start_date DATE NOT NULL,
    c_end_date DATE,
    c_is_current BOOLEAN NOT NULL DEFAULT TRUE,
    c_version_number INT NOT NULL,
    PRIMARY KEY (client_key)
);

CREATE TABLE postal_delivery_system_dwh.Dim_PersonalClient (
    client_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_Client(client_key),
    client_location_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_Location(location_key),
    primary key (client_key)
);



CREATE TABLE postal_delivery_system_dwh.Dim_StoreClient (
    client_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_Client(client_key),
    client_has_warehouse BOOLEAN,
    primary key (client_key)
);


-- Store/Warehouse dimension with SCD Type 2
CREATE TABLE postal_delivery_system_dwh.Dim_StoreWarehouse (
    warehouse_key varchar(10),                                 -- Surrogate key
    store_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_StoreClient(client_key),                          
    wh_location_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_Location(location_key),
    wh_capacity INT,                                     -- SCD tracked
    wh_worker_count INT,                                     -- SCD tracked
    supervisor_id INT,
    supervisor_name VARCHAR(255),
    -- SCD Type 2 tracking columns
    w_start_date DATE NOT NULL,
    w_end_date DATE,
    w_is_current BOOLEAN NOT NULL DEFAULT TRUE,
    w_version_number INT NOT NULL,
    PRIMARY KEY (warehouse_key)
);




-- Delivery related dimension tables with SCD Type 2
CREATE TABLE postal_delivery_system_dwh.Dim_DeliveryTruck (
    truck_key varchar(10),                                     -- Surrogate key
    truck_id VARCHAR(50),                                 -- Natural/business key
    truck_type VARCHAR(100),
    max_capacity DECIMAL,
    insurance_no VARCHAR(50),                             -- SCD tracked
    insurance_exp_date_key INT REFERENCES postal_delivery_system_dwh.Dim_Date(date_key), -- SCD tracked
    -- SCD Type 2 tracking columns
    t_start_date DATE NOT NULL,
    t_end_date DATE,
    t_is_current BOOLEAN NOT NULL DEFAULT TRUE,
    t_version_number INT NOT NULL,
    PRIMARY KEY (truck_key)
);

CREATE TABLE postal_delivery_system_dwh.Dim_DeliveryPerson (
    delivery_person_key varchar(10),                           -- Surrogate key
    employee_id VARCHAR(50),                              -- Natural/business key
    license_no VARCHAR(50),                               -- SCD tracked
    license_exp_date DATE,                                -- SCD tracked
    can_lift_heavy_truck BOOLEAN,                         -- SCD tracked
    can_drive_out_state BOOLEAN,                          -- SCD tracked
    join_date_key INT REFERENCES postal_delivery_system_dwh.Dim_Date(date_key),
    birth_date_key INT REFERENCES postal_delivery_system_dwh.Dim_Date(date_key),
    base_location_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_Location(location_key), -- SCD tracked
    -- SCD Type 2 tracking columns
    d_start_date DATE NOT NULL,
    d_end_date DATE,
    d_is_current BOOLEAN NOT NULL DEFAULT TRUE,
    d_version_number INT NOT NULL,
    PRIMARY KEY (delivery_person_key)
);

-- Order dimension
CREATE TABLE postal_delivery_system_dwh.Dim_Order (
    order_key varchar(10) PRIMARY KEY,
    order_type VARCHAR(50),
    weight_in_lbs DECIMAL,
    dimension TEXT,
    order_tracking_no varchar(50),
    delivery_code VARCHAR(50),
    payment_cost DECIMAL,
    customer_phone varchar(20),
    order_status VARCHAR(50)
);

-- DeliveryAttempt Dimension
CREATE TABLE postal_delivery_system_dwh.Dim_DeliveryAttempt (
    attempt_key varchar(10) PRIMARY KEY,
    delivery_account_type VARCHAR(50),
    attempt_status VARCHAR(100)
);



-- Fact tables
CREATE TABLE postal_delivery_system_dwh.Fact_DeliveryTracking (
	tracking_key varchar(10) unique not NULL, 
    order_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_Order(order_key),
    attempt_key varchar(10) references postal_delivery_system_dwh.Dim_DeliveryAttempt(attempt_key),
    order_date_key INT REFERENCES postal_delivery_system_dwh.Dim_Date(date_key),
    client_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_Client(client_key),
    current_location_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_Location(location_key),
    truck_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_DeliveryTruck(truck_key),
    estimated_completion_date_key INT REFERENCES postal_delivery_system_dwh.Dim_Date(date_key),
    last_status_update_time TIMESTAMP,
    total_deliveries DECIMAL, 
    total_distance DECIMAL,
    total_cost DECIMAL,
    PRIMARY KEY (tracking_key, order_key, client_key, current_location_key, truck_key)
);


CREATE TABLE postal_delivery_system_dwh.Fact_DeliveryComplaints (
	complaint_key varchar(10) unique not null,
    order_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_Order(order_key),
    client_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_Client(client_key),
    complaint_regis_date_key INT REFERENCES postal_delivery_system_dwh.Dim_Date(date_key),
    complaint_reason TEXT,
    complaint_tracking_no VARCHAR(100),
    complaint_status VARCHAR(50),
    PRIMARY KEY (complaint_key, order_key, client_key, complaint_regis_date_key)
);



CREATE TABLE postal_delivery_system_dwh.Fact_OrderDeliveries(
	delivery_key varchar(10) unique not null,
    order_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_Order(order_key),
    client_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_Client(client_key),
    delivery_location_key varchar(10) REFERENCES postal_delivery_system_dwh.Dim_Location(location_key),
    attempt_key varchar(10) references postal_delivery_system_dwh.Dim_DeliveryAttempt(attempt_key),
    order_date_key INT REFERENCES postal_delivery_system_dwh.Dim_Date(date_key),
    allocated_cost DECIMAL,
    cost_per_mile DECIMAL,
    PRIMARY KEY (delivery_key, order_key, client_key, delivery_location_key, attempt_key, order_date_key)
);




