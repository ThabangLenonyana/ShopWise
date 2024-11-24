import { useState, useEffect } from 'react';
import { fetchUserProfile, updateUserProfile } from '../services/auth.js';
import '../styles/Profile.css';

import { 
    TextField, 
    Button, 
    Avatar, 
    Container, 
    Typography, 
    Box, 
    Grid,
    Alert, 
    Paper } 
from '@mui/material';

const Profile = () => {
    const [profileData, setProfileData] = useState({
        email: '',
        username: '', 
        first_name: '',
        last_name: '',
        avatar: '',
        postal_code: '',
        suburb: '',
        phone_number: '',
        current_password: '',
        new_password: '',
        confirm_password: '',
    });

    const [initialProfileData, setInitialProfileData] = useState({
        email: '',
        username: '',
        first_name: '',
        last_name: '',
        avatar: '',
        postal_code: '',
        suburb: '',
        phone_number: '',
        current_password: '',
        new_password: '',
        confirm_password: '',
    });

    const [errors, setErrors] = useState({});
    const [isLoading, setIsLoading] = useState(false);
    const [isSuccess, setIsSuccess] = useState(false);
    const [globalError, setGlobalError] = useState('');
    const [avatarPreview, setAvatarPreview] = useState('');

    useEffect(() => {
        const loadUserProfile = async () => {
            try {
                const response = await fetchUserProfile();
                    setProfileData(response.data);
                    setInitialProfileData(response.data);
                    setAvatarPreview(response.data.avatar);
            } catch (error) {
                setGlobalError(error.message || 'Failed to load profile data');
            }
        };

        loadUserProfile();
    }, []);

    const validateForm = () => {
        const newErrors = {};

        if (!profileData.username?.trim()) {
        newErrors.username = 'Username is required';
        } else if (profileData.username.length < 3) {
        newErrors.username = 'Username must be at least 3 characters';
        }
    
        // Name validations
        if (!profileData.first_name?.trim()) {
        newErrors.first_name = 'First name is required';
        }
        if (!profileData.last_name?.trim()) {
        newErrors.last_name = 'Last name is required';
        }
    
        // Phone number validation
        if (profileData.phone_number && !/^\d{10}$/.test(profileData.phone_number)) {
        newErrors.phone_number = 'Please enter a valid 10-digit phone number';
        }
    
        // Postal code validation
        if (profileData.postal_code && !/^\d{4,5}$/.test(profileData.postal_code)) {
        newErrors.postal_code = 'Please enter a valid postal code';
        }
    
        // Password validation
        if (profileData.new_password && !profileData.current_password) {
        newErrors.current_password = 'Current password is required to set new password';
        }
        if (profileData.new_password && profileData.new_password.length < 6) {
        newErrors.new_password = 'New password must be at least 6 characters';
        }
    
        return newErrors;
        };
    

    const handleChange = (e) => {
        const { name, value } = e.target;
        setProfileData(prev => ({
            ...prev,
            [name]: value
        }));
        setErrors(prev => ({
            ...prev,
            [name]: ''
        }));
        setGlobalError('');
        };

    const handleAvatarChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            // Validate file type
            const validTypes = ['image/jpeg', 'image/png', 'image/gif'];
            if (!validTypes.includes(file.type)) {
                setGlobalError('Please upload a valid image file (JPEG, PNG, or GIF)');
                return;
            }
                
            // Validate file size (e.g., 5MB max)
            if (file.size > 5 * 1024 * 1024) {
                setGlobalError('Image file size must be less than 5MB');
                return;
            }
                
            setProfileData(prev => ({
                ...prev,
                avatar: file
            }));
            setAvatarPreview(URL.createObjectURL(file));
                
            // Clean up the object URL when component unmounts
            return () => URL.revokeObjectURL(avatarPreview);
        }
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
            const formData = new FormData();
            const changedFields = Object.keys(profileData).filter(key => 
                profileData[key] !== initialProfileData[key] && profileData[key] !== '');
            
            changedFields.forEach(key => {
              if (key === 'avatar' && profileData[key] instanceof File) {
                formData.append('avatar', profileData[key]);
              } else if (profileData[key]) {
                formData.append(key, profileData[key].toString());
              }
            });
            
            // Debugging: log form data
            for (let pair of formData.entries()) {
              console.log(pair[0], pair[1]);
            }

            await updateUserProfile(formData);
            setIsSuccess(true);
            setTimeout(() => setIsSuccess(false), 3000);
        }   catch (error) {
            setIsSuccess(false);
            setGlobalError(error.message || 'Failed to update profile');
        }   finally {
            setIsLoading(false);
        }
    };

    return (
        <Container maxWidth="sm">
          <Box sx={{ mt: 8 }}>
            <Paper sx={{ p: 4 }}>
              <Typography variant="h4" gutterBottom>
                Edit Profile
              </Typography>
              <form onSubmit={handleSubmit}>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Email"
                      name="email"
                      value={profileData.email}
                      disabled
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Username"
                      name="username"
                      value={profileData.username}
                      onChange={handleChange}
                      error={!!errors.username}
                      helperText={errors.username}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="First Name"
                      name="first_name"
                      value={profileData.first_name}
                      onChange={handleChange}
                      error={!!errors.first_name}
                      helperText={errors.first_name}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Last Name"
                      name="last_name"
                      value={profileData.last_name}
                      onChange={handleChange}
                      error={!!errors.last_name}
                      helperText={errors.last_name}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Postal Code"
                      name="postal_code"
                      value={profileData.postal_code || ''}
                      onChange={handleChange}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="suburb"
                      name="suburb"
                      value={profileData.suburb || ''}
                      onChange={handleChange}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Phone Number"
                      name="phone_number"
                      value={profileData.phone_number || ''}
                      onChange={handleChange}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <input
                      accept="image/*"
                      style={{ display: 'none' }}
                      id="avatar-upload"
                      type="file"
                      onChange={handleAvatarChange}
                    />
                    <label htmlFor="avatar-upload">
                      <Button variant="contained" component="span">
                        Upload Avatar
                      </Button>
                    </label>
                    {avatarPreview && (
                      <Avatar
                        src={avatarPreview}
                        sx={{ width: 56, height: 56, mt: 2 }}
                      />
                    )}
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Current Password"
                      name="current_password"
                      type="password"
                      value={profileData.current_password}
                      onChange={handleChange}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="New Password"
                      name="new_password"
                      type="password"
                      value={profileData.new_password}
                      onChange={handleChange}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Confirm New Password"
                      name="confirm_new_password"
                      type="password"
                      value={profileData.confirm_new_password}
                      onChange={handleChange}
                      error={!!errors.confirm_new_password}
                      helperText={errors.confirm_new_password}
                    />
                  </Grid>

                  {isSuccess && (
                    <Grid item xs={12}>
                        <Alert 
                            severity="success"
                            onClose={() => setIsSuccess(false)}
                            sx={{ mb: 2 }}
                        >
                            Profile updated successfully!
                        </Alert>
                    </Grid>
                  )}

                  {globalError && (
                    <Grid item xs={12}>
                      <Typography color="error">{globalError}</Typography>
                    </Grid>
                  )}
                  <Grid item xs={12}>
                    <Button
                      type="submit"
                      variant="contained"
                      color="primary"
                      fullWidth
                      disabled={isLoading}
                    >
                      {isLoading ? 'Updating...' : 'Update Profile'}
                    </Button>
                  </Grid>
                </Grid>
              </form>
            </Paper>
          </Box>
        </Container>
      );
    };
    export default Profile;