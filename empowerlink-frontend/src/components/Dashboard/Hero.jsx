// src/components/Dashboard/Hero.jsx
import React from 'react';
import './Hero.css';

export default function Hero({ title, subtitle, children }) {
  return (
    <section className="dashboard-hero">
      <div className="hero-content">
        <h1 className="hero-title">{title}</h1>
        <p className="hero-subtitle">{subtitle}</p>
      </div>
      {children && (
        <div className="hero-extra">
          {children}
        </div>
      )}
    </section>
  );
}

