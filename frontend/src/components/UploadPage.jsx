import React, { useState } from 'react';
import { Box, Typography, Container, Paper, Button, Accordion, AccordionSummary, AccordionDetails, List, ListItem, ListItemIcon, ListItemText, Chip, Divider } from '@mui/material';
import FileUpload from './FileUpload';
import { useNavigate } from 'react-router-dom';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import UploadIcon from '@mui/icons-material/Upload';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import ChatIcon from '@mui/icons-material/Chat';
import DescriptionIcon from '@mui/icons-material/Description';
import DownloadIcon from '@mui/icons-material/Download';
import InfoIcon from '@mui/icons-material/Info';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';

const UploadPage = ({ onReportGenerated, onError, existingFileNames = [] }) => {
  const navigate = useNavigate();
  const [activeSection, setActiveSection] = useState('overview');

  const projectDescription = {
    title: "FinanceBot - AI-Powered Financial Document Analysis",
    description: "FinanceBot is an intelligent platform that uses advanced AI to analyze financial documents, extract key insights, and provide comprehensive reports. Perfect for investors, analysts, and anyone needing to understand financial documents quickly and accurately.",
    features: [
      "AI-powered document analysis and text extraction",
      "Interactive chat interface for document queries",
      "Comprehensive financial report generation",
      "PDF viewing with citation tracking",
      "Export capabilities for reports and data",
      "Real-time analysis with progress tracking"
    ]
  };

  const componentGuide = [
    {
      name: "File Upload Component",
      icon: <UploadIcon />,
      description: "The starting point of your analysis journey",
      features: [
        "Drag & drop PDF file upload",
        "Multiple file support",
        "File validation and preview",
        "Progress tracking during upload"
      ],
      usage: "Simply drag your PDF files into the upload area or click to browse. Supported formats include financial reports, statements, and any PDF documents."
    },
    {
      name: "Report Display Component",
      icon: <DescriptionIcon />,
      description: "Comprehensive analysis results and insights",
      features: [
        "Business overview extraction",
        "Financial metrics analysis",
        "Key thesis points identification",
        "Interactive data visualization"
      ],
      usage: "After analysis, view detailed reports with business insights, financial metrics, and key findings extracted from your documents."
    },
    {
      name: "Chat Interface",
      icon: <ChatIcon />,
      description: "Interactive AI-powered document querying",
      features: [
        "Natural language questions",
        "Citation-based answers",
        "Context-aware responses",
        "Document-specific insights"
      ],
      usage: "Ask questions about your uploaded documents and get AI-powered answers with direct citations to source material."
    },
    {
      name: "PDF Viewer",
      icon: <DescriptionIcon />,
      description: "Enhanced document viewing with citation tracking",
      features: [
        "Inline PDF viewing",
        "Citation highlighting",
        "Page navigation",
        "Text extraction display"
      ],
      usage: "View your uploaded PDFs with highlighted citations and navigate between pages while maintaining context."
    },
    {
      name: "Analysis Engine",
      icon: <AnalyticsIcon />,
      description: "AI-powered document processing and analysis",
      features: [
        "Text extraction and processing",
        "Financial data identification",
        "Business metrics calculation",
        "Insight generation"
      ],
      usage: "The core AI engine processes your documents to extract meaningful insights and generate comprehensive reports."
    },
    {
      name: "Export Tools",
      icon: <DownloadIcon />,
      description: "Download and share analysis results",
      features: [
        "PDF report generation",
        "Data export capabilities",
        "Customizable report formats",
        "Share functionality"
      ],
      usage: "Export your analysis results in various formats for sharing, presentation, or further analysis."
    }
  ];

  const stepByStepGuide = [
    {
      step: 1,
      title: "Upload Your Documents",
      description: "Start by uploading your financial PDF documents. You can upload multiple files for comprehensive analysis.",
      action: "Drag and drop files or click to browse"
    },
    {
      step: 2,
      title: "Initiate Analysis",
      description: "Click the 'Analyze Files' button to start the AI-powered analysis process.",
      action: "Click 'Analyze Files' button"
    },
    {
      step: 3,
      title: "Review Results",
      description: "Explore the generated report with business overview, financial metrics, and key insights.",
      action: "Navigate through different report sections"
    },
    {
      step: 4,
      title: "Chat with Documents",
      description: "Ask specific questions about your documents using the interactive chat interface.",
      action: "Switch to 'Chat with the Report' section"
    },
    {
      step: 5,
      title: "Export and Share",
      description: "Download your analysis results or share them with your team.",
      action: "Use export features in the report display"
    }
  ];

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)',
        color: '#f8fafc',
        p: 2,
        position: 'relative',
        overflow: 'auto',
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
            top: '5%',
            left: '5%',
            width: '300px',
            height: '300px',
            background: 'radial-gradient(circle, rgba(99, 102, 241, 0.08) 0%, transparent 70%)',
            borderRadius: '50%',
            animation: 'float 8s ease-in-out infinite',
          }}
        />
        <Box
          sx={{
            position: 'absolute',
            top: '40%',
            right: '10%',
            width: '200px',
            height: '200px',
            background: 'radial-gradient(circle, rgba(236, 72, 153, 0.08) 0%, transparent 70%)',
            borderRadius: '50%',
            animation: 'float 10s ease-in-out infinite reverse',
          }}
        />
        <Box
          sx={{
            position: 'absolute',
            top: '15%',
            left: '15%',
            width: '150px',
            height: '150px',
            background: 'radial-gradient(circle, rgba(16, 185, 129, 0.08) 0%, transparent 70%)',
            borderRadius: '50%',
            animation: 'pulse 6s ease-in-out infinite',
          }}
        />
        <Box
          sx={{
            position: 'absolute',
            top: '70%',
            right: '30%',
            width: '100px',
            height: '100px',
            background: 'radial-gradient(circle, rgba(139, 92, 246, 0.08) 0%, transparent 70%)',
            borderRadius: '50%',
            animation: 'float 12s ease-in-out infinite',
          }}
        />
      </Box>

      <Container
        maxWidth="lg"
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'flex-start',
          flex: 1,
          position: 'relative',
          zIndex: 1,
          py: 4,
          minHeight: '100vh',
        }}
      >
        {/* Navigation Tabs */}
        <Box sx={{ mb: 4, display: 'flex', gap: 2, flexWrap: 'wrap', justifyContent: 'center' }}>
          {[
            { id: 'overview', label: 'Project Overview', icon: <InfoIcon /> },
            { id: 'components', label: 'Components Guide', icon: <DescriptionIcon /> },
            { id: 'guide', label: 'Step-by-Step Guide', icon: <PlayArrowIcon /> },
            { id: 'upload', label: 'Start Upload', icon: <UploadIcon /> }
          ].map((tab) => (
            <Button
              key={tab.id}
              variant={activeSection === tab.id ? "contained" : "outlined"}
              startIcon={tab.icon}
              onClick={() => setActiveSection(tab.id)}
              sx={{
                borderRadius: 3,
                px: 3,
                py: 1.5,
                fontWeight: 600,
                textTransform: 'none',
                fontSize: '0.875rem',
                background: activeSection === tab.id 
                  ? 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)'
                  : 'transparent',
                borderColor: activeSection === tab.id ? 'transparent' : 'rgba(255, 255, 255, 0.2)',
                color: activeSection === tab.id ? '#ffffff' : '#cbd5e1',
                '&:hover': {
                  background: activeSection === tab.id 
                    ? 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)'
                    : 'rgba(255, 255, 255, 0.1)',
                },
              }}
            >
              {tab.label}
            </Button>
          ))}
        </Box>

        {/* Project Overview Section */}
        {activeSection === 'overview' && (
          <Paper
            elevation={0}
            sx={{
              p: { xs: 4, md: 6 },
              background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(51, 65, 85, 0.9) 100%)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: 6,
              backdropFilter: 'blur(30px)',
              boxShadow: '0 25px 50px rgba(0, 0, 0, 0.5)',
              maxWidth: '900px',
              width: '100%',
              textAlign: 'center',
              position: 'relative',
              overflow: 'hidden',
              animation: 'fadeIn 1s ease-out',
            }}
          >
            <Box
              sx={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                height: '3px',
                background: 'linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899, #10b981)',
                borderRadius: '3px 3px 0 0',
              }}
            />

            <Typography
              variant="h1"
              sx={{
                fontSize: { xs: '2.5rem', sm: '3.5rem', md: '4rem' },
                fontWeight: 900,
                background: 'linear-gradient(135deg, #f8fafc 0%, #cbd5e1 50%, #94a3b8 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
                letterSpacing: '-0.025em',
                lineHeight: 1.1,
                textShadow: '0 0 40px rgba(248, 250, 252, 0.3)',
                mb: 3,
              }}
            >
              {projectDescription.title}
            </Typography>

            <Typography
              variant="h2"
              sx={{
                fontSize: { xs: '1.25rem', sm: '1.5rem', md: '1.75rem' },
                fontWeight: 400,
                color: '#cbd5e1',
                letterSpacing: '0.025em',
                lineHeight: 1.4,
                maxWidth: '700px',
                mx: 'auto',
                opacity: 0.9,
                mb: 4,
              }}
            >
              {projectDescription.description}
            </Typography>

            <Box sx={{ mb: 4 }}>
              <Typography
                variant="h3"
                sx={{
                  fontSize: '1.5rem',
                  fontWeight: 600,
                  color: '#f8fafc',
                  mb: 3,
                }}
              >
                Key Features
              </Typography>
              <Box
                sx={{
                  display: 'grid',
                  gridTemplateColumns: { xs: '1fr', sm: 'repeat(2, 1fr)' },
                  gap: 2,
                }}
              >
                {projectDescription.features.map((feature, index) => (
                  <Chip
                    key={index}
                    label={feature}
                    sx={{
                      background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%)',
                      color: '#f8fafc',
                      border: '1px solid rgba(99, 102, 241, 0.3)',
                      fontWeight: 500,
                      '&:hover': {
                        background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.3) 100%)',
                      },
                    }}
                  />
                ))}
              </Box>
            </Box>

            <Button
              variant="contained"
              onClick={() => setActiveSection('upload')}
              sx={{
                background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                borderRadius: 3,
                px: 4,
                py: 2,
                fontWeight: 600,
                textTransform: 'none',
                fontSize: '1.1rem',
                '&:hover': {
                  background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
                  transform: 'translateY(-2px)',
                },
              }}
            >
              Get Started
            </Button>
          </Paper>
        )}

        {/* Components Guide Section */}
        {activeSection === 'components' && (
          <Paper
            elevation={0}
            sx={{
              p: { xs: 4, md: 6 },
              background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(51, 65, 85, 0.9) 100%)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: 6,
              backdropFilter: 'blur(30px)',
              boxShadow: '0 25px 50px rgba(0, 0, 0, 0.5)',
              maxWidth: '900px',
              width: '100%',
              position: 'relative',
              overflow: 'hidden',
              animation: 'fadeIn 1s ease-out',
            }}
          >
            <Typography
              variant="h2"
              sx={{
                fontSize: { xs: '2rem', sm: '2.5rem', md: '3rem' },
                fontWeight: 700,
                color: '#f8fafc',
                mb: 4,
                textAlign: 'center',
              }}
            >
              Component Guide
            </Typography>

            {componentGuide.map((component, index) => (
              <Accordion
                key={index}
                sx={{
                  background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  borderRadius: 3,
                  mb: 2,
                  '&:before': { display: 'none' },
                  '&.Mui-expanded': {
                    background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)',
                  },
                }}
              >
                <AccordionSummary
                  expandIcon={<ExpandMoreIcon sx={{ color: '#cbd5e1' }} />}
                  sx={{
                    '& .MuiAccordionSummary-content': {
                      alignItems: 'center',
                      gap: 2,
                    },
                  }}
                >
                  <Box sx={{ color: '#6366f1', display: 'flex', alignItems: 'center' }}>
                    {component.icon}
                  </Box>
                  <Box>
                    <Typography
                      variant="h6"
                      sx={{
                        fontWeight: 600,
                        color: '#f8fafc',
                        fontSize: '1.1rem',
                      }}
                    >
                      {component.name}
                    </Typography>
                    <Typography
                      sx={{
                        color: '#94a3b8',
                        fontSize: '0.9rem',
                      }}
                    >
                      {component.description}
                    </Typography>
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  <Box>
                    <Typography
                      variant="subtitle1"
                      sx={{
                        fontWeight: 600,
                        color: '#f8fafc',
                        mb: 2,
                      }}
                    >
                      Features:
                    </Typography>
                    <List dense>
                      {component.features.map((feature, featureIndex) => (
                        <ListItem key={featureIndex} sx={{ py: 0.5 }}>
                          <ListItemIcon sx={{ minWidth: 30 }}>
                            <Box
                              sx={{
                                width: 6,
                                height: 6,
                                borderRadius: '50%',
                                background: '#6366f1',
                              }}
                            />
                          </ListItemIcon>
                          <ListItemText
                            primary={feature}
                            sx={{
                              '& .MuiListItemText-primary': {
                                color: '#cbd5e1',
                                fontSize: '0.9rem',
                              },
                            }}
                          />
                        </ListItem>
                      ))}
                    </List>
                    <Divider sx={{ my: 2, borderColor: 'rgba(255, 255, 255, 0.1)' }} />
                    <Typography
                      variant="subtitle1"
                      sx={{
                        fontWeight: 600,
                        color: '#f8fafc',
                        mb: 1,
                      }}
                    >
                      How to Use:
                    </Typography>
                    <Typography
                      sx={{
                        color: '#94a3b8',
                        fontSize: '0.9rem',
                        lineHeight: 1.6,
                      }}
                    >
                      {component.usage}
                    </Typography>
                  </Box>
                </AccordionDetails>
              </Accordion>
            ))}
          </Paper>
        )}

        {/* Step-by-Step Guide Section */}
        {activeSection === 'guide' && (
          <Paper
            elevation={0}
            sx={{
              p: { xs: 4, md: 6 },
              background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(51, 65, 85, 0.9) 100%)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: 6,
              backdropFilter: 'blur(30px)',
              boxShadow: '0 25px 50px rgba(0, 0, 0, 0.5)',
              maxWidth: '900px',
              width: '100%',
              position: 'relative',
              overflow: 'hidden',
              animation: 'fadeIn 1s ease-out',
            }}
          >
            <Typography
              variant="h2"
              sx={{
                fontSize: { xs: '2rem', sm: '2.5rem', md: '3rem' },
                fontWeight: 700,
                color: '#f8fafc',
                mb: 4,
                textAlign: 'center',
              }}
            >
              Step-by-Step Guide
            </Typography>

            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
              {stepByStepGuide.map((step, index) => (
                <Box
                  key={index}
                  sx={{
                    display: 'flex',
                    gap: 3,
                    p: 3,
                    background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: 4,
                    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                    '&:hover': {
                      background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)',
                      borderColor: 'rgba(99, 102, 241, 0.3)',
                    },
                  }}
                >
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      width: 50,
                      height: 50,
                      borderRadius: '50%',
                      background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                      color: '#ffffff',
                      fontWeight: 700,
                      fontSize: '1.2rem',
                      flexShrink: 0,
                    }}
                  >
                    {step.step}
                  </Box>
                  <Box sx={{ flex: 1 }}>
                    <Typography
                      variant="h6"
                      sx={{
                        fontWeight: 600,
                        color: '#f8fafc',
                        mb: 1,
                        fontSize: '1.1rem',
                      }}
                    >
                      {step.title}
                    </Typography>
                    <Typography
                      sx={{
                        color: '#94a3b8',
                        fontSize: '0.9rem',
                        lineHeight: 1.6,
                        mb: 2,
                      }}
                    >
                      {step.description}
                    </Typography>
                    <Chip
                      label={step.action}
                      size="small"
                      sx={{
                        background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(34, 197, 94, 0.2) 100%)',
                        color: '#10b981',
                        border: '1px solid rgba(16, 185, 129, 0.3)',
                        fontWeight: 500,
                      }}
                    />
                  </Box>
                </Box>
              ))}
            </Box>
          </Paper>
        )}

        {/* Upload Section */}
        {activeSection === 'upload' && (
          <Paper
            elevation={0}
            sx={{
              p: { xs: 4, md: 6 },
              background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(51, 65, 85, 0.9) 100%)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: 6,
              backdropFilter: 'blur(30px)',
              boxShadow: '0 25px 50px rgba(0, 0, 0, 0.5)',
              maxWidth: '900px',
              width: '100%',
              textAlign: 'center',
              position: 'relative',
              overflow: 'hidden',
              animation: 'fadeIn 1s ease-out',
            }}
          >
            <Box
              sx={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                height: '3px',
                background: 'linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899, #10b981)',
                borderRadius: '3px 3px 0 0',
              }}
            />

            <Typography
              variant="h1"
              sx={{
                fontSize: { xs: '2.5rem', sm: '3.5rem', md: '4rem' },
                fontWeight: 900,
                background: 'linear-gradient(135deg, #f8fafc 0%, #cbd5e1 50%, #94a3b8 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
                letterSpacing: '-0.025em',
                lineHeight: 1.1,
                textShadow: '0 0 40px rgba(248, 250, 252, 0.3)',
                mb: 2,
              }}
            >
              Ready to Start?
            </Typography>
            <Typography
              variant="h2"
              sx={{
                fontSize: { xs: '1.25rem', sm: '1.5rem', md: '1.75rem' },
                fontWeight: 400,
                color: '#cbd5e1',
                letterSpacing: '0.025em',
                lineHeight: 1.4,
                maxWidth: '600px',
                mx: 'auto',
                opacity: 0.9,
                mb: 4,
              }}
            >
              Upload your financial documents and let AI analyze them for you
            </Typography>

            <Box
              sx={{
                background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%)',
                border: '1px solid rgba(255, 255, 255, 0.05)',
                borderRadius: 4,
                p: 3,
                mb: 4,
              }}
            >
              <FileUpload
                onReportGenerated={onReportGenerated}
                onError={onError}
                navigate={navigate}
                showAnalyzeButton={false}
                existingFileNames={existingFileNames}
              />
            </Box>

            <Typography
              sx={{
                color: '#64748b',
                fontSize: '0.875rem',
                textAlign: 'center',
                opacity: 0.7,
              }}
            >
              Supported formats: PDF documents • Secure and private • Fast processing
            </Typography>
          </Paper>
        )}
      </Container>
    </Box>
  );
};

export default UploadPage;



