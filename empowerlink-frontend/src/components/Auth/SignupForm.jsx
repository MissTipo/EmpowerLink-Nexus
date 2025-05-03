// src/components/Auth/SignupForm.jsx

import React, { useState } from 'react';
import "./LoginForm.css";        // reusing the auth-form styles
import { gql, useMutation } from '@apollo/client';
import { useNavigate, Link } from 'react-router-dom';

const SIGNUP_ORG = gql`
  mutation SignupOrganization($input: OrganizationInput!) {
    signupOrganization(input: $input) {
      id
      name
      email
      phone
      location
      role
    }
  }
`;

export default function SignupForm() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
    phone: '',
    location: '',
    role: 'Organization',
  });
  const [signup, { loading, error }] = useMutation(SIGNUP_ORG, {
    onError(err) {
      console.error(err.networkError?.result || err);
    },
    onCompleted() {
      navigate('/login');
    },
  });

  const handleChange = (e) =>
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));

  const handleSubmit = (e) => {
    e.preventDefault();
    signup({ variables: { input: form } });
  };

  return (
    <div className="auth-form">
      <h2 className="auth-form__title">Sign Up (Organization)</h2>
      <form onSubmit={handleSubmit}>
        {['name', 'email', 'password', 'phone', 'location', 'role'].map((field) => (
          <div className="auth-form__group" key={field}>
            <label>
              {field.charAt(0).toUpperCase() + field.slice(1)}
            </label>
            {field === 'role' ? (
              <select
                name="role"
                value={form.role}
                onChange={handleChange}
              >
                <option value="Organization">Organization</option>
                <option value="NonProfit">NonProfit</option>
                <option value="NGO">NGO</option>
              </select>
            ) : (
              <input
                type={field === 'password' ? 'password' : 'text'}
                name={field}
                value={form[field]}
                onChange={handleChange}
                required={['name', 'email', 'password'].includes(field)}
              />
            )}
          </div>
        ))}

        {error && <p className="auth-form__error">{error.message}</p>}

        <button
          type="submit"
          disabled={loading}
          className="auth-form__button"
        >
          {loading ? 'Signing up…' : 'Sign Up'}
        </button>
      </form>

      <p className="auth-form__footer">
        Already registered?{' '}
        <Link to="/login">Log in</Link>
      </p>
    </div>
  );
}

