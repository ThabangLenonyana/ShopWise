import React, { useState } from 'react';
import { useAuth } from '../context/authContext';
import { useNavigate } from 'react-router-dom';
import { 
  Box,
  Button,
  TextField,
  Link,
  Typography,
  Grid,
  Card as MuiCard,
  styled,
  FormControl,
  FormLabel,
} from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import SecurityOutlinedIcon from '@mui/icons-material/SecurityOutlined';
import StarOutlineIcon from '@mui/icons-material/StarOutline';
import '../styles/Auth.css';
import { loginUser } from '../services/auth.js';

const Card = styled(MuiCard)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  width: '100%',
  maxWidth: '400px',
  padding: theme.spacing(4),
  gap: theme.spacing(2),
  boxShadow: 'rgba(0, 0, 0, 0.1) 0px 4px 12px',
  margin: ' auto',
}));

const LoginContainer = styled(Box)(({ theme }) => ({
  minHeight: '100vh',
  padding: theme.spacing(0, 2),
  backgroundColor: '#f5f5f5',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  [theme.breakpoints.down('md')]: {
    padding: theme.spacing(0, 2),
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

const Login = () => {
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [globalError, setGlobalError] = useState('');
  const navigate = useNavigate();

  const validateForm = () => {
    const newErrors = {};
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
    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear errors when user starts typing
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
      const response = await loginUser(formData.email, formData.password);
      if (response?.data) {
        login(response.data.user, response.data.access);
        navigate('/');
      }
    } catch (error) {
      setGlobalError(
        error.message || 'Login failed. Please check your credentials.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <LoginContainer>
      <Grid container spacing={4} maxWidth="1200px" sx={{ margin: '0 auto' }}>
        <Grid item xs={12} md={6}>
          <Box sx={{ pr: {md: 4} }}>
            <Typography variant="h3" gutterBottom color="primary.main" sx={{ mb: 4 }}>
              Welcome Back
            </Typography>
            
            <BenefitItem
              icon={<SecurityOutlinedIcon />}
              title="Secure Login"
              description="Your data is protected with industry-standard encryption."
            />
            
            <BenefitItem
              icon={<LockOutlinedIcon />}
              title="Access Your Account"
              description="View your orders, manage your profile, and check your rewards."
            />

            <BenefitItem
              icon={<StarOutlineIcon />}
              title="Personalized Experience"
              description="Get customized product recommendations and tailored shopping insights."
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
              Login
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
                <FormLabel htmlFor="password">Password</FormLabel>
                <TextField
                  required
                  fullWidth
                  name="password"
                  type="password"
                  id="password"
                  placeholder="••••••"
                  autoComplete="current-password"
                  value={formData.password}
                  onChange={handleChange}
                  error={!!errors.password}
                  helperText={errors.password}
                />
              </FormControl>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                disabled={isLoading}
              >
                {isLoading ? 'Logging in...' : 'Login'}
              </Button>
            </Box>
            <Typography sx={{ textAlign: 'center', mt: 2 }}>
              Don't have an account?{' '}
              <Link href="/register" variant="body2">
                Sign up
              </Link>
            </Typography>
          </Card>
        </Grid>
      </Grid>
    </LoginContainer>
  );
};

export default Login;