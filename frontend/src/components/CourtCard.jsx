import { Link } from "react-router-dom";

function CourtCard({ court }) {
  return (
    <Link to={`/courts/${court.id}`} className="court-card">
      <img src={court.image} alt={court.name} />
      <div className="court-card-body">
        <span className="court-type">{court.type}</span>
        <h3>{court.name}</h3>
        <p>
          {court.address_1}
          {court.address_2 ? `, ${court.address_2}` : ""}
          <br />
          {court.city}, {court.state} {court.zipcode}
        </p>
        <p>Hours: {court.hours_of_operation}</p>
      </div>
    </Link>
  );
}

export default CourtCard;
