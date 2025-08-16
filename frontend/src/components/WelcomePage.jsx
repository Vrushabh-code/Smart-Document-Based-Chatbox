import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import AddIcon from '@mui/icons-material/Add';

const WelcomePage = () => {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        bgcolor: '#27292D',
        color: '#ffffff',
        p: 2,
      }}
    >
      <Typography
        variant="h1"
        sx={{
          mb: 8,
          fontSize: { xs: '2.5rem', sm: '3.5rem', md: '4.5rem' },
          fontWeight: 'bold',
          textAlign: 'center',
          color: '#b0bec5',
        }}
      >
        Welcome to FinBot
      </Typography>
      <Button
        variant="contained"
        startIcon={<AddIcon />}
        onClick={() => navigate('/upload')}
        sx={{
          bgcolor: '#42a5f5',
          '&:hover': { bgcolor: '#1e88e5' },
          borderRadius: 3,
          textTransform: 'none',
          fontSize: '1.2rem',
          py: 1.5,
          px: 3,
        }}
      >
        Create Project
      </Button>
    </Box>
  );
};

export default WelcomePage;