# Placement Portal Frontend

A modern, responsive Vue.js frontend for the Placement Portal Application.

## Tech Stack

- **Framework**: Vue 3
- **Routing**: Vue Router
- **State Management**: Pinia
- **Styling**: Bootstrap 5
- **Charts**: Chart.js
- **HTTP Client**: Axios
- **Build Tool**: Vite

## Features

- Modern responsive UI with Bootstrap 5
- Role-based authentication (Admin, Company, Student)
- Real-time dashboard with statistics
- Chart visualizations using Chart.js
- PWA support with offline capabilities
- Mobile-first responsive design

## Project Structure

```
src/
├── components/          # Reusable components
├── layouts/             # Layout components
├── views/               # Page components
├── services/            # API services
├── stores/              # Pinia stores
├── router/              # Vue Router
├── App.vue              # Root component
└── main.js              # Entry point
```

## Setup Instructions

### Prerequisites

- Node.js (v20.19.0 or higher)
- npm or yarn
- Backend server running on http://localhost:5000

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The application will run on `http://localhost:5173`

3. Build for production:
```bash
npm run build
```

## User Roles

### Admin
- View dashboard with statistics
- Approve/reject companies
- Approve placement drives

### Company
- Create placement drives
- View applications
- Shortlist/select/reject candidates

### Student
- Browse eligible placement drives
- Apply to drives
- Track application status
- Manage profile

## API Integration

Backend API: `http://localhost:5000`

JWT tokens stored in localStorage with automatic injection.

## Browser Support

- Chrome, Firefox, Safari, Edge (latest versions)

## PWA Features

- Offline support
- Add to Home Screen
- Native-like experience

## License

College Project
