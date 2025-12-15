-- 🧍 Patient table
CREATE TABLE Patient (
    patientID INT AUTO_INCREMENT PRIMARY KEY,
    patientName VARCHAR(100) NOT NULL,
    patientGender ENUM('Male', 'Female', 'Other') NOT NULL,
    patientBirthDate DATE,
    patientPhoneNumber VARCHAR(15)
);

-- 🩺 Doctor table
CREATE TABLE Doctor (
    doctorID INT AUTO_INCREMENT PRIMARY KEY,
    doctorName VARCHAR(100) NOT NULL,
    doctorSpecialty VARCHAR(100)
);

-- 🏠 Room table
CREATE TABLE Room (
    roomNumber INT AUTO_INCREMENT PRIMARY KEY,
    roomStatus ENUM('Available', 'Occupied', 'Maintenance') DEFAULT 'Available'
);

-- 💊 Treatment table
CREATE TABLE Treatment (
    treatmentID INT AUTO_INCREMENT PRIMARY KEY,
    treatment VARCHAR(100) NOT NULL,
    treatmentCost DECIMAL(10,2)
);

-- 💵 Payment table
CREATE TABLE Payment (
    paymentID INT AUTO_INCREMENT PRIMARY KEY,
    paymentAmount DECIMAL(10,2),
    paymentDate DATETIME,
    paymentStatus ENUM('Pending', 'Completed', 'Cancelled') DEFAULT 'Pending'
);

-- 👩‍💼 Staff table
CREATE TABLE Staff (
    staffID INT AUTO_INCREMENT PRIMARY KEY,
    staffName VARCHAR(100) NOT NULL,
    staffRole VARCHAR(50)
);

-- 📅 Appointment table with composite PK and cascades
CREATE TABLE Appointment (
    appointmentDate DATE,
    appointmentTime TIME,
    appointmentStatus ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
    patientID INT NOT NULL,
    doctorID INT NOT NULL,
    roomNumber INT,
    treatmentID INT,
    paymentID INT,
    staffID INT,
    PRIMARY KEY (appointmentDate, appointmentTime, patientID, doctorID),
    FOREIGN KEY (patientID) REFERENCES Patient(patientID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (doctorID) REFERENCES Doctor(doctorID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (roomNumber) REFERENCES Room(roomNumber)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (treatmentID) REFERENCES Treatment(treatmentID)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (paymentID) REFERENCES Payment(paymentID)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (staffID) REFERENCES Staff(staffID)
        ON UPDATE CASCADE ON DELETE SET NULL
);