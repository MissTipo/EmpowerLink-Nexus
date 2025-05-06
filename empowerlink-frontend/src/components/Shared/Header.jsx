import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';
import logo from '../../assets/logo.webp';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars } from '@fortawesome/free-solid-svg-icons';

export default function Header() {
  return (
    <header className="header">
      <div className="header__brand">
        <img src={logo} alt="EmpowerLink Nexus" className="header__logo" />
        <h1 className="header__title">ELN</h1>
      </div>
      <nav className="header__nav">
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/resources">Resources</Link>
        <Link to="/reports">Reports</Link>
        <Link to="/feedback">Feedback</Link>
      </nav>
      <button className="header__menu-btn">
        <FontAwesomeIcon icon={faBars} />
      </button>
    </header>
  );
}


// import React from 'react';
// import "./Header.css";
// import { Link, useNavigate } from 'react-router-dom';
//
// export default function Header() {
//   const navigate = useNavigate();
//   const handleLogout = () => {
//     // clear auth token then navigate
//     localStorage.removeItem('authToken');
//     navigate('/login');
//   };
//   return (
//     <header className="header">
//       <Link to="/" className="header__logo">EmpowerLink Nexus</Link>
//       <nav className="header__nav">
//         <Link to="/">Dashboard</Link>
//         <Link to="/resources">Resources</Link>
//         <Link to="/reports">Reports</Link>
//         <Link to="/feedback">Feedback</Link>
//         <button onClick={handleLogout}>Logout</button>
//       </nav>
//     </header>
//   );
// }
