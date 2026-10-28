import { useEffect, useState } from "react";

import { getCourts } from "../api.js";
import CourtCard from "../components/CourtCard.jsx";

function CourtsPage() {
  const [courts, setCourts] = useState([]);

  useEffect(() => {
    getCourts().then(setCourts);
  }, []);

  return (
    <div>
      <h1>Available Courts</h1>
      <div className="court-grid">
        {courts.map((court) => (
          <CourtCard key={court.id} court={court} />
        ))}
      </div>
    </div>
  );
}

export default CourtsPage;
