import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Pages 
// import Home from "./pages/Home";
// import FavoriteRestaurant from "./pages/FavoriteRestaurant";
import Login from "./pages/Login";

// import RestaurantInfo from "./pages/RestaurantInfo";
// import Review from "./pages/Review";
// import SignUp from "./pages/SignUp";
// import UserInfo from "./pages/UserInfo";

function App() {
  const [count, setCount] = useState(0)

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App
