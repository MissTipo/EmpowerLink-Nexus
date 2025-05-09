import React from "react";
import Dashboard from "../components/Dashboard/Dashboard";
import USSDDialer from "../components/USSD/USSDDialer";
import "./DashboardPage.css";   // wrapper styles

export default function DashboardPage() {
  return (
    <div className="dashboard-page" style={{ display: "flex", height: "100vh" }}>
      <div style={{ flex: 1, overflowY: "auto" }}>
        <Dashboard />
      </div>
      <div style={{ width: "400px" }}>
        <USSDDialer />
      </div>
    </div>
  );
}

