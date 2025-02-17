-- DeliveryAttempt INSERT statements
-- Location Types: 1 = Urban, 2 = Suburban, 3 = Rural, 4 = Remote
-- Status: 'Completed', 'In Progress', 'Scheduled'

-- Cargo Trucks (40 deliveries each) - Only drivers with HeavyVehicleLicense
INSERT INTO postal_delivery_system_opdb.DeliveryAttempt VALUES ('DA001', 1, 'Completed', 40, 85.50, 2.50, 213.75, 'DT004', 'DP001');
INSERT INTO postal_delivery_system_opdb.DeliveryAttempt VALUES ('DA002', 2, 'Completed', 40, 92.30, 2.50, 230.75, 'DT008', 'DP005');
INSERT INTO postal_delivery_system_opdb.DeliveryAttempt VALUES ('DA003', 1, 'Completed', 40, 78.40, 2.50, 196.00, 'DT012', 'DP007');
INSERT INTO postal_delivery_system_opdb.DeliveryAttempt VALUES ('DA004', 3, 'Completed', 40, 110.20, 2.75, 303.05, 'DT016', 'DP013');

-- Heavy Trucks (25 deliveries each) - Only drivers with HeavyVehicleLicense
INSERT INTO postal_delivery_system_opdb.DeliveryAttempt VALUES ('DA005', 2, 'Completed', 25, 65.30, 2.50, 163.25, 'DT003', 'DP017');
INSERT INTO postal_delivery_system_opdb.DeliveryAttempt VALUES ('DA006', 1, 'Completed', 25, 58.90, 2.50, 147.25, 'DT007', 'DP019');
INSERT INTO postal_delivery_system_opdb.DeliveryAttempt VALUES ('DA007', 3, 'Completed', 25, 88.40, 2.75, 243.10, 'DT011', 'DP025');

-- Mini Trucks (15 deliveries each)
INSERT INTO postal_delivery_system_opdb.DeliveryAttempt VALUES ('DA008', 1, 'Completed', 15, 45.20, 2.25, 101.70, 'DT002', 'DP002');
INSERT INTO postal_delivery_system_opdb.DeliveryAttempt VALUES ('DA009', 2, 'Completed', 15, 52.80, 2.25, 118.80, 'DT006', 'DP004');
INSERT INTO postal_delivery_system_opdb.DeliveryAttempt VALUES ('DA010', 1, 'Completed', 15, 43.60, 2.25, 98.10, 'DT010', 'DP008');

-- Vans (8 deliveries each)
INSERT INTO postal_delivery_system_opdb.DeliveryAttempt VALUES ('DA011', 1, 'Completed', 8, 32.40, 2.00, 64.80, 'DT001', 'DP003');
INSERT INTO postal_delivery_system_opdb.DeliveryAttempt VALUES ('DA012', 2, 'Completed', 8, 35.60, 2.00, 71.20, 'DT005', 'DP006');
INSERT INTO postal_delivery_system_opdb.DeliveryAttempt VALUES ('DA013', 1, 'Completed', 8, 30.90, 2.00, 61.80, 'DT009', 'DP009');
INSERT INTO postal_delivery_system_opdb.DeliveryAttempt VALUES ('DA014', 3, 'In Progress', 8, 45.80, 2.25, 103.05, 'DT013', 'DP011');

-- Total deliveries calculation:
-- Cargo Trucks: 4 * 40 = 160
-- Heavy Trucks: 3 * 25 = 75
-- Mini Trucks: 3 * 15 = 45
-- Vans: 4 * 8 = 32
-- Total: 312 deliveries (covering the required 250 orders with some capacity buffer)