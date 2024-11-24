import React, { useState, useEffect } from 'react';
import { AppBar, Toolbar, Typography, Button, Box, Container, Avatar, IconButton, Tooltip, } from '@mui/material';
import LogoutIcon from '@mui/icons-material/Logout';
import { Link, useNavigate } from 'react-router-dom';
import { fetchUserProfile } from '../services/auth.js';
import '../styles/Navbar.css';
import '@fontsource/poppins/700.css';

const Navbar = () => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const loadUserProfile = async () => {
      try {
        const response = await fetchUserProfile();
        setUser(response.data);
      } catch (error) {
        console.error('Failed to load user profile', error);
      }
    }

    const token = localStorage.getItem('token');
    if (token) {
      loadUserProfile();
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    navigate('/');
  };

  return (
    <AppBar
      position="static"
      sx={{
        display: 'flex',
        justifyContent: 'center',
        bgcolor: 'white',
        border: '2.5px solid',
        borderColor: 'primary.main',
        borderRadius: '50px',
        mx: 'auto', // Adjusts horizontal margin if needed
        mt: 2, // Adjusts top margin if needed
        maxWidth: 'lg'
      }}
      elevation={0}
    >
      <Container maxWidth="lg">
        <Toolbar disableGutters>
          <Typography 
            variant="h6" 
            component="div" 
            sx={{ flexGrow: 1,
              fontFamily: 'Poppins, sans-serif',
              fontWeight: 700,
              fontStyle: 'italic',
              color: 'primary.main',
            }}>
            <Link to="/" className="navbar-logo" style={{ color: 'inherit', textDecoration: 'none' }}>
              ShopWise
            </Link>
          </Typography>
          <Box>
            <Button
              variant="text"
              color="primary"
              component={Link}
              to="/products"
              sx={{
                textTransform: 'none',
                fontSize: '14px',
                px: 2,
              }}
            >
              Products
            </Button>
            <Button
              variant="text"
              color="primary"
              component={Link}
              to="/retailers"
              sx={{
                textTransform: 'none',
                fontSize: '14px',
                px: 2,
              }}
            >
              Stores
            </Button>
            <Button
              variant="text"
              color="primary"
              component={Link}
              to="/recommendations"
              sx={{
                textTransform: 'none',
                fontSize: '14px',
                px: 2,
              }}
            >
              Compare
            </Button>
            {user ? (
              <>
                <IconButton
                  color="primary"
                  component={Link}
                  to="/profile"
                  sx={{ textTransform: 'none', fontSize: '14px', px: 2 }}
                >
                  <Avatar
                    src={user.avatar || '/default-avatar.png'}
                    alt={user.username}
                    sx={{ width: 24, height: 24, mr: 1 }}
                  />
                  {user.username}
                </IconButton>
                <Tooltip title="Logout">
                  <IconButton
                    onClick={handleLogout}
                    color="secondary"
                    sx={{
                      ml: 2,
                      '&:hover': {
                        backgroundColor: 'rgba(156, 39, 176, 0.04)', // Light purple hover effect
                        }
                    }}
                  >
                    <LogoutIcon />
                  </ IconButton>
                </Tooltip>
              </>
            ) : (
              <>
                <Button
                  variant="contained"
                  color="secondary"
                  component={Link}
                  to="/register"
                  sx={{
                    textTransform: 'none',
                    fontSize: '14px',
                    px: 2,
                    mr: 1,
                    borderRadius: '25px',
                  }}
                >
                  Sign Up
                </Button>
                <Button
                  variant="outlined"
                  color="secondary"
                  component={Link}
                  to="/login"
                  sx={{
                    textTransform: 'none',
                    fontSize: '14px',
                    px: 2,
                    borderRadius: '25px',
                  }}
                >
                  Login
                </Button>
              </>
            )}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar;