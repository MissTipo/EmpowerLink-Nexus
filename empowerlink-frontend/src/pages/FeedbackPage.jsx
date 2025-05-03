import React from 'react';
import './FeedbackPage.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCommentDots } from '@fortawesome/free-solid-svg-icons';

export default function FeedbackPage() {
  const feedbacks = [
    { id: 1, message: "Great initiative! Would love to see more workshops.", sender: "Jane Doe", date: "2025-04-01", status: "Reviewed" },
    { id: 2, message: "Need a feature for anonymous feedback.", sender: "Ali Mwangi", date: "2025-03-29", status: "Pending" },
    { id: 3, message: "Platform feels fast and intuitive.", sender: "Elodie K.", date: "2025-03-22", status: "Reviewed" },
  ];

  return (
    <div className="feedback-page">
      <div className="page-title">
        <h1>User Feedback</h1>
      </div>

      <div className="feedback-list">
        {feedbacks.map((item) => (
          <div className="feedback-card" key={item.id}>
            <FontAwesomeIcon icon={faCommentDots} className="feedback-icon" />
            <div className="feedback-details">
              <p className="message">"{item.message}"</p>
              <div className="meta">
                <span className="sender">{item.sender}</span>
                <span className="date">{item.date}</span>
              </div>
            </div>
            <span className={`status-badge ${item.status.toLowerCase()}`}>
              {item.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

