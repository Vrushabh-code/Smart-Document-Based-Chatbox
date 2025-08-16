import { useSearchParams, useNavigate } from 'react-router-dom';
import { Document, Page, pdfjs } from 'react-pdf';
import { useState, useCallback } from 'react';
import { Box, Typography, IconButton, Paper, LinearProgress, Container } from '@mui/material';
import { ArrowBack, NavigateBefore, NavigateNext, ZoomIn, ZoomOut } from '@mui/icons-material';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const PDFViewerPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const file = searchParams.get('file');
  const [pageNumber, setPageNumber] = useState(parseInt(searchParams.get('page')) || 1);
  const [numPages, setNumPages] = useState(null);
  const [scale, setScale] = useState(1.0);
  const [isLoading, setIsLoading] = useState(true);

  const onDocumentLoadSuccess = useCallback(({ numPages }) => {
    setNumPages(numPages);
    setIsLoading(false);
  }, []);

  const goToPrevPage = () => {
    if (pageNumber > 1) {
      const newPage = pageNumber - 1;
      setPageNumber(newPage);
      updateUrl(newPage);
    }
  };

  const goToNextPage = () => {
    if (pageNumber < numPages) {
      const newPage = pageNumber + 1;
      setPageNumber(newPage);
      updateUrl(newPage);
    }
  };

  const updateUrl = (page) => {
    window.history.pushState({}, '', `?file=${file}&page=${page}`);
  };

  const zoomIn = () => setScale(prev => Math.min(prev + 0.2, 2));
  const zoomOut = () => setScale(prev => Math.max(prev - 0.2, 0.5));

  return (
    <Box sx={{ 
      minHeight: '100vh',
      bgcolor: '#f5f5f5',
      pb: 4
    }}>
      {/* Header */}
      <Paper elevation={3} sx={{ 
        p: 2, 
        mb: 3, 
        borderRadius: 0,
        bgcolor: '#1e88e5',
        color: 'white',
        display: 'flex',
        alignItems: 'center',
        gap: 2
      }}>
        <IconButton color="inherit" onClick={() => navigate(-1)}>
          <ArrowBack />
        </IconButton>
        <Typography variant="h6" noWrap sx={{ flexGrow: 1 }}>
          {file}
        </Typography>
      </Paper>

      <Container maxWidth="lg">
        {/* PDF Controls */}
        <Paper elevation={2} sx={{ 
          p: 1.5, 
          mb: 2, 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: 1
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <IconButton 
              onClick={goToPrevPage} 
              disabled={pageNumber <= 1}
              color="primary"
              size="small"
            >
              <NavigateBefore />
            </IconButton>
            <Typography variant="body2">
              Page {pageNumber} of {numPages || '--'}
            </Typography>
            <IconButton 
              onClick={goToNextPage} 
              disabled={pageNumber >= (numPages || 0)}
              color="primary"
              size="small"
            >
              <NavigateNext />
            </IconButton>
          </Box>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <IconButton onClick={zoomOut} size="small" disabled={scale <= 0.5}>
              <ZoomOut fontSize="small" />
            </IconButton>
            <Typography variant="body2" sx={{ minWidth: '40px', textAlign: 'center' }}>
              {Math.round(scale * 100)}%
            </Typography>
            <IconButton onClick={zoomIn} size="small" disabled={scale >= 2}>
              <ZoomIn fontSize="small" />
            </IconButton>
          </Box>
        </Paper>

        {/* PDF Viewer */}
        <Paper 
          elevation={3} 
          sx={{ 
            p: 2, 
            minHeight: '70vh',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            position: 'relative',
            bgcolor: '#e0e0e0'
          }}
        >
          {isLoading && (
            <Box sx={{ width: '100%', position: 'absolute', top: 0, left: 0 }}>
              <LinearProgress />
            </Box>
          )}
          <Box sx={{ 
            transform: `scale(${scale})`,
            transformOrigin: 'top center',
            transition: 'transform 0.2s ease-in-out',
            width: '100%',
            display: 'flex',
            justifyContent: 'center'
          }}>
            <Document
              file={`/pdfs/${file}`}
              onLoadSuccess={onDocumentLoadSuccess}
              onLoadError={console.error}
              loading={
                <Box sx={{ p: 4, textAlign: 'center' }}>
                  <Typography>Loading PDF...</Typography>
                </Box>
              }
            >
              <Page 
                pageNumber={pageNumber} 
                width={Math.min(800, window.innerWidth * 0.8)}
                loading={
                  <Box sx={{ p: 4, textAlign: 'center' }}>
                    <Typography>Loading page {pageNumber}...</Typography>
                  </Box>
                }
              />
            </Document>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
};

export default PDFViewerPage;


