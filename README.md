# Blood Bridge Project

## Overview
Blood Bridge is a full-stack application designed to facilitate blood donation and requests. It consists of a Django backend API and a React Native frontend mobile app built with Expo.

## Backend

The backend is built with Django 5.2 and Django REST Framework. It provides RESTful APIs for managing donors, recipients, and blood requests. The backend uses token-based authentication and SQLite as the database.

### Setup and Run

1. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate      # On macOS/Linux
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply migrations:

```bash
python manage.py migrate
```

4. Run the development server:

```bash
python manage.py runserver
```

The backend server will be available at `http://localhost:8000`.

## Frontend

The frontend is a React Native app built with Expo. It provides user interfaces for donors and recipients to interact with the Blood Bridge system.

### Setup and Run

1. Install Node.js and Yarn if not already installed.

2. Install Expo CLI globally (if not installed):

```bash
npm install -g expo-cli
```

3. Navigate to the frontend directory:

```bash
cd blood-bridge-js
```

4. Install dependencies:

```bash
yarn install
```

5. Start the Expo development server:

```bash
yarn start
```

6. Run the app on your device or emulator:

- For Android:

```bash
yarn android
```

- For iOS:

```bash
yarn ios
```

- For Web:

```bash
yarn web
```

## Configuration

- The backend allows CORS from the frontend origin for development.
- The backend uses a custom user model `Donor`.
- The frontend communicates with the backend API for authentication and data.

## Contributing

Contributions are welcome. Please fork the repository and create pull requests for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
