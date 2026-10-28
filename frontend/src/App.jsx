import { Link, Route, Routes } from "react-router-dom";

import BookingsPage from "./pages/BookingsPage.jsx";
import CourtsPage from "./pages/CourtsPage.jsx";

function App() {
  return (
    <div>
      <nav>
        <Link to="/">Courts</Link>
        <Link to="/bookings">My Bookings</Link>
      </nav>
      <div className="container">
        <Routes>
          <Route path="/" element={<CourtsPage />} />
          <Route path="/bookings" element={<BookingsPage />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
