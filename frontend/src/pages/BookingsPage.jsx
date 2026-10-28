import { useEffect, useState } from "react";

import { createBooking, getBookings, getCourts } from "../api.js";
import { getUserId } from "../userId.js";

function BookingsPage() {
  const userId = getUserId();
  const [bookings, setBookings] = useState([]);
  const [courts, setCourts] = useState([]);
  const [courtId, setCourtId] = useState("");
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [error, setError] = useState("");

  function loadBookings() {
    getBookings(userId).then(setBookings);
  }

  useEffect(() => {
    loadBookings();
    getCourts().then(setCourts);
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await createBooking({
        user_id: userId,
        court_id: Number(courtId),
        start_timestamp: start,
        end_timestamp: end,
      });
      setCourtId("");
      setStart("");
      setEnd("");
      loadBookings();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <h1>My Bookings</h1>
      <p className="user-id-note">Your user ID: {userId}</p>

      <form className="booking-form" onSubmit={handleSubmit}>
        <h3>New Booking</h3>
        <label>
          Court
          <select
            value={courtId}
            onChange={(e) => setCourtId(e.target.value)}
            required
          >
            <option value="">Select a court</option>
            {courts.map((court) => (
              <option key={court.id} value={court.id}>
                {court.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Start
          <input
            type="datetime-local"
            value={start}
            onChange={(e) => setStart(e.target.value)}
            required
          />
        </label>
        <label>
          End
          <input
            type="datetime-local"
            value={end}
            onChange={(e) => setEnd(e.target.value)}
            required
          />
        </label>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit">Book</button>
      </form>

      <h3>Past Bookings</h3>
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
    </div>
  );
}

export default BookingsPage;
