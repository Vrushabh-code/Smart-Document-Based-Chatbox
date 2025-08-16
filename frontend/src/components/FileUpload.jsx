import React, { useState, useRef } from 'react';
import axios from 'axios';
import axiosRetry from 'axios-retry';
import { Box, Button, CircularProgress, Typography, Paper, IconButton, Chip, Divider } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DeleteIcon from '@mui/icons-material/Delete';
import DescriptionIcon from '@mui/icons-material/Description';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import UploadFileIcon from '@mui/icons-material/UploadFile';

axiosRetry(axios, {
  retries: 3,
  retryDelay: (retryCount) => retryCount * 1000,
  retryCondition: (error) => error.message.includes('Network Error'),
});

const FileUpload = ({ onReportGenerated, onError, navigate, showAnalyzeButton = false, existingFileNames = [] }) => {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [uploadedFileNames, setUploadedFileNames] = useState([]);
  const [pdfBlobs, setPdfBlobs] = useState({});
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(selectedFiles);
    setUploadedFileNames(selectedFiles.map(file => file.name));
    setUploadSuccess(false);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDragIn = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.items && e.dataTransfer.items.length > 0) {
      setDragActive(true);
    }
  };

  const handleDragOut = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFiles = Array.from(e.dataTransfer.files).filter(file => file.type === 'application/pdf');
      if (droppedFiles.length > 0) {
        setFiles(droppedFiles);
        setUploadedFileNames(droppedFiles.map(file => file.name));
        setUploadSuccess(false);
      }
    }
  };

  const removeFile = (index) => {
    const newFiles = files.filter((_, i) => i !== index);
    setFiles(newFiles);
    setUploadedFileNames(newFiles.map(file => file.name));
    setUploadSuccess(false);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (files.length === 0) {
      onError('Please select at least one PDF file.');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));
    formData.append('existing_files', JSON.stringify(existingFileNames));

    try {
      console.time('upload-files');
      console.log('Sending request to:', 'http://127.0.0.1:8000/api/upload-files', { existing_files: existingFileNames });
      const uploadResponse = await axios.post('http://127.0.0.1:8000/api/upload-files', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 60000,
      });
      console.log('Upload response:', {
        data: uploadResponse.data,
        status: uploadResponse.status,
      });
      console.timeEnd('upload-files');

      if (uploadResponse.data.status !== 'success') {
        throw new Error('File upload failed: ' + (uploadResponse.data.detail || 'Unknown error'));
      }

      setUploadSuccess(true);
      onError(null);
      const newPdfBlobs = {};
      files.forEach((file) => {
        const blobUrl = URL.createObjectURL(file);
        newPdfBlobs[file.name] = blobUrl;
      });
      setPdfBlobs(newPdfBlobs);

      // Trigger onReportGenerated with uploaded file names and pdfBlobs
      onReportGenerated({
        uploadedFileNames: [...new Set([...existingFileNames, ...uploadedFileNames])],
        pdfBlobs: newPdfBlobs,
      });
    } catch (error) {
      console.error('Upload Error:', {
        message: error.message,
        code: error.code,
        response: error.response ? {
          status: error.response.status,
          data: error.response.data,
          headers: error.response.headers,
        } : null,
        config: error.config ? {
          url: error.config.url,
          headers: error.config.headers,
        } : null,
      });
      if (error.code === 'ECONNABORTED') {
        onError('Upload timed out after 60s. Check if the backend server is running on http://127.0.0.1:8000.');
      } else if (error.message.includes('Network Error')) {
        onError('Network error: Unable to reach the backend. Ensure the server is running on http://127.0.0.1:8000.');
      } else if (error.response?.data?.detail) {
        onError(`Upload error: ${error.response.data.detail}`);
      } else {
        onError(`Error uploading files: ${error.message || 'Unknown error'}`);
      }
    } finally {
      setUploading(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <Box sx={{ width: '100%' }}>
      {/* PROMINENT UPLOAD SECTION */}
      <Paper
        elevation={0}
        sx={{
          p: 4,
          mb: 4,
          background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%)',
          border: '2px solid rgba(99, 102, 241, 0.3)',
          borderRadius: 4,
          textAlign: 'center',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        {/* Glowing border effect */}
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '2px',
            background: 'linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899)',
            animation: 'glow 2s ease-in-out infinite',
          }}
        />

        <Typography
          variant="h4"
          sx={{
            color: '#f8fafc',
            fontWeight: 700,
            mb: 3,
            textShadow: '0 0 20px rgba(99, 102, 241, 0.5)',
          }}
        >
          📁 UPLOAD YOUR PDF FILES
        </Typography>

        <Typography
          sx={{
            color: '#cbd5e1',
            fontSize: '1.1rem',
            mb: 4,
            maxWidth: '600px',
            mx: 'auto',
          }}
        >
          Select your financial documents to get started with AI-powered analysis
        </Typography>

        {/* Main Upload Button */}
        <Box sx={{ mb: 4 }}>
          <Button
            variant="contained"
            size="large"
            onClick={() => fileInputRef.current?.click()}
            startIcon={<UploadFileIcon />}
            sx={{
              background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
              borderRadius: 3,
              px: 6,
              py: 2,
              fontWeight: 700,
              textTransform: 'none',
              fontSize: '1.1rem',
              letterSpacing: '0.025em',
              boxShadow: '0 8px 25px rgba(99, 102, 241, 0.4)',
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
              '&:hover': {
                transform: 'translateY(-3px)',
                boxShadow: '0 15px 35px rgba(99, 102, 241, 0.6)',
                background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
              },
            }}
          >
            CHOOSE FILES
          </Button>
        </Box>

        {/* Hidden file input */}
        <input
          ref={fileInputRef}
          type="file"
          accept="application/pdf"
          multiple
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />

        <Divider sx={{ my: 3, borderColor: 'rgba(255, 255, 255, 0.2)' }}>
          <Typography sx={{ color: '#94a3b8', px: 2 }}>OR</Typography>
        </Divider>

        {/* Drag and Drop Area */}
        <Paper
          elevation={0}
          sx={{
            p: 4,
            background: dragActive 
              ? 'linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%)'
              : 'linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)',
            border: dragActive 
              ? '2px dashed #6366f1'
              : '2px dashed rgba(255, 255, 255, 0.3)',
            borderRadius: 4,
            textAlign: 'center',
            cursor: 'pointer',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            '&:hover': {
              background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)',
              borderColor: 'rgba(99, 102, 241, 0.5)',
              transform: 'translateY(-2px)',
            },
            animation: dragActive ? 'pulse 1s ease-in-out infinite' : 'none',
          }}
          onDragEnter={handleDragIn}
          onDragLeave={handleDragOut}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <CloudUploadIcon 
            sx={{ 
              fontSize: '3rem', 
              color: dragActive ? '#6366f1' : '#94a3b8',
              mb: 2,
              transition: 'all 0.3s ease',
            }} 
          />
          
          <Typography
            variant="h6"
            sx={{
              color: dragActive ? '#6366f1' : '#f8fafc',
              fontWeight: 600,
              mb: 1,
              transition: 'all 0.3s ease',
            }}
          >
            {dragActive ? 'Drop your PDF files here' : 'Drag & Drop PDF files here'}
          </Typography>
          
          <Typography
            sx={{
              color: '#94a3b8',
              fontSize: '1rem',
              mb: 2,
            }}
          >
            or use the button above to browse files
          </Typography>
          
          <Typography
            sx={{
              color: '#64748b',
              fontSize: '0.875rem',
              fontStyle: 'italic',
            }}
          >
            Supports multiple PDF files • Max file size: 50MB
          </Typography>
        </Paper>
      </Paper>

      {/* File List */}
      {files.length > 0 && (
        <Paper
          elevation={0}
          sx={{
            p: 3,
            mb: 3,
            background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(51, 65, 85, 0.8) 100%)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: 4,
            backdropFilter: 'blur(20px)',
          }}
        >
          <Typography
            variant="h6"
            sx={{
              color: '#f8fafc',
              fontWeight: 600,
              mb: 3,
              display: 'flex',
              alignItems: 'center',
              gap: 1,
            }}
          >
            <DescriptionIcon sx={{ color: '#6366f1' }} />
            Selected Files ({files.length})
          </Typography>
          
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {files.map((file, index) => (
              <Box
                key={index}
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  p: 2,
                  background: 'rgba(255, 255, 255, 0.03)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  borderRadius: 3,
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    background: 'rgba(255, 255, 255, 0.05)',
                    borderColor: 'rgba(99, 102, 241, 0.3)',
                  },
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flex: 1 }}>
                  <DescriptionIcon sx={{ color: '#6366f1', fontSize: '1.5rem' }} />
                  <Box sx={{ flex: 1, minWidth: 0 }}>
                    <Typography
                      sx={{
                        color: '#f8fafc',
                        fontWeight: 500,
                        fontSize: '0.9rem',
                        mb: 0.5,
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                      }}
                    >
                      {file.name}
                    </Typography>
                    <Typography
                      sx={{
                        color: '#94a3b8',
                        fontSize: '0.8rem',
                      }}
                    >
                      {formatFileSize(file.size)}
                    </Typography>
                  </Box>
                </Box>
                
                <IconButton
                  onClick={() => removeFile(index)}
                  sx={{
                    color: '#ef4444',
                    '&:hover': {
                      background: 'rgba(239, 68, 68, 0.1)',
                    },
                  }}
                >
                  <DeleteIcon />
                </IconButton>
              </Box>
            ))}
          </Box>
        </Paper>
      )}

      {/* Upload Button */}
      {files.length > 0 && (
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <Button
            variant="contained"
            size="large"
            onClick={handleUpload}
            disabled={uploading}
            startIcon={uploading ? <CircularProgress size={20} /> : uploadSuccess ? <CheckCircleIcon /> : <CloudUploadIcon />}
            sx={{
              background: 'linear-gradient(135deg, #10b981 0%, #34d399 100%)',
              borderRadius: 3,
              px: 6,
              py: 2,
              fontWeight: 700,
              textTransform: 'none',
              fontSize: '1.1rem',
              letterSpacing: '0.025em',
              boxShadow: '0 8px 25px rgba(16, 185, 129, 0.4)',
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
              '&:hover': {
                transform: 'translateY(-3px)',
                boxShadow: '0 15px 35px rgba(16, 185, 129, 0.6)',
                background: 'linear-gradient(135deg, #059669 0%, #10b981 100%)',
              },
              '&:disabled': {
                background: 'rgba(255, 255, 255, 0.1)',
                color: 'rgba(255, 255, 255, 0.5)',
                boxShadow: 'none',
              },
            }}
          >
            {uploading ? 'UPLOADING...' : uploadSuccess ? 'FILES UPLOADED!' : 'UPLOAD FILES'}
          </Button>
        </Box>
      )}

      {/* Success Message */}
      {uploadSuccess && (
        <Box
          sx={{
            mt: 3,
            p: 3,
            background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(52, 211, 153, 0.1) 100%)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            borderRadius: 3,
            textAlign: 'center',
            animation: 'fadeIn 0.5s ease-out',
          }}
        >
          <Typography
            sx={{
              color: '#10b981',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 1,
              fontSize: '1.1rem',
            }}
          >
            <CheckCircleIcon />
            Files uploaded successfully! You can now analyze them.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default FileUpload;


