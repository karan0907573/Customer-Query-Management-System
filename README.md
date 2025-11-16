# Customer Query Management System

A Streamlit-based web application for managing customer support queries with role-based access control. This system allows clients to create and track their queries while support team can view and close them.

## Features

### Client Dashboard
- Create new support queries with email, phone, title, and description
- View all personal queries with filtering options (Open/Closed/All)
- Track query status and timestamps
- Form validation for email and phone number inputs

### Support Dashboard
- View all customer queries across the system
- Filter queries by status (Open/Closed/All)
- Select and close open queries
- Track query details including customer information

### Authentication
- Role-based login system (client/support)
- Secure password hashing using SHA-256
- User registration functionality for testing

## Tech Stack

- **Frontend**: Streamlit
- **Database**: MySQL
- **Authentication**: SHA-256 password hashing
- **Data Processing**: Pandas
- **Python Version**: 3.14+

## Project Structure

```
.
├── main.py                      # Main application entry point
├── auth.py                      # Authentication and password hashing
├── db.py                        # Database connection and queries
├── views/
│   ├── login.py                 # Login page
│   ├── customer.py              # Client dashboard
│   └── support.py               # Support dashboard
├── dialog/
│   ├── create_query.py          # Query creation dialog
│   └── close_query.py           # Query closing dialog
├── pyproject.toml               # Project dependencies
├── users.csv                    # Sample users for testing
└── README.md                    # This file
```

## Database Schema

### Users Table
- `username` (Primary Key)
- `hashed_password`
- `role` (client/support)

### Client Query Table
- `query_id` (Primary Key)
- `mail_id`
- `mobile_number`
- `query_heading`
- `query_description`
- `status` (Open/Closed)
- `query_created_date`
- `query_closed_date`
- `user_id` (Foreign Key)

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install streamlit pandas mysql-connector-python
   ```

2. **Configure Database**
   - Create a MySQL database named `client_query_management`
   - Update the `DB_CONFIG` in `db.py` with your MySQL credentials:
     ```python
     DB_CONFIG = {
         "host": "localhost",
         "user": "your_username",
         "password": "your_password",
         "database": "client_query_management"
     }
     ```

3. **Create Database Tables**
   
   Run the following SQL statements in your MySQL database:

   ```sql
   -- Users table for authentication
   CREATE TABLE `users` (
     `username` varchar(150) NOT NULL,
     `hashed_password` text,
     `role` varchar(45) DEFAULT NULL,
     PRIMARY KEY (`username`)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci 
   COMMENT='users table for login purpose';

   -- Client query table for storing support tickets
   CREATE TABLE `client_query` (
     `query_id` int NOT NULL AUTO_INCREMENT,
     `mail_id` varchar(100) DEFAULT NULL,
     `mobile_number` varchar(10) DEFAULT NULL,
     `query_heading` text,
     `query_description` text,
     `status` varchar(10) DEFAULT NULL,
     `query_created_date` date DEFAULT NULL,
     `query_closed_date` date DEFAULT NULL,
     `query_created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
     `query_closed_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
     `user_id` varchar(150) DEFAULT NULL,
     PRIMARY KEY (`query_id`),
     KEY `fk_user_id_idx` (`user_id`),
     CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`username`)
   ) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci 
   COMMENT='client query are stored here';
   ```

4. **Import Sample Users (Optional)**
   
   The project includes a `users.csv` file with pre-configured test users. Import it using MySQL:

   ```sql
   LOAD DATA INFILE '/path/to/users.csv'
   INTO TABLE users
   FIELDS TERMINATED BY ','
   ENCLOSED BY '"'
   LINES TERMINATED BY '\n'
   IGNORE 1 ROWS
   (username, hashed_password, role, @dummy);
   ```

   Or use MySQL Workbench's Table Data Import Wizard to import the CSV file.

   **Test User Credentials:**
   | Username | Password | Role |
   |----------|----------|------|
   | divya | divya@26 | client |
   | kevin@21 | kevin@2025 | client |
   | ram | ram@2022 | client |
   | rajan@ | rajan@thfg | support |
   | ramana | r@cjstyy | support |
   | ramesh@03 | k@chennai | support |

5. **Run the Application**
   ```bash
   streamlit run main.py
   ```

## Usage

1. **First Time Setup**
   - Use the "Create a test user" expander on the login page to create users
   - Create both client and support users for testing

2. **Client Workflow**
   - Login with client credentials
   - Click "➕ Add New Query" to create a new support ticket
   - Fill in email, phone, title, and description
   - View and filter your queries

3. **Support Workflow**
   - Login with support credentials
   - View all customer queries
   - Select an open query and click "Close" to resolve it
   - Filter queries by status

## Form Validation

- **Email**: Must be in valid email format (user@domain.com)
- **Phone**: Must be exactly 10 digits
- **Title**: Required field, max 250 characters
- **Description**: Required field, max 400 characters

## Course Project

This application was developed as a course project to demonstrate:
- Full-stack web application development with Streamlit
- Database integration and CRUD operations
- Role-based access control
- Form validation and user input handling
- Session state management
- Responsive UI design with custom CSS
