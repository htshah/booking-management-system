import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getBookings } from "../api.js";
import { getUserId } from "../userId.js";

function BookingsTable({ bookings }) {
  if (bookings.length === 0) {
    return <p>No bookings here yet.</p>;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>Court</th>
          <th>Start</th>
          <th>End</th>
        </tr>
      </thead>
      <tbody>
        {bookings.map((booking) => (
          <tr key={booking.id}>
            <td>{booking.court.name}</td>
            <td>{new Date(booking.start_timestamp).toLocaleString()}</td>
            <td>{new Date(booking.end_timestamp).toLocaleString()}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function BookingsPage() {
  const userId = getUserId();
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    getBookings(userId).then(setBookings);
  }, []);

  const now = new Date();
  const upcoming = bookings
    .filter((b) => new Date(b.end_timestamp) >= now)
    .sort((a, b) => new Date(a.start_timestamp) - new Date(b.start_timestamp));
  const past = bookings
    .filter((b) => new Date(b.end_timestamp) < now)
    .sort((a, b) => new Date(b.start_timestamp) - new Date(a.start_timestamp));

  return (
    <div>
      <h1>My Bookings</h1>
      <p className="user-id-note">Your user ID: {userId}</p>
      <p>
        Want to book a court? <Link to="/">Browse available courts</Link>.
      </p>

      <h2>Upcoming</h2>
      <BookingsTable bookings={upcoming} />

      <h2>Past</h2>
      <BookingsTable bookings={past} />
    </div>
  );
}

export default BookingsPage;
