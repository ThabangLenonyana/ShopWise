import React, { createContext, useState, useEffect, useContext } from 'react';
import { fetchUserProfile } from '../services/auth.js';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    const loadUserProfile = async () => {
        try {
            const response = await fetchUserProfile();
            setUser(response.data);
        } catch (error) {
            console.error('Failed to load user profile', error);
            setUser(null);
        }
    }

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            loadUserProfile();
        }
    }, []);

    const login = (userData, token) => {
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(userData));
        setUser(userData);
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loadUserProfile }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);