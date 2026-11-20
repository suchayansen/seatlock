# seatlock
# Event Management & Booking Platform

A web-based event management platform designed to simplify event creation, management, discovery, and booking. The platform provides dedicated dashboards for Students, Organisers, and Administrators, allowing each role to access features according to their permissions.

## 🚀 Features

### 👨‍🎓 Student Dashboard
- Student registration and login.
- Browse available events.
- View event details.
- Book seats for available events.
- View previously booked events.
- Access personal booking history.
- Manage student account.

### 🧑‍💼 Organiser Dashboard
- Organiser authentication.
- Create and publish events.
- Manage existing events.
- View event bookings.
- Monitor student registrations.
- Manage event information.

### 🛡️ Admin Dashboard
- Dedicated administrator login.
- Centralized platform management.
- Manage students and organisers.
- Monitor events and activities.
- Access administrative dashboard features.

### 🔐 Authentication & Authorization
- Role-based login system.
- Separate access for Students, Organisers, and Admins.
- Session-based authentication.
- Protected dashboards.
- Logout functionality.
- User-specific booking history.
- Booking records associated with the respective student account.

## 🛠️ Technology Stack

### Frontend
- React.js
- Vite
- JavaScript
- HTML5
- CSS3

### Backend
- Python
- Flask
- REST API

### Development Tools
- Visual Studio Code
- Git
- GitHub
- npm

## 📁 Project Structure

```text
Event-Management-Platform/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── models/
│   └── requirements.txt
│
└── README.md
```

*Note: Adjust the folder structure above to match your actual repository.*

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd Event-Management-Platform
```

### 2. Setup Frontend

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

### 3. Configure Vite Proxy

Configure your `vite.config.js` to connect the React frontend with the Flask backend.

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    strictPort: true,
    proxy: {
      '/login': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },
      '/logout': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },
      '/dashboard': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },
      '/student': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },
      '/organizer': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },
      '/admin': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      }
    }
  }
})
```

### 4. Run Frontend

```bash
npm run dev
```

Frontend will be available at:

```text
http://localhost:3000
```

### 5. Setup Backend

Open another terminal and navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows:**

```bash
venv\Scripts\activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

### 6. Run Flask Backend

```bash
python app.py
```

Backend will run at:

```text
http://127.0.0.1:5000
```

## 🔄 Application Architecture

The application follows a frontend-backend architecture.

```text
              USER
                |
                v
       React + Vite Frontend
          (Port 3000)
                |
                v
          Vite Proxy
                |
                v
         Flask Backend
          (Port 5000)
                |
                v
       Application Logic
                |
                v
       Database / Storage
```

### User Roles

| Role | Access |
|------|--------|
| Student | Browse events and book seats |
| Organiser | Create and manage events |
| Admin | Manage and monitor the platform |

## 🔑 Application Workflow

1. Users access the platform.
2. Users log in using their respective credentials.
3. The backend authenticates the user.
4. Based on the user's role, the appropriate dashboard is displayed.
5. Students can explore and book events.
6. Organisers can create and manage events.
7. Administrators can oversee platform activities.
8. Booking information is maintained for the respective student account.

## 🧪 Running the Project

You need two separate terminals:

**Terminal 1 – Frontend**

```bash
cd frontend
npm run dev
```

**Terminal 2 – Backend**

```bash
cd backend
venv\Scripts\activate
python app.py
```

## 🔮 Future Enhancements

- Online payment gateway integration.
- QR-based event tickets.
- Email notifications and booking confirmations.
- Event analytics and reporting.
- Advanced event search and filtering.
- Event feedback and rating system.
- Deployment on cloud infrastructure.

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Commit your changes.
5. Push to your branch.
6. Submit a Pull Request.

## 📄 License

This project is developed for educational and demonstration purposes. Licensing can be updated according to the project's distribution requirements.

---

**Developed with ❤️ using React.js and Flask.**
