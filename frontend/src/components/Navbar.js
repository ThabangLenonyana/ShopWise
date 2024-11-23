import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box, Container } from '@mui/material';
import { Link } from 'react-router-dom';
import '../styles/Navbar.css';
import '@fontsource/poppins/700.css';

const Navbar = () => {
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
            <Link to="/" className="navbar-logo" style={{color: 'inherit', textDecoration: 'none' }}>
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
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar;