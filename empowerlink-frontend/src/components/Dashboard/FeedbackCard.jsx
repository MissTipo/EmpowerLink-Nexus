import React from 'react';
import './FeedbackCard.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSmile, faFrown, faMeh } from '@fortawesome/free-regular-svg-icons';

export default function FeedbackCard() {
  const handleFeedback = (type) => {
    alert(`You selected: ${type}`);
    // Optional: send feedback to backend here
  };

  return (
    <div className="feedback-card">
      <h3 className="feedback-title">Your Experience Matters</h3>
      <p className="feedback-subtitle">How would you rate your experience?</p>
      <div className="feedback-buttons">
        <button className="feedback-btn" onClick={() => handleFeedback('Good')}>
          <FontAwesomeIcon icon={faSmile} className="icon good" />
          Good
        </button>
        <button className="feedback-btn" onClick={() => handleFeedback('Neutral')}>
          <FontAwesomeIcon icon={faMeh} className="icon neutral" />
          Neutral
        </button>
        <button className="feedback-btn" onClick={() => handleFeedback('Bad')}>
          <FontAwesomeIcon icon={faFrown} className="icon bad" />
          Bad
        </button>
      </div>
    </div>
  );
}

