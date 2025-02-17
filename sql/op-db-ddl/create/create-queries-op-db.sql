
-- Client
CREATE TABLE postal_delivery_system_opdb.Client (
    Client_ID VARCHAR(50),
    Client_Zipcode VARCHAR(10),
    Client_Name VARCHAR(100),
    Client_Phone VARCHAR(15),
    Client_Location VARCHAR(200),
    Client_DateJoined DATE,
    PRIMARY KEY (Client_ID, Client_Zipcode)
);

-- DeliveryOrder
CREATE TABLE postal_delivery_system_opdb.DeliveryOrder (
    Do_ID VARCHAR(50) PRIMARY KEY,
    Do_Type INTEGER CHECK (Do_Type IN (1, 2)),
    Do_Date DATE,
    Do_Location VARCHAR(200),
    Do_Zipcode VARCHAR(10),
    Do_CustomerPhone VARCHAR(15),
    Do_CustomerPaymentCost DECIMAL(10,2),
    Do_Status VARCHAR(50),
    Do_WeightInLBS DECIMAL(10,2),
    Do_Dimensions VARCHAR(50),
    Client_ID VARCHAR(50),
    Client_Zipcode VARCHAR(10),
    FOREIGN KEY (Client_ID, Client_Zipcode) REFERENCES postal_delivery_system_opdb.Client(Client_ID, Client_Zipcode)
);

-- Client Type - Personal
CREATE TABLE postal_delivery_system_opdb.Client_Personal (
    Client_Id VARCHAR(50),
    Client_Zipcode VARCHAR(10),
    Pr_Addresses VARCHAR(200) NOT NULL,
    PRIMARY KEY (Client_Id, Client_Zipcode),
    FOREIGN KEY (Client_Id, Client_Zipcode) REFERENCES postal_delivery_system_opdb.client(Client_ID, Client_Zipcode)
);

-- Client Type - Store
CREATE TABLE postal_delivery_system_opdb.Client_Store (
    Client_Id VARCHAR(50),
    Client_Zipcode VARCHAR(10),
    St_HasWarehouse BOOLEAN,
    PRIMARY KEY (Client_Id, Client_Zipcode),
    FOREIGN KEY (Client_Id, Client_Zipcode) REFERENCES postal_delivery_system_opdb.Client(Client_ID, Client_Zipcode)
);

-- Client Type - Client: Has StoreWarehouse
CREATE TABLE postal_delivery_system_opdb.Client_StoreWarehouse (
    Client_Id VARCHAR(50),
    Client_Zipcode VARCHAR(10),
    Sw_Id VARCHAR(50),
    Sw_Capacity INTEGER,
    Sw_NoOfWorkers INTEGER,
    Sw_SupervisorID VARCHAR(50),
    Sw_SupervisorName VARCHAR(100),
    Sw_Location VARCHAR(200),
    Sw_Zipcode VARCHAR(10),
    PRIMARY KEY (Client_Id, Client_Zipcode, Sw_Id),
    FOREIGN KEY (Client_Id, Client_Zipcode) REFERENCES postal_delivery_system_opdb.Client_Store(Client_Id, Client_Zipcode)
);

-- DeliveryTruck
CREATE TABLE postal_delivery_system_opdb.DeliveryTruck (
    Dt_Id VARCHAR(50) PRIMARY KEY,
    Dt_Type VARCHAR(50),
    Dt_MakeQuantity INTEGER,
    Dt_LicencePlate VARCHAR(20),
    Dt_InsuranceNo VARCHAR(50),
    Dt_InsuranceValidity DATE
);

-- DeliveryPerson
CREATE TABLE postal_delivery_system_opdb.DeliveryPerson (
    Dp_EmpID VARCHAR(50) PRIMARY KEY,
    Dp_ManagerID VARCHAR(50),
    Dp_JoinDate DATE,
    Dp_LicenceNo VARCHAR(50),
    Dp_LicenceEndDate DATE,
    Dp_CanDriveHeavyTruck BOOLEAN,
    Dp_CanDriveOutstate BOOLEAN
);

-- DeliveryAttempt
CREATE TABLE postal_delivery_system_opdb.DeliveryAttempt (
    Da_ID VARCHAR(50) PRIMARY KEY,
    Da_LocType INTEGER CHECK (Da_LocType IN (1, 2, 3, 4)),
    Da_Status VARCHAR(50),
    Da_TotalDeliveries INTEGER,
    Da_TotalDistance DECIMAL(10,2),
    Da_CostPerMile DECIMAL(10,2),
    Da_TotalCost DECIMAL(10,2),
    Dt_id VARCHAR(50),
    Dp_EmpID VARCHAR(50),
    FOREIGN KEY (Dt_id) REFERENCES postal_delivery_system_opdb.deliverytruck(Dt_id),
    FOREIGN KEY (Dp_EmpID) REFERENCES postal_delivery_system_opdb.deliveryperson(Dp_EmpID)
);

-- DeliveryOrder Requires DeliveryAttempt
-- Client Delivery Tracking No. is given here
CREATE TABLE postal_delivery_system_opdb.Do_Requires_Da (
    Do_ID VARCHAR(50),
    DA_ID VARCHAR(50),
    Do_ClientTrackingNumber VARCHAR(50),
    Do_DeliveryCode VARCHAR(50),
    PRIMARY KEY (Do_ID, DA_ID),
    FOREIGN KEY (Do_ID) REFERENCES postal_delivery_system_opdb.DeliveryOrder(Do_ID),
    FOREIGN KEY (DA_ID) REFERENCES postal_delivery_system_opdb.DeliveryAttempt(Da_ID)
);

-- DeliveryAttempt is Delivered by DeliveryTruck and DeliveryPerson
CREATE TABLE postal_delivery_system_opdb.Da_Dt_Dp_Deliveres (
    Da_ID VARCHAR(50),
    Dt_ID VARCHAR(50),
    Dp_EmpID VARCHAR(50),
    Dp_Salary DECIMAL(10,2),
    Dp_TotalGasCost DECIMAL(10,2),
    Dt_DeliveryOrderQty INTEGER,
    PRIMARY KEY (Da_ID, Dt_ID, Dp_EmpID),
    FOREIGN KEY (Da_ID) REFERENCES postal_delivery_system_opdb.DeliveryAttempt(Da_ID),
    FOREIGN KEY (Dt_ID) REFERENCES postal_delivery_system_opdb.DeliveryTruck(Dt_Id),
    FOREIGN KEY (Dp_EmpID) REFERENCES postal_delivery_system_opdb.DeliveryPerson(Dp_EmpID)
);

-- DeliveryComplaint
CREATE TABLE postal_delivery_system_opdb.DeliveryComplaint (
    Dc_ID VARCHAR(50),
    Da_Id VARCHAR(50),
    Dc_RegistrationDate DATE,
    Dc_Reason VARCHAR(200),
    Dc_Status VARCHAR(50),
    Dc_CustomerPhone VARCHAR(15),
    Dc_TrackingNo VARCHAR(50),
    PRIMARY KEY (Dc_ID, Da_Id),
    FOREIGN KEY (Da_Id) REFERENCES postal_delivery_system_opdb.DeliveryAttempt(Da_ID)
);

-- DeliveryTracking - for internal system tracking
CREATE TABLE postal_delivery_system_opdb.DeliveryTracking (
    Tr_TrackingNo VARCHAR(50) PRIMARY KEY,
    Tr_CurrentLocation VARCHAR(200),
    Tr_StatusUpdateTime TIMESTAMP,
    Tr_EstimatedTimeToNextStage TIMESTAMP,
    Tr_EstimatedDeliveryCompletionDate DATE,
    Tr_RemainingDeliveries INTEGER,
    Da_ID VARCHAR(50),
    FOREIGN KEY (Da_ID) REFERENCES postal_delivery_system_opdb.DeliveryAttempt(Da_ID)
);