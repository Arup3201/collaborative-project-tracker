import { BrowserRouter as Router, Routes, Route } from "react-router"

import Login from "./pages/Login"
import Register from "./pages/Register"

function App() {
  return (
    <Router>
      <Routes>
        <Route index element={<Login />}/>
        <Route path="/register" element={<Register />}/>
      </Routes>
    </Router>
  )
}

export default App
