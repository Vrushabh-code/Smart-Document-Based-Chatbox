import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const PdfThumbnail = ({ name, onClick, selected }) => {
  return (
    <Card
      elevation={0}
      sx={{
        width: 230,
        height: 100,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        cursor: 'pointer',
        background: selected 
          ? 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)'
          : 'linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(51, 65, 85, 0.9) 100%)',
        border: selected 
          ? '2px solid rgba(255, 255, 255, 0.3)'
          : '1px solid rgba(255, 255, 255, 0.1)',
        borderRadius: 3,
        color: selected ? '#ffffff' : '#cbd5e1',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        position: 'relative',
        overflow: 'hidden',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: selected 
            ? '0 15px 35px rgba(99, 102, 241, 0.4)'
            : '0 10px 25px rgba(0, 0, 0, 0.3)',
          background: selected 
            ? 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)'
            : 'linear-gradient(135deg, rgba(30, 41, 59, 1) 0%, rgba(51, 65, 85, 1) 100%)',
          borderColor: selected 
            ? 'rgba(255, 255, 255, 0.5)'
            : 'rgba(99, 102, 241, 0.3)',
        },
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '2px',
          background: selected 
            ? 'linear-gradient(90deg, #ffffff, rgba(255, 255, 255, 0.5))'
            : 'linear-gradient(90deg, #6366f1, #8b5cf6)',
          opacity: selected ? 1 : 0,
          transition: 'opacity 0.3s ease',
        },
        '&:hover::before': {
          opacity: 1,
        },
      }}
      onClick={onClick}
      aria-label={`Open PDF: ${name}`}
    >
      {/* Selection indicator */}
      {selected && (
        <Box
          sx={{
            position: 'absolute',
            top: 8,
            right: 8,
            background: 'rgba(255, 255, 255, 0.2)',
            borderRadius: '50%',
            p: 0.5,
            animation: 'pulse 2s ease-in-out infinite',
          }}
        >
          <CheckCircleIcon sx={{ fontSize: '16px', color: '#ffffff' }} />
        </Box>
      )}

      <CardContent sx={{ textAlign: 'center', p: 1, width: '100%' }}>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 1,
          }}
        >
          <PictureAsPdfIcon
            sx={{ 
              fontSize: '24px',
              color: selected ? '#ffffff' : '#ef4444',
              filter: selected ? 'drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3))' : 'none',
              transition: 'all 0.3s ease',
            }}
          />
          <Typography
            variant="caption"
            component="div"
            sx={{
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              maxWidth: '200px',
              fontSize: '0.75rem',
              fontWeight: selected ? 600 : 500,
              color: selected ? '#ffffff' : '#cbd5e1',
              lineHeight: 1.2,
              textShadow: selected ? '0 1px 2px rgba(0, 0, 0, 0.3)' : 'none',
            }}
          >
            {name}
          </Typography>
          
          {/* File type indicator */}
          <Box
            sx={{
              px: 1.5,
              py: 0.5,
              background: selected 
                ? 'rgba(255, 255, 255, 0.2)'
                : 'rgba(239, 68, 68, 0.2)',
              borderRadius: 2,
              border: `1px solid ${selected 
                ? 'rgba(255, 255, 255, 0.3)'
                : 'rgba(239, 68, 68, 0.3)'
              }`,
            }}
          >
            <Typography
              sx={{
                fontSize: '0.6rem',
                fontWeight: 600,
                color: selected ? '#ffffff' : '#ef4444',
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
              }}
            >
              PDF
            </Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default PdfThumbnail;