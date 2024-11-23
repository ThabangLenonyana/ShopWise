import React from 'react';
import { 
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Stack,
  Paper,
  Divider,
  TextField,
  IconButton,
  Link
} from '@mui/material';
import {
  CompareArrows,
  TrendingUp,
  Psychology,
  Facebook,
  Twitter,
  Instagram
} from '@mui/icons-material';
import '../styles/Home.css';

const Home = () => {
  return (
    <Box>
      {/* Hero Section */}
        <Paper 
          elevation={0}
          sx={{
            bgcolor: 'primary.main',
            color: 'white',
            minHeight: '80vh',
            display: 'flex',
            alignItems: 'center',
            mb: 6
          }}
        >
          <Container maxWidth="lg">
            <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
            <Typography variant="h2" component="h1" gutterBottom>
              Welcome to ShopWise
            </Typography>
            <Typography variant="h5" paragraph>
              Compare prices and get personalized product recommendations to make smarter shopping decisions.
            </Typography>
            <Stack direction="row" spacing={2}>
              <Button variant="contained" color="secondary" size="large">
            Get Started
              </Button>
              <Button variant="outlined" color="inherit" size="large">
            Learn More
              </Button>
            </Stack>
          </Grid>
          <Grid item xs={12} md={6}>
            {/* You can add an image or graphic here */}
            <Box
              component="img"
              src="hero2-1.png"
              alt="Shopping comparison illustration"
              sx={{
                width: '100%',
                height: 'auto',
                maxWidth: '500px',
                display: 'block',
                margin: '5 auto',
              
              }}
            />
          </Grid>
            </Grid>
          </Container>
        </Paper>

        {/* Benefits Section */}
      <Container maxWidth="lg" sx={{ mb: 4 }}>
        <Typography variant="h3" component="h2" textAlign="center" gutterBottom>
          Why Choose ShopWise?
        </Typography>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <CompareArrows color="secondary" 
                sx={{ 
                  fontSize: 60, 
                  mb: 2, 
                  mx: 2 
                  }} />
                <Typography variant="h5" gutterBottom 
                sx={{
                  mx: 2
                }}>
                  Price Comparison
                </Typography>
                <Typography color="text.secondary" sx={{
                  mx: 2
                }}>
                  Compare prices across multiple stores to find the best deals instantly
                  Phasellus molestie vehicula est. Mauris posuere bibendum ligula, sit 
                  amet viverra tellus. Aenean massa dolor, faucibus eget lorem nec, 
                  fringilla lacinia arcu. Morbi sapien ipsum, porta nec urna sit amet, 
                  suscipit congue est. 
                </Typography>
                <Button 
                  variant="contained" 
                  color="secondary" 
                  sx={{ 
                    mt: 2,
                    mx: 2
                  }}
                >
                  Learn More
                </Button>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Psychology color="secondary" 
                sx={{ 
                  fontSize: 60, 
                  mb: 2,
                  mx: 2 }} />
                <Typography variant="h5" gutterBottom
                sx={{
                  mx: 2
                }}>
                  Smart Recommendations
                </Typography>
                <Typography color="text.secondary"
                  sx = {{
                    mx: 2
                  }}>
                  Get personalized product suggestions based on your preferences
                  Nullam congue, massa sed vestibulum eleifend, libero nisi vulputate 
                  massa, nec fringilla dui ipsum quis ipsum. Nam dapibus quis eros  
                  eget iaculis. Vestibulum ante ipsum primis in faucibus orci luctus
                  et ultrices posuere cubilia curae; 
                </Typography>
                <Button 
                  variant="contained" 
                  color="secondary" 
                  sx={{ 
                    mt: 2,
                    mx: 2
                  }}
                >
                  Learn More
                </Button>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <TrendingUp color="secondary" 
                sx={{ 
                  fontSize: 60, 
                  mb: 2,
                  mx: 2 }} />
                <Typography variant="h5" gutterBottom
                sx={{
                  mx: 2
                }}>
                  Real-time Updates
                </Typography>
                <Typography color="text.secondary"
                sx={{
                  mx: 2
                }}>
                  Stay updated with the latest prices and availability
                  Nullam congue, massa sed vestibulum eleifend, libero 
                  nisi vulputate massa, nec fringilla dui ipsum quis ipsum. 
                  Nam dapibus quis eros eget iaculis. Vestibulum ante ipsum 
                  primis in faucibus orci luctus et ultrices posuere wehfsek
                  sefhuihefksn ioewfns.
                  
                </Typography>
                <Button 
                  variant="contained" 
                  color="secondary" 
                  sx={{ 
                    mt: 2,
                    mx: 2
                  }}
                >
                  Learn More
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
      
      <Divider sx={{ 
        mt: 4,
        mb: 4 }} />

      <Grid item xs={12}>
        <Typography variant="h4" component="h2" textAlign='center' gutterBottom
        sx={{
          mb: 4,
          color: 'GrayText'
          
        }}>
          Our Stores
        </Typography>
        <Grid container spacing={2} justifyContent='center' 
        sx={{
            mb: 5,
            marginLeft: 3.5
        }}>
          <Grid item xs={6} sm={4} md={2}>
            <Box
              sx={{
                width: 100,
                height: 100,
                borderRadius: '50%',
                border: '2px solid',
                borderColor: 'primary.main',
                overflow: 'hidden',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                bgcolor: 'background.paper',
              }}
            >
              <Box
                component="img"
                src="pnp.png"
                alt="Pick n Pay"
                sx={{
                  width: '80%',
                  height: '80%',
                  objectFit: 'contain',
                }}
              />
            </Box>
            
          </Grid>
          <Grid item xs={6} sm={4} md={2}>
            <Box
              sx={{
                width: 100,
                height: 100,
                borderRadius: '50%',
                border: '2px solid',
                borderColor: 'primary.main',
                overflow: 'hidden',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                bgcolor: 'background.paper',
              }}
            >
              <Box
                component="img"
                src="checkers.jpg"
                alt="Checkers"
                sx={{
                  width: '80%',
                  height: '80%',
                  objectFit: 'contain',
                }}
              />
            </Box>
          </Grid>
          <Grid item xs={6} sm={4} md={2}>
            <Box
              sx={{
                width: 100,
                height: 100,
                borderRadius: '50%',
                border: '2px solid',
                borderColor: 'primary.main',
                overflow: 'hidden',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                bgcolor: 'background.paper',
              }}
            >
              <Box
                component="img"
                src="clicks.png"
                alt="Clicks"
                sx={{
                  width: '80%',
                  height: '80%',
                  objectFit: 'contain',
                }}
              />
            </Box>
          </Grid>
          {/* Add more store logos as needed */}
          <Grid item xs={6} sm={4} md={2}>
            <Box
              sx={{
                width: 100,
                height: 100,
                borderRadius: '50%',
                border: '2px solid',
                borderColor: 'primary.main',
                overflow: 'hidden',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                bgcolor: 'background.paper',
              }}
            >
              <Box
                component="img"
                src="shoprite.png"
                alt="Shoprite"
                sx={{
                  width: '80%',
                  height: '80%',
                  objectFit: 'contain',
                }}
              />
            </Box>
          </Grid>
          <Grid item xs={6} sm={4} md={2}>
            <Box
              sx={{
                width: 100,
                height: 100,
                borderRadius: '50%',
                border: '2px solid',
                borderColor: 'primary.main',
                overflow: 'hidden',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                bgcolor: 'background.paper',
              }}
            >
              <Box
                component="img"
                src="takealot.jpg"
                alt="Takealot"
                sx={{
                  width: '80%',
                  height: '80%',
                  objectFit: 'contain',
                }}
              />
            </Box>
          </Grid>
          <Grid item xs={6} sm={4} md={2}>
            <Box
              sx={{
                width: 100,
                height: 100,
                borderRadius: '50%',
                border: '2px solid',
                borderColor: 'primary.main',
                overflow: 'hidden',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                bgcolor: 'background.paper',
              }}
            >
              <Box
                component="img"
                src="spar9320.jpg"
                alt="Spar"
                sx={{
                  width: '80%',
                  height: '80%',
                  objectFit: 'contain',
                }}
              />
            </Box>
          </Grid>
        </Grid>
        
      </Grid>

      <Divider sx={{ 
        mt: 4,
        mb: 4 }} />


      {/* Call to Action */}
      <Box sx={{ bgcolor: 'primary.main', color: 'white', py: 2 }}>
        <Container maxWidth="md">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <Box
                component="img"
                src="cta-image.png"
                alt="Call to Action"
                sx={{
                  width: '100%',
                  borderRadius: 2,
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <Box textAlign="center">
                <Typography variant="h4" gutterBottom>
                  Ready to Start Saving?
                </Typography>
                <Typography variant="h6" paragraph>
                  Join thousands of smart shoppers who are already saving money with ShopWise
                </Typography>
                <Box component="form" sx={{ mt: 2 }}>
                  <TextField
                    fullWidth
                    label="First Name"
                    variant="filled"
                    margin="normal"
                    sx={{ bgcolor: 'white', borderRadius: 1 }}
                  />
                  <TextField
                    fullWidth
                    label="Last Name"
                    variant="filled"
                    margin="normal"
                    sx={{ bgcolor: 'white', borderRadius: 1 }}
                  />
                  <TextField
                    fullWidth
                    label="Email"
                    variant="filled"
                    margin="normal"
                    sx={{ bgcolor: 'white', borderRadius: 1 }}
                  />
                  <Button
                    variant="contained"
                    color="secondary"
                    size="large"
                    type="submit"
                    sx={{ mt: 2 }}
                  >
                    Sign Up Now
                  </Button>
                </Box>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>
      
      <Divider sx={{ 
        mt: 2,
         }} />


      {/* Footer Section */}
      <Box sx={{ bgcolor: 'white', color: 'grayText', py: 4 }}>
        <Container maxWidth="lg">
          <Grid container spacing={4}>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom>
                ShopWise
              </Typography>
              <Typography variant="body2">
                © {new Date().getFullYear()} ShopWise. All rights reserved.
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom>
                Quick Links
              </Typography>
              <Typography variant="body2">
                <Link href="#" color="inherit" underline="none">
                  About Us
                </Link>
              </Typography>
              <Typography variant="body2">
                <Link href="#" color="inherit" underline="none">
                  Contact
                </Link>
              </Typography>
              <Typography variant="body2">
                <Link href="#" color="inherit" underline="none">
                  Privacy Policy
                </Link>
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom>
                Follow Us
              </Typography>
              <Box>
                <IconButton color="inherit" href="#">
                  <Facebook />
                </IconButton>
                <IconButton color="inherit" href="#">
                  <Twitter />
                </IconButton>
                <IconButton color="inherit" href="#">
                  <Instagram />
                </IconButton>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>
    </Box>
  );
};

export default Home;

