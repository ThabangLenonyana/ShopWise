import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Auth.css';
import { register } from '../services/auth.js';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: ''
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [globalError, setGlobalError] = useState('');
  const navigate = useNavigate();

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.username) {
      newErrors.username = 'Username is required';
    } else if (formData.username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters';
    }

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (!formData.firstName) {
      newErrors.firstName = 'First name is required';
    }

    if (!formData.lastName) {
      newErrors.lastName = 'Last name is required';
    }

    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setErrors(prev => ({
      ...prev,
      [name]: ''
    }));
    setGlobalError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validateForm();
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsLoading(true);
    setGlobalError('');

    try {
      const response = await register(
        formData.username,
        formData.email,
        formData.password,
        formData.confirmPassword,
        formData.firstName,
        formData.lastName
      );
      if (response?.data) {
        navigate('/login');
      }
    } catch (error) {
      setGlobalError(
        error.message || 'Registration failed. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <h2>Register</h2>
      <form className="auth-form" onSubmit={handleSubmit}>
        <label>Username</label>
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
          className={errors.username ? 'error' : ''}
          disabled={isLoading}
        />
        {errors.username && <div className="field-error">{errors.username}</div>}
  
        <label>Email</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          className={errors.email ? 'error' : ''}
          disabled={isLoading}
        />
        {errors.email && <div className="field-error">{errors.email}</div>}
  
        <label>Password</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          className={errors.password ? 'error' : ''}
          disabled={isLoading}
        />
        {errors.password && <div className="field-error">{errors.password}</div>}
  
        <label>Confirm Password</label>
        <input
          type="password"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
          className={errors.confirmPassword ? 'error' : ''}
          disabled={isLoading}
        />
        {errors.confirmPassword && <div className="field-error">{errors.confirmPassword}</div>}
  
        <label>First Name</label>
        <input
          type="text"
          name="firstName"
          value={formData.firstName}
          onChange={handleChange}
          className={errors.firstName ? 'error' : ''}
          disabled={isLoading}
        />
        {errors.firstName && <div className="field-error">{errors.firstName}</div>}
  
        <label>Last Name</label>
        <input
          type="text"
          name="lastName"
          value={formData.lastName}
          onChange={handleChange}
          className={errors.lastName ? 'error' : ''}
          disabled={isLoading}
        />
        {errors.lastName && <div className="field-error">{errors.lastName}</div>}
  
        {globalError && <div className="auth-error">{globalError}</div>}
        
        <button type="submit" className="auth-button" disabled={isLoading}>
          {isLoading ? (
            <>
              Registering...
              <span className="loading-spinner"></span>
            </>
          ) : (
            'Register'
          )}
        </button>
      </form>
    </div>
  );
};

export default Register;