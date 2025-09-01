import { BrowserRouter as Router, Routes, Route } from "react-router"

import Login from "./pages/Login"
import Register from "./pages/Register"
import Dashboard from "./pages/Dashboard"

function App() {
  return (
    <Router>
      <Routes>
        <Route index element={<Login />}/>
        <Route path="/register" element={<Register />}/>

        <Route path="projects" element={<Dashboard />} />
      </Routes>
    </Router>
  )
}

export default App
