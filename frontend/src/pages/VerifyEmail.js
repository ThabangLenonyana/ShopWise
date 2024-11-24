import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { verifyEmail } from '../services/auth';
import { 
  Box, 
  Typography, 
  CircularProgress,
  Container,
  Paper
} from '@mui/material';

const VerifyEmail = () => {
  const { token } = useParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState('verifying');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const verify = async () => {
      try {
        const response = await verifyEmail(token);
        setStatus('success');
        setMessage(response.data.message);
        setTimeout(() => {
          navigate('/login');
        }, 3000);
      } catch (error) {
        setStatus('error');
        setMessage(error.message);
      }
    };

    if (token) {
      verify();
    }
  }, [token, navigate]);

  return(
    <Container maxWidth="sm">
    <Box sx={{ mt: 8 }}>
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        {status === 'verifying' && (
          <>
            <CircularProgress sx={{ mb: 2 }} />
            <Typography>Verifying your email...</Typography>
          </>
        )}
        
        {status === 'success' && (
          <>
            <Typography variant="h5" color="primary" gutterBottom>
              Email Verified Successfully!
            </Typography>
            <Typography>
              {message}
            </Typography>
            <Typography sx={{ mt: 2 }}>
              Redirecting to login page...
            </Typography>
          </>
        )}
        
        {status === 'error' && (
          <>
            <Typography variant="h5" color="error" gutterBottom>
              Verification Failed
            </Typography>
            <Typography>
              {message}
            </Typography>
          </>
        )}
      </Paper>
    </Box>
  </Container>
  )
};

export default VerifyEmail;