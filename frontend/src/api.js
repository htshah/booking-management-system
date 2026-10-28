const API_BASE_URL = "http://localhost:8000";

export async function getCourts() {
  const res = await fetch(`${API_BASE_URL}/courts`);
  return res.json();
}

export async function getCourt(courtId) {
  const res = await fetch(`${API_BASE_URL}/courts/${courtId}`);
  return res.json();
}

export async function getAvailability(courtId, date) {
  const res = await fetch(
    `${API_BASE_URL}/courts/${courtId}/availability?date=${date}`
  );
  return res.json();
}

export async function getBookings(userId) {
  const res = await fetch(`${API_BASE_URL}/bookings?user_id=${userId}`);
  return res.json();
}

export async function createBooking(booking) {
  const res = await fetch(`${API_BASE_URL}/bookings`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(booking),
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Failed to create booking");
  }
  return res.json();
}
