import React, { useState } from 'react';
import axios from 'axios';
import { Box, Typography, Button, Alert, CircularProgress } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';

const PDFDownloader = ({ reportData, onError }) => {
  const [downloading, setDownloading] = useState(false);
  const [success, setSuccess] = useState(null);

  const handleDownload = async () => {
    setDownloading(true);
    try {
      const response = await axios.get(`http://localhost:8000/api/generate-pdf/${reportData.task_id}`, {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${reportData.company_name || 'report'}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      setSuccess('PDF downloaded successfully.');
    } catch (error) {
      onError(error.response?.data?.detail || 'Error downloading PDF.');
    } finally {
      setDownloading(false);
    }
  };

  return (
    <Box sx={{ mb: 2, bgcolor: '#27292D', p: 2 }}>
      <Typography variant="h3" gutterBottom color="text.primary" sx={{ mb: 2 }}>
        Download PDF Report
      </Typography>
      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}
      <Button
        variant="contained"
        color="primary"
        onClick={handleDownload}
        disabled={downloading}
        startIcon={downloading ? <CircularProgress size={20} color="inherit" /> : <DownloadIcon />}
        sx={{ mt: 1 }}
      >
        {downloading ? 'Downloading...' : 'Download PDF'}
      </Button>
    </Box>
  );
};

export default PDFDownloader;


