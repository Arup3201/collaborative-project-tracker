import { BrowserRouter as Router, Routes, Route } from "react-router";

import { AuthProvider } from "./contexts/auth-context";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Project from "./pages/Project";

function App() {
  return (
    <AuthProvider>
      <Router>
      <Routes>
        <Route index element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route path="/projects" element={<Dashboard />} />
        <Route path="/projects/:id" element={<Project />} />
      </Routes>
    </Router>
    </AuthProvider>
  );
}

export default App;
