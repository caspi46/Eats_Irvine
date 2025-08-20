import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Pages 
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Review from "./pages/Review";

// import Home from "./pages/Home";
// import FavoriteRestaurant from "./pages/FavoriteRestaurant";
// import RestaurantInfo from "./pages/RestaurantInfo";
// import UserInfo from "./pages/UserInfo";

function App() {
  const [count, setCount] = useState(0)

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/review" element={<Review />} />
      </Routes>
    </Router>
  );
}

export default App
