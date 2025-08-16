import React, { useState, useRef, useEffect } from 'react';
import { Container, Typography, Box, Alert, Divider, FormControl, InputLabel, Select, MenuItem, Button, CircularProgress, Paper, Tooltip, IconButton, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import axios from 'axios';
import HelpIcon from '@mui/icons-material/Help';
import InfoIcon from '@mui/icons-material/Info';
import FileUpload from './components/FileUpload';
import ReportDisplay from './components/ReportDisplay';
import ChatBox from './components/ChatBox';
import PdfThumbnail from './components/PdfThumbnail';
import InlinePDFViewer from './components/inlinePDFviewer';
import WelcomePage from './components/WelcomePage';
import UploadPage from './components/UploadPage';
import theme from './theme';

class ErrorBoundary extends React.Component {
  state = { error: null };

  static getDerivedStateFromError(error) {
    return { error: error.message };
  }

  render() {
    if (this.state.error) {
      return (
        <Alert severity="error" sx={{ mb: 3 }}>
          Error rendering component: {this.state.error}. Check for invalid hook usage.
        </Alert>
      );
    }
    return this.props.children;
  }
}

function App() {
  const [reportData, setReportData] = useState(null);
  const [error, setError] = useState(null);
  const [pdfView, setPdfView] = useState(null);
  const [pdfBlobs, setPdfBlobs] = useState({});
  const [uploadedFileNames, setUploadedFileNames] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedSection, setSelectedSection] = useState('Chat with the Report');
  const [analyzing, setAnalyzing] = useState(false);
  const leftSectionRef = useRef(null);
  const rightSectionRef = useRef(null);
  const navigate = useNavigate();
  const [selectedCitation, setSelectedCitation] = useState(null);
  const [helpOpen, setHelpOpen] = useState(false);
  const [currentHelpSection, setCurrentHelpSection] = useState('overview');

  useEffect(() => {
    if (window.location.pathname === '/') {
      navigate('/upload', { replace: true });
    }
  }, [navigate]);

  useEffect(() => {
    const navigationType = performance.getEntriesByType('navigation')[0]?.type;
    const currentPath = window.location.pathname;
    // Only redirect on actual page reloads, not on programmatic navigation
    if (navigationType === 'reload') {
      if (
        currentPath !== '/' &&
        currentPath !== '/upload' &&
        currentPath !== '/main'
      ) {
        navigate('/upload', { replace: true });
      }
    }
  }, [navigate]);

  useEffect(() => {
    if (leftSectionRef.current) {
      console.log('Left section scrollHeight:', leftSectionRef.current.scrollHeight);
      console.log('Left section clientHeight:', leftSectionRef.current.clientHeight);
    }
    if (rightSectionRef.current) {
      console.log('Right section scrollHeight:', rightSectionRef.current.scrollHeight);
      console.log('Right section clientHeight:', rightSectionRef.current.clientHeight);
    }
  }, [reportData, pdfView, selectedSection]);

  const handleReportGenerated = (data) => {
    setUploadedFileNames(prev => [...new Set([...prev, ...(data.uploadedFileNames || [])])]);
    setPdfBlobs(prev => ({ ...prev, ...(data.pdfBlobs || {}) }));
    setError(null);
    if (!reportData) {
      setReportData({ uploadedFileNames: data.uploadedFileNames, pdfBlobs: data.pdfBlobs });
    } else {
      setReportData(prev => ({
        ...prev,
        uploadedFileNames: [...new Set([...prev.uploadedFileNames, ...(data.uploadedFileNames || [])])],
        pdfBlobs: { ...prev.pdfBlobs, ...(data.pdfBlobs || {}) }
      }));
    }
    if (data.uploadedFileNames?.length > 0) {
      const firstFile = data.uploadedFileNames[0];
      const blobUrl = data.pdfBlobs?.[firstFile];
      if (blobUrl && !pdfView) {
        setPdfView({ file: firstFile, page: 1, blobUrl });
      }
    }
    navigate('/main');
  };

  const handleAnalyze = async () => {
    if (uploadedFileNames.length === 0) {
      setError('Please upload files first before analyzing.');
      return;
    }

    setAnalyzing(true);
    try {
      console.time('analyze');
      const analyzeResponse = await axios.post('http://127.0.0.1:8000/api/analyze', {}, {
        headers: {
          'Accept': 'application/json',
        },
        timeout: 60000,
      });

      if (analyzeResponse.data.status !== 'processing' || !analyzeResponse.data.task_id) {
        throw new Error('Invalid analyze response: Expected task_id and status "processing".');
      }

      const taskId = analyzeResponse.data.task_id;

      let status = 'pending';
      while (status === 'pending') {
        await new Promise(resolve => setTimeout(resolve, 5000));
        const statusResponse = await axios.get(`http://127.0.0.1:8000/api/status/${taskId}`, {
          timeout: 60000,
        });
        status = statusResponse.data.status;
        if (status === 'error') {
          throw new Error('Analysis failed on backend. Check backend logs.');
        }
      }

      const resultResponse = await axios.get(`http://127.0.0.1:8000/api/result/${taskId}`, {
        timeout: 60000,
      });

      const result = resultResponse.data;
      if (result.status === 'error') {
        throw new Error(`Analysis error: ${result.errors.join(', ')}`);
      }

      if (result.pdf_base64 && result.pdf_base64.length > 50_000_000) {
        throw new Error('Response size too large. Try uploading smaller PDFs.');
      }
      if (!result.company_name || !result.business_overview) {
        throw new Error('Incomplete response: Missing required fields.');
      }

      try {
        const report = {
          ...result,
          task_id: taskId,
          uploadedFileNames,
          pdfBlobs,
        };
        setReportData(report);
        setSelectedSection('Report Display');
        setError(null);
      } catch (error) {
        setError('Error rendering analysis result. Check for invalid hook usage in the report display component.');
      }
    } catch (error) {
      if (error.code === 'ECONNABORTED') {
        setError('Analysis timed out. Check backend logs for delays or try a smaller file.');
      } else if (error.message.includes('Network Error')) {
        setError('Network error: Unable to reach the backend. Ensure the server is running on http://127.0.0.1:8000.');
      } else if (error.response?.data?.detail) {
        setError(`Analysis error: ${error.response.data.detail}`);
      } else {
        setError(`Error analyzing files: ${error.message || 'Unknown error'}`);
      }
    } finally {
      setAnalyzing(false);
    }
  };

  const handleError = (errorMsg) => {
    setError(errorMsg);
  };

  const helpContent = {
    overview: {
      title: "Welcome to FinanceBot",
      content: "FinanceBot is an AI-powered platform that analyzes financial documents and provides comprehensive insights. Upload PDF documents, analyze them with AI, and interact with your data through chat."
    },
    upload: {
      title: "File Upload",
      content: "Drag and drop PDF files or click to browse. Supported formats include financial reports, statements, and any PDF documents. You can upload multiple files for comprehensive analysis."
    },
    analysis: {
      title: "Analysis Process",
      content: "Click 'Analyze Files' to start AI-powered analysis. The system will extract text, identify financial metrics, and generate comprehensive reports with business insights."
    },
    report: {
      title: "Report Display",
      content: "View detailed analysis results including business overview, financial metrics, and key findings. Use the export features to download reports in various formats."
    },
    chat: {
      title: "Chat Interface",
      content: "Ask questions about your uploaded documents using natural language. Get AI-powered answers with direct citations to source material. Click on citations to view the original text."
    },
    pdf: {
      title: "PDF Viewer",
      content: "View your uploaded PDFs with highlighted citations. Navigate between pages and see the exact source of information referenced in the analysis."
    }
  };

  const renderSelectedSection = () => {
    if (!reportData) return null;
    switch (selectedSection) {
      case 'Report Display':
        return (
          <ReportDisplay
            reportData={reportData}
            uploadedFileNames={reportData.uploadedFileNames}
            pdfBlobs={pdfBlobs}
            onCitationClick={({ file, page }) => {
              const blobUrl = pdfBlobs?.[file];
              if (!blobUrl) {
                alert("PDF not available in memory.");
                return;
              }
              setPdfView({ file, page, blobUrl });
            }}
            showModifySection
            showUnitConverter
            showPDFDownloader
            taskId={reportData?.task_id}
            onReportGenerated={handleReportGenerated}
            onError={handleError}
          />
        );
      case 'Chat with the Report':
        return (
          <ChatBox
            sessionId={reportData.session_id || 'default_session'}
            fileNames={reportData.uploadedFileNames || []}
            pdfBlobs={pdfBlobs}
            selectedFile={selectedFile}
            onCitationClick={({ file, page, highlightedPages, highlightedPage }) => {
              if (highlightedPages) {
                setPdfView({
                  file,
                  page: highlightedPage,
                  highlightedText: highlightedPages[highlightedPage],
                });
              } else {
                const blobUrl = pdfBlobs?.[file];
                if (!blobUrl) {
                  alert("PDF not available in memory.");
                  return;
                }
                setPdfView({ file, page, blobUrl });
              }
            }}
          />
        );
      default:
        return null;
    }
  };

  return (
    <Routes>
      <Route
        path="/upload"
        element={<UploadPage onReportGenerated={handleReportGenerated} onError={handleError} navigate={navigate} />}
      />
      <Route
        path="/main"
        element={
                      <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                minHeight: '100vh',
                background: 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)',
                width: '100vw',
                overflow: 'auto',
                position: 'relative',
              }}
            >
            {/* Animated background elements */}
            <Box
              sx={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                overflow: 'hidden',
                zIndex: 0,
              }}
            >
              <Box
                sx={{
                  position: 'absolute',
                  top: '10%',
                  left: '10%',
                  width: '200px',
                  height: '200px',
                  background: 'radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%)',
                  borderRadius: '50%',
                  animation: 'float 6s ease-in-out infinite',
                }}
              />
              <Box
                sx={{
                  position: 'absolute',
                  top: '60%',
                  right: '15%',
                  width: '150px',
                  height: '150px',
                  background: 'radial-gradient(circle, rgba(236, 72, 153, 0.1) 0%, transparent 70%)',
                  borderRadius: '50%',
                  animation: 'float 8s ease-in-out infinite reverse',
                }}
              />
              <Box
                sx={{
                  position: 'absolute',
                  bottom: '20%',
                  left: '20%',
                  width: '100px',
                  height: '100px',
                  background: 'radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, transparent 70%)',
                  borderRadius: '50%',
                  animation: 'pulse 4s ease-in-out infinite',
                }}
              />
            </Box>

            <Container
              maxWidth={false}
              sx={{
                flex: 1,
                display: 'flex',
                flexDirection: 'row',
                gap: 0,
                height: 'calc(100vh - 120px)',
                width: '100%',
                mx: 0,
                overflow: 'hidden',
                position: 'relative',
                zIndex: 1,
              }}
            >
              {/* Left Section */}
              <Box
                ref={leftSectionRef}
                sx={{
                  flex: 1,
                  overflowY: 'auto',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: 3,
                  pr: 2,
                  pb: 2,
                                     maxHeight: 'calc(100vh - 120px)',
                   minHeight: 'calc(100vh - 120px)',
                   touchAction: 'pan-y',
                  '&::-webkit-scrollbar': { width: '8px' },
                  '&::-webkit-scrollbar-thumb': { 
                    background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                    borderRadius: '4px'
                  },
                  '&::-webkit-scrollbar-track': { backgroundColor: 'rgba(255, 255, 255, 0.05)' },
                  scrollbarWidth: 'thin',
                  scrollbarColor: '#6366f1 rgba(255, 255, 255, 0.05)',
                }}
                onWheel={(e) => e.stopPropagation()}
                aria-label="PDF Viewer and Upload Section"
                className="slide-in-left"
              >
                {/* Header Section */}
                <Paper
                  elevation={0}
                  sx={{
                    p: 3,
                    mb: 3,
                    background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(51, 65, 85, 0.8) 100%)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: 4,
                    backdropFilter: 'blur(20px)',
                    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
                  }}
                >
                  <Box sx={{ display: 'flex', gap: 3, alignItems: 'center', flexWrap: 'wrap' }}>
                    <Typography 
                      variant="h1" 
                      className="section-title"
                      sx={{
                        background: 'linear-gradient(135deg, #f8fafc 0%, #cbd5e1 100%)',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        backgroundClip: 'text',
                        fontSize: { xs: '2rem', sm: '2.5rem', md: '3rem' },
                        fontWeight: 800,
                        letterSpacing: '-0.025em',
                        textShadow: '0 0 30px rgba(248, 250, 252, 0.3)',
                        mb: 0,
                      }}
                    >
                      FinanceBot
                    </Typography>
                    <Box sx={{ flexGrow: 1 }} />
                    <Tooltip title="Upload additional PDF documents for analysis">
                      <Button
                        variant="contained"
                        onClick={() => navigate('/upload')}
                        sx={{
                          background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                          borderRadius: 3,
                          mr: 2,
                          px: 3,
                          py: 1.5,
                          fontWeight: 600,
                          textTransform: 'none',
                          fontSize: '0.875rem',
                          letterSpacing: '0.025em',
                          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                          '&:hover': {
                            transform: 'translateY(-2px)',
                            boxShadow: '0 10px 25px rgba(99, 102, 241, 0.4)',
                            background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
                          },
                        }}
                      >
                        Add Files
                      </Button>
                    </Tooltip>
                    <Tooltip title="Help & Information">
                      <IconButton
                        onClick={() => setHelpOpen(true)}
                        sx={{
                          color: '#cbd5e1',
                          mr: 2,
                          '&:hover': {
                            color: '#6366f1',
                            transform: 'scale(1.1)',
                          },
                        }}
                      >
                        <HelpIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title={uploadedFileNames.length === 0 ? "Upload files first to start analysis" : "Start AI-powered analysis of uploaded documents"}>
                      <Button
                        variant="contained"
                        onClick={handleAnalyze}
                        disabled={analyzing || uploadedFileNames.length === 0}
                        startIcon={analyzing ? <CircularProgress size={20} /> : null}
                        sx={{
                          background: 'linear-gradient(135deg, #ec4899 0%, #f472b6 100%)',
                          borderRadius: 3,
                          px: 3,
                          py: 1.5,
                          fontWeight: 600,
                          textTransform: 'none',
                          fontSize: '0.875rem',
                          letterSpacing: '0.025em',
                          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                          '&:hover': {
                            transform: 'translateY(-2px)',
                            boxShadow: '0 10px 25px rgba(236, 72, 153, 0.4)',
                            background: 'linear-gradient(135deg, #db2777 0%, #ec4899 100%)',
                          },
                          '&:disabled': {
                            background: 'rgba(255, 255, 255, 0.1)',
                            color: 'rgba(255, 255, 255, 0.5)',
                          },
                        }}
                      >
                        {analyzing ? 'Analyzing...' : 'Analyze Files'}
                      </Button>
                    </Tooltip>
                  </Box>
                </Paper>

                {error && (
                  <Alert 
                    severity="error" 
                    sx={{ 
                      mb: 3,
                      borderRadius: 3,
                      border: '1px solid rgba(239, 68, 68, 0.3)',
                      background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(248, 113, 113, 0.1) 100%)',
                      backdropFilter: 'blur(20px)',
                    }}
                  >
                    {error}
                  </Alert>
                )}

                {pdfView && (
                  <ErrorBoundary>
                    <Paper
                      elevation={0}
                      sx={{
                        p: 3,
                        background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(51, 65, 85, 0.8) 100%)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: 4,
                        backdropFilter: 'blur(20px)',
                        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
                        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                        '&:hover': {
                          transform: 'translateY(-2px)',
                          boxShadow: '0 20px 40px rgba(0, 0, 0, 0.4)',
                          borderColor: 'rgba(255, 255, 255, 0.2)',
                        },
                      }}
                    >
                      <Box sx={{ minHeight: '300px' }}>
                        {pdfView.highlightedText ? (
                          <Box
                            sx={{
                              whiteSpace: 'pre-wrap',
                              color: '#f8fafc',
                              backgroundColor: 'rgba(30, 41, 59, 0.8)',
                              borderRadius: 3,
                              p: 3,
                              lineHeight: 1.6,
                              border: '1px solid rgba(99, 102, 241, 0.3)',
                              maxHeight: '500px',
                              overflowY: 'auto',
                              backdropFilter: 'blur(20px)',
                            }}
                            dangerouslySetInnerHTML={{ __html: pdfView.highlightedText }}
                          />
                        ) : (
                          <Box
                            sx={{
                              whiteSpace: 'pre-wrap',
                              color: '#cbd5e1',
                              backgroundColor: 'rgba(30, 41, 59, 0.8)',
                              borderRadius: 3,
                              p: 3,
                              lineHeight: 1.6,
                              border: '1px solid rgba(255, 255, 255, 0.1)',
                              maxHeight: '500px',
                              overflowY: 'auto',
                              backdropFilter: 'blur(20px)',
                              textAlign: 'center',
                              fontSize: '1.1rem',
                            }}
                          >
                            Select a citation to view the text here.
                          </Box>
                        )}
                      </Box>
                    </Paper>
                  </ErrorBoundary>
                )}
              </Box>

              {/* Divider */}
              <Divider 
                orientation="vertical" 
                flexItem 
                sx={{ 
                  mx: 2, 
                  bgcolor: 'rgba(255, 255, 255, 0.1)',
                  height: '1px',
                  width: '1px',
                }} 
              />

              {/* Right Section */}
              <Box
                ref={rightSectionRef}
                sx={{
                  flex: 1,
                  display: 'flex',
                  flexDirection: 'column',
                  maxHeight: 'calc(100vh - 120px)',
                  minHeight: 'calc(100vh - 120px)',
                  position: 'relative',
                  zIndex: 1,
                }}
                className="slide-in-right"
              >
                {reportData && (
                  <Paper
                    elevation={0}
                    sx={{
                      p: 3,
                      mb: 3,
                      background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(51, 65, 85, 0.8) 100%)',
                      border: '1px solid rgba(255, 255, 255, 0.1)',
                      borderRadius: 4,
                      backdropFilter: 'blur(20px)',
                      boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
                    }}
                  >
                    <FormControl fullWidth sx={{ mb: 2 }}>
                      <InputLabel sx={{ color: '#cbd5e1', fontWeight: 500 }}>Sections</InputLabel>
                      <Select
                        value={selectedSection}
                        onChange={(e) => setSelectedSection(e.target.value)}
                        label="Sections"
                        sx={{
                          color: '#f8fafc',
                          borderRadius: 3,
                          '& .MuiOutlinedInput-notchedOutline': {
                            borderColor: 'rgba(255, 255, 255, 0.2)',
                          },
                          '&:hover .MuiOutlinedInput-notchedOutline': {
                            borderColor: 'rgba(99, 102, 241, 0.5)',
                          },
                          '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                            borderColor: '#6366f1',
                            borderWidth: '2px',
                          },
                          '& .MuiSvgIcon-root': { color: '#cbd5e1' },
                        }}
                      >
                        <MenuItem value="Report Display">
                          <Tooltip title="View comprehensive analysis results with business insights and financial metrics">
                            <Box>Report Display</Box>
                          </Tooltip>
                        </MenuItem>
                        <MenuItem value="Chat with the Report">
                          <Tooltip title="Ask questions about your documents and get AI-powered answers with citations">
                            <Box>Chat with the Report</Box>
                          </Tooltip>
                        </MenuItem>
                      </Select>
                    </FormControl>
                  </Paper>
                )}

                <Box
                  sx={{
                    flex: 1,
                    overflowY: 'auto',
                    pl: 1,
                    pb: 2,
                    '&::-webkit-scrollbar': { width: '8px' },
                    '&::-webkit-scrollbar-thumb': { 
                      background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                      borderRadius: '4px'
                    },
                    '&::-webkit-scrollbar-track': { backgroundColor: 'rgba(255, 255, 255, 0.05)' },
                    scrollbarWidth: 'thin',
                    scrollbarColor: '#6366f1 rgba(255, 255, 255, 0.05)',
                  }}
                  onWheel={(e) => e.stopPropagation()}
                  aria-label="Report and Sections Section"
                >
                  {reportData && (
                    <ErrorBoundary>
                      {renderSelectedSection()}
                    </ErrorBoundary>
                  )}
                </Box>
              </Box>
            </Container>

            {/* Fixed Bottom PDF Thumbnails */}
            {reportData?.uploadedFileNames?.length > 0 && (
              <Paper
                elevation={0}
                sx={{
                  position: 'fixed',
                  bottom: 0,
                  left: 0,
                  right: 0,
                  background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(51, 65, 85, 0.95) 100%)',
                  backdropFilter: 'blur(20px)',
                  borderTop: '1px solid rgba(255, 255, 255, 0.1)',
                  boxShadow: '0 -8px 32px rgba(0, 0, 0, 0.3)',
                  p: 2,
                  display: 'flex',
                  gap: 2,
                  overflowX: 'auto',
                  zIndex: 1000,
                  height: '120px',
                  alignItems: 'center',
                  '&::-webkit-scrollbar': { height: '6px' },
                  '&::-webkit-scrollbar-thumb': { 
                    background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                    borderRadius: '3px'
                  },
                  '&::-webkit-scrollbar-track': { backgroundColor: 'rgba(255, 255, 255, 0.05)' },
                }}
              >
                {reportData.uploadedFileNames.map((name, index) => (
                  <PdfThumbnail
                    key={index}
                    name={name}
                    selected={selectedFile === name}
                    onClick={() => {
                      const blobUrl = pdfBlobs[name];
                      if (blobUrl) {
                        setPdfView({ file: name, page: 1, blobUrl });
                        setSelectedFile(name);
                      } else {
                        alert("PDF not available in memory.");
                      }
                    }}
                  />
                ))}
              </Paper>
            )}

            {/* Help Dialog */}
            <Dialog
              open={helpOpen}
              onClose={() => setHelpOpen(false)}
              maxWidth="md"
              fullWidth
              PaperProps={{
                sx: {
                  background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(51, 65, 85, 0.95) 100%)',
                  backdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  borderRadius: 4,
                },
              }}
            >
              <DialogTitle
                sx={{
                  color: '#f8fafc',
                  borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
                  pb: 2,
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <InfoIcon sx={{ color: '#6366f1' }} />
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Help & Information
                  </Typography>
                </Box>
              </DialogTitle>
              <DialogContent sx={{ pt: 3 }}>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                  {Object.entries(helpContent).map(([key, content]) => (
                    <Box
                      key={key}
                      sx={{
                        p: 3,
                        background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: 3,
                        transition: 'all 0.3s ease',
                        '&:hover': {
                          background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)',
                          borderColor: 'rgba(99, 102, 241, 0.3)',
                        },
                      }}
                    >
                      <Typography
                        variant="h6"
                        sx={{
                          color: '#f8fafc',
                          fontWeight: 600,
                          mb: 1,
                          display: 'flex',
                          alignItems: 'center',
                          gap: 1,
                        }}
                      >
                        {content.title}
                      </Typography>
                      <Typography
                        sx={{
                          color: '#cbd5e1',
                          fontSize: '0.9rem',
                          lineHeight: 1.6,
                        }}
                      >
                        {content.content}
                      </Typography>
                    </Box>
                  ))}
                </Box>
              </DialogContent>
              <DialogActions sx={{ p: 3, borderTop: '1px solid rgba(255, 255, 255, 0.1)' }}>
                <Button
                  onClick={() => setHelpOpen(false)}
                  variant="contained"
                  sx={{
                    background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                    borderRadius: 3,
                    px: 3,
                    py: 1,
                    fontWeight: 600,
                    textTransform: 'none',
                    '&:hover': {
                      background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
                    },
                  }}
                >
                  Got it!
                </Button>
              </DialogActions>
            </Dialog>
          </Box>
        }
      />
      <Route path="/" element={<Navigate to="/upload" replace />} />
      <Route path="*" element={<Navigate to="/upload" replace />} />
    </Routes>


  );
}

export default App;