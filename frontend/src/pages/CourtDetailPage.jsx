import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { createBooking, getAvailability, getCourt } from "../api.js";
import { getUserId } from "../userId.js";

function todayAsInputValue() {
  return new Date().toISOString().slice(0, 10);
}

function formatSlotTime(isoString) {
  return new Date(isoString).toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit",
  });
}

function CourtDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const userId = getUserId();

  const [court, setCourt] = useState(null);
  const [date, setDate] = useState(todayAsInputValue());
  const [slots, setSlots] = useState([]);
  const [selectedSlots, setSelectedSlots] = useState([]);
  const [error, setError] = useState("");
  const [booking, setBooking] = useState(false);

  useEffect(() => {
    getCourt(id).then(setCourt);
  }, [id]);

  useEffect(() => {
    setSelectedSlots([]);
    getAvailability(id, date).then(setSlots);
  }, [id, date]);

  function toggleSlot(slot) {
    if (!slot.available) return;
    const isSelected = selectedSlots.some(
      (s) => s.start_timestamp === slot.start_timestamp
    );
    if (isSelected) {
      setSelectedSlots(
        selectedSlots.filter((s) => s.start_timestamp !== slot.start_timestamp)
      );
    } else {
      setSelectedSlots([...selectedSlots, slot]);
    }
  }

  async function handleBook() {
    setError("");
    setBooking(true);
    try {
      for (const slot of selectedSlots) {
        await createBooking({
          user_id: userId,
          court_id: Number(id),
          start_timestamp: slot.start_timestamp,
          end_timestamp: slot.end_timestamp,
        });
      }
      navigate("/bookings");
    } catch (err) {
      setError(err.message);
      getAvailability(id, date).then(setSlots);
      setSelectedSlots([]);
    } finally {
      setBooking(false);
    }
  }

  if (!court) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <Link to="/" className="back-link">
        &larr; Back to courts
      </Link>

      <div className="court-detail-header">
        <img src={court.image} alt={court.name} />
        <div className="court-detail-body">
          <span className="court-type">{court.type}</span>
          <h1>{court.name}</h1>
          <p>
            {court.address_1}
            {court.address_2 ? `, ${court.address_2}` : ""}
            <br />
            {court.city}, {court.state} {court.zipcode}
          </p>
          <p>Hours: {court.hours_of_operation}</p>
        </div>
      </div>

      <h2>Select a date</h2>
      <input
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
      />

      <h2>Available time slots</h2>
      <div className="slot-grid">
        {slots.map((slot) => {
          const isSelected = selectedSlots.some(
            (s) => s.start_timestamp === slot.start_timestamp
          );
          return (
            <button
              key={slot.start_timestamp}
              type="button"
              className={`slot-button${isSelected ? " selected" : ""}`}
              disabled={!slot.available}
              onClick={() => toggleSlot(slot)}
            >
              {formatSlotTime(slot.start_timestamp)}
            </button>
          );
        })}
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <button
        type="button"
        disabled={selectedSlots.length === 0 || booking}
        onClick={handleBook}
      >
        {booking
          ? "Booking..."
          : `Book ${selectedSlots.length || ""} slot${
              selectedSlots.length === 1 ? "" : "s"
            }`.trim()}
      </button>
    </div>
  );
}

export default CourtDetailPage;
