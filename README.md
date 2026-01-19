# Stock Data Intelligence

## DESIGN
![system design](screenshots/infra-design.png)

## SWAGGER DOC
![swagger doc](screenshots/swagger-doc.png)

## UI
![ui](screenshots/stock-ui.png)

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- Git

### Backend Setup (Python/FastAPI)

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirment.txt
   ```

5. Run the backend server:
   ```
   uvicorn app.main:app --reload
   ```

The backend will be running on `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

### Frontend Setup (React/Vite)

1. Navigate to the client directory:
   ```
   cd client
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

The frontend will be running on `http://localhost:5173`.

### Running the Application

1. Start the backend server first (as described above).
2. Start the frontend development server (as described above).
3. Open your browser and navigate to `http://localhost:5173` to access the application.

The backend API is configured to allow requests from the frontend running on port 5173.
