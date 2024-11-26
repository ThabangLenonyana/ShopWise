import { useState } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import MuiCard from '@mui/material/Card';
import { styled } from '@mui/material/styles';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import SecurityOutlinedIcon from '@mui/icons-material/SecurityOutlined';
import SpeedOutlinedIcon from '@mui/icons-material/SpeedOutlined';
import { register as authRegister } from '../services/auth.js';
import { useNavigate } from 'react-router-dom';

const Card = styled(MuiCard)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  width: '100%',
  maxWidth: '400px',
  padding: theme.spacing(4),
  gap: theme.spacing(2),
  boxShadow: 'rgba(0, 0, 0, 0.1) 0px 4px 12px',
  margin: 'auto',
}));

const SignUpContainer = styled(Box)(({ theme }) => ({
  minHeight: '100vh',
  padding: theme.spacing(2),
  backgroundColor: '#f5f5f5',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  [theme.breakpoints.up('sm')]: {
    padding: theme.spacing(4),
  },
}));

const BenefitItem = ({ icon, title, description }) => (
  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2, mb: 4 }}>
    <Box sx={{ 
      p: 1, 
      borderRadius: 1, 
      backgroundColor: 'primary.main',
      color: 'white',
      display: 'flex'
    }}>
      {icon}
    </Box>
    <Box>
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <Typography color="text.secondary">
        {description}
      </Typography>
    </Box>
  </Box>
);

export default function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    password2: '',
    
  });

  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [globalError, setGlobalError] = useState('');

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.email || !/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }
    
    if (!formData.password || formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    
    if (formData.password !== formData.password2) {
      newErrors.password2 = 'Passwords do not match';
    }

    return newErrors;
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
      const response = await authRegister(
        formData.email, 
        formData.username,
        formData.password,
        formData.password2);
        
      if (response?.data) {
        navigate('/login');
      }
    } catch (error) {
      setGlobalError(error.message || 'Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    if (errors[e.target.name]) {
      setErrors({
        ...errors,
        [e.target.name]: ''
      });
    }
  };

  return (
    <SignUpContainer >
      <Grid container spacing={4} maxWidth="1200px" sx={{ margin: '0 auto' }}>
        <Grid item xs={12} md={6}>
          <Box sx = {{ pr: {md: 4} }} >
            <Typography variant="h3" gutterBottom color="primary.main" sx={{ mb: 4 }}>
              Join Our Community
            </Typography>
            
            <BenefitItem
              icon={<SecurityOutlinedIcon />}
              title="Secure Shopping"
              description="Your data is protected with industry-standard encryption and security measures."
            />
            
            <BenefitItem
              icon={<SpeedOutlinedIcon />}
              title="Fast Checkout"
              description="Save your preferences for quick and easy shopping experiences."
            />
            
            <BenefitItem
              icon={<LockOutlinedIcon />}
              title="Private Account"
              description="Manage your orders, returns, and wishlist all in one place."
            />
          </Box>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card variant="outlined">
            <Typography
              component="h1"
              variant="h4"
              sx={{ width: '100%', textAlign: 'center', mb: 3 }}
            >
              Sign up
            </Typography>
            {globalError && (
              <Typography color="error" textAlign="center">
                {globalError}
              </Typography>
            )}
            <Box
              component="form"
              onSubmit={handleSubmit}
              sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}
            >
              <FormControl>
                <FormLabel htmlFor="email">Email</FormLabel>
                <TextField
                  required
                  fullWidth
                  id="email"
                  name="email"
                  placeholder="your@email.com"
                  autoComplete="email"
                  value={formData.email}
                  onChange={handleChange}
                  error={!!errors.email}
                  helperText={errors.email}
                />
                </FormControl>
                <FormControl>
                <FormLabel htmlFor="username">Username</FormLabel>
                <TextField
                  required
                  fullWidth
                  id="email"
                  name="username"
                  placeholder="MyUsername"
                  autoComplete="username"
                  value={formData.username}
                  onChange={handleChange}
                  error={!!errors.email}
                  helperText={errors.email}
                />
                </FormControl>
              <FormControl>
                <FormLabel htmlFor="password">Password</FormLabel>
                <TextField
                  required
                  fullWidth
                  name="password"
                  type="password"
                  id="password"
                  placeholder="••••••"
                  autoComplete="new-password"
                  value={formData.password}
                  onChange={handleChange}
                  error={!!errors.password}
                  helperText={errors.password}
                />
              </FormControl>
              <FormControl>
                <FormLabel htmlFor="password2">Confirm Password</FormLabel>
                <TextField
                  required
                  fullWidth
                  name="password2"
                  type="password"
                  id="password2"
                  placeholder="••••••"
                  value={formData.password2}
                  onChange={handleChange}
                  error={!!errors.password2}
                  helperText={errors.password2}
                />
                </FormControl>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                disabled={isLoading}
              >
                {isLoading ? 'Signing up...' : 'Sign up'}
              </Button>
            </Box>
            <Typography sx={{ textAlign: 'center', mt: 2 }}>
              Already have an account?{' '}
              <Link href="/login" variant="body2">
                Sign in
              </Link>
            </Typography>
          </Card>
        </Grid>
      </Grid>
    </SignUpContainer>
  );
}
