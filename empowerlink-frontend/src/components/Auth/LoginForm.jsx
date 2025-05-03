// src/components/Auth/LoginForm.jsx

import React, { useState } from 'react';
import "./LoginForm.css";
import { gql, useMutation } from '@apollo/client';
import { useNavigate, Link } from 'react-router-dom';

const SIGNIN_ORG = gql`
  mutation SigninOrganization($email: String!, $password: String!) {
    signinOrganization(email: $email, password: $password) {
      access_token
      token_type
    }
  }
`;

export default function LoginForm() {
  const navigate = useNavigate();
  const [creds, setCreds] = useState({ email: '', password: '' });
  const [formError, setFormError] = useState(null);

  const [signin, { loading }] = useMutation(SIGNIN_ORG, {
    onCompleted(data) {
      const payload = data.signinOrganization;
      if (!payload?.access_token) {
        setFormError('Invalid email or password.');
        return;
      }
      localStorage.setItem('authToken', payload.access_token);
      navigate('/');
    },
    onError(err) {
      setFormError(err.message);
    }
  });

  const handleChange = (e) =>
    setCreds((prev) => ({ ...prev, [e.target.name]: e.target.value }));

  const handleSubmit = (e) => {
    e.preventDefault();
    setFormError(null);
    signin({ variables: creds });
  };

  return (
    <div className="auth-form">
      <h2 className="auth-form__title">EmpowerLink Nexus</h2>
      <form onSubmit={handleSubmit}>
        <div className="auth-form__group">
          <label>Email Address</label>
          <input
            type="email"
            name="email"
            value={creds.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="auth-form__group">
          <label>Password</label>
          <input
            type="password"
            name="password"
            value={creds.password}
            onChange={handleChange}
            required
          />
        </div>
        {formError && <p className="auth-form__error">{formError}</p>}
        <button
          type="submit"
          disabled={loading}
          className="auth-form__button"
        >
          {loading ? 'Logging in…' : 'Log In'}
        </button>
      </form>
      <p className="auth-form__footer">
        New organization?{' '}
        <Link to="/signup">Sign up here</Link>
      </p>
    </div>
  );
}

