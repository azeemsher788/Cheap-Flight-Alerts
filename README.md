# Cheap-Flight-Alerts

## Overview
Cheap-Flight-Alerts is a Python-based application designed to help users find the cheapest flights available. The application searches for flights from a specified origin city to various destination cities and sends email alerts to users when a cheaper flight is found.

## Features
- **Flight Search**: Searches for both direct and indirect flights.
- **Email Notifications**: Sends email alerts to users when a cheaper flight is found.
- **Data Management**: Manages flight data and user information using Google Sheets.

## Technologies Used
- **Python**: Core programming language.
- **Pandas**: For data manipulation.
- **Requests**: For making HTTP requests to flight search APIs.
- **Smtplib**: For sending emails.
- **Google Sheets API**: For managing flight and user data.

## Data Collection
- **Cities Information**: Cities data is managed using Sheety.
- **User Information**: Customers names and emails are collected through Google Forms.

## Setup Instructions
1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/Cheap-Flight-Alerts.git
    cd Cheap-Flight-Alerts
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    - Create a `.env` file in the root directory.
    - Add the required API keys and other configurations in the `.env` file.

4. **Run the application**:
    ```sh
    python main.py
    ```

## Usage
- The application will automatically search for flights and send email alerts based on the criteria defined in the code.
- Ensure that the Google Sheets are properly set up and accessible via the API.

## Contributing
- Fork the repository.
- Create a new branch (`git checkout -b feature-branch`).
- Commit your changes (`git commit -am 'Add new feature'`).
- Push to the branch (`git push origin feature-branch`).
- Create a new Pull Request.

## License
This project is licensed under the MIT License.