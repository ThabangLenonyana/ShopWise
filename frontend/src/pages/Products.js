import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  TextField, 
  Grid, 
  Card, 
  CardContent, 
  CardMedia, 
  Pagination, 
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
} from '@mui/material';
import { fetchProducts, fetchCategories, fetchRetailers} from '../services/api';
import win from 'global';

const RETAILER_DOMAINS = {
  'shoprite': 'www.shoprite.co.za',
  'checkers': 'www.checkers.co.za',
};

// 
const Products = () => {
  // State variables
  const [products, setProducts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const [categories, setCategories] = useState([]);
  const [retailers, setRetailers] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedRetailer, setSelectedRetailer] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const pageSize = 24;
  const [error, setError] = useState(null);

  const formatImageUrl = (product) => {
    console.log('Full product object:', product);
    // Get domain from mapping instead of database
    const retailerDomain = RETAILER_DOMAINS[product.retailer_name];
  
    // Debug logging
    console.log('Original URL:', product.image_url);
    console.log('Retailer ID:', product.retailer_name);
    console.log('Retailer Domain:', retailerDomain);
       
    if (!retailerDomain) return product.image_url;
      
    const cleanImagePath = product.image_url.replace(/^https:\/\/+/, '');
    console.log('Clean Image Path:', cleanImagePath);
  
    const formattedUrl = `https://${retailerDomain}/${cleanImagePath}`;
    console.log('Formatted URL:', formattedUrl);
      
    return formattedUrl;
  };

  useEffect(() => {
    const loadProducts = async () => {
      setIsLoading(true); 
      setError(null);
      try {
        const response = await fetchProducts(searchTerm, page, {
          category: selectedCategory,
          retailer: selectedRetailer
        }, pageSize);

        setProducts(response.data || []);
        setTotalPages(response.pagination?.totalPages || 1);
    
      } catch (error) {
        console.error('Failed to load products', error);
        setError('Failed to load products. Please try again.');
        setProducts([]);
      } finally {
        setIsLoading(false);
      }
    };

    loadProducts();
  }, [searchTerm, page, selectedCategory, selectedRetailer]);

  useEffect(() => {
    const loadFilterOptions = async () => {
      try {
        const [categoriesResponse, retailersResponse] = await Promise.all([
          fetchCategories(),
          fetchRetailers()
        ]);
        setCategories(categoriesResponse.data);
        setRetailers(retailersResponse.data);
      } catch (error) {
        console.error('Failed to load filter options', error);
      }
    };
    loadFilterOptions();
  }, []);

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
    setPage(1); // Reset to first page on new search
  };

  const handlePageChange = (event, newPage) => {
    setPage(newPage);
    win.scrollTo(0, 0);
  };

  const handleCategoryChange = (event) => {
    setSelectedCategory(event.target.value);
    setPage(1);
  };
  
  const handleRetailerChange = (event) => {
    setSelectedRetailer(event.target.value);
    setPage(1);
  };

  return (
    <Container maxWidth="lg">
      {isLoading && <CircularProgress />}
      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Products
        </Typography>
        <TextField
          fullWidth
          label="Search Products"
          variant="outlined"
          value={searchTerm}
          onChange={handleSearchChange}
          sx={{ mb: 4 }}
        />
        <Box sx={{ display: 'flex', gap: 2, mb: 4 }}>
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Category</InputLabel>
            <Select
              value={selectedCategory}
              label="Category"
              onChange={handleCategoryChange}
            >
              <MenuItem value="">All Categories</MenuItem>
              {categories.map((category) => (
                <MenuItem key={category.id} value={category.id}>
                  {category.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Retailer</InputLabel>
            <Select
              value={selectedRetailer}
              label="Retailer"
              onChange={handleRetailerChange}
            >
              <MenuItem value="">All Retailers</MenuItem>
              {retailers.map((retailer) => (
                <MenuItem key={retailer.id} value={retailer.id}>
                  {retailer.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
        <Grid container spacing={4}>
          {products.map((product) => (
            <Grid item xs={12} sm={6} md={4} key={product.id}>
              <Card>
                <Box sx={{ padding: 3 }}> 
                  <CardMedia
                    component="img"
                    sx={{ 
                      height: 250,
                      width: '100%',
                      objectFit: 'cover',
                    }}
                    image={formatImageUrl(product)}
                    alt={product.name}
                  />
                </Box>
                <CardContent sx={{ padding: 3 }}>
                  <Typography gutterBottom variant="h6" component="div" sx={{mb: 1}}>
                    {product.name}
                  </Typography>
                  <Typography variant="h4"
                  sx={{
                    fontWeight: 'bold',
                    color: 'primary.main',
                    mb: 1,
                  }}>
                    R{product.current_price?.toFixed(2)}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {product.retailer_name}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <Pagination
            count={totalPages}
            page={page}
            onChange={handlePageChange}
            color="primary"
          />
        </Box>
      </Box>
    </Container>
  );
};


export default Products;
