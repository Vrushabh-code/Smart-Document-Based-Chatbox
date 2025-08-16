<<<<<<< HEAD
# FinanceBot - AI-Powered Financial Document Analysis

## 🚀 Project Overview

FinanceBot is an intelligent web application that uses advanced AI to analyze financial documents, extract key insights, and provide comprehensive reports. Perfect for investors, analysts, and anyone needing to understand financial documents quickly and accurately.

## ✨ Key Features

- **AI-Powered Analysis**: Advanced text extraction and financial data identification
- **Interactive Chat Interface**: Ask questions about your documents using natural language
- **Comprehensive Reports**: Detailed business overview, financial metrics, and key findings
- **PDF Viewer with Citations**: View documents with highlighted citations and source tracking
- **Export Capabilities**: Download reports in multiple formats
- **Real-time Processing**: Live analysis with progress tracking
- **Multi-file Support**: Upload and analyze multiple PDF documents simultaneously

## 🏗️ Architecture

### Frontend Components

1. **UploadPage** - Enhanced landing page with project overview and navigation
   - Project description and features
   - Component guide with detailed explanations
   - Step-by-step user guide
   - File upload interface

2. **FileUpload Component**
   - Drag & drop PDF file upload
   - Multiple file support
   - File validation and preview
   - Progress tracking during upload

3. **ReportDisplay Component**
   - Business overview extraction
   - Financial metrics analysis
   - Key thesis points identification
   - Interactive data visualization
   - Export functionality

4. **ChatBox Component**
   - Natural language questions
   - Citation-based answers
   - Context-aware responses
   - Document-specific insights

5. **PDF Viewer Components**
   - Inline PDF viewing
   - Citation highlighting
   - Page navigation
   - Text extraction display

6. **Main Dashboard**
   - Integrated help system
   - Contextual tooltips
   - Section navigation
   - File management

### Backend Services

- **Document Processing**: PDF text extraction and analysis
- **AI Analysis Engine**: Financial data identification and insight generation
- **Chat Interface**: Natural language processing for document queries
- **Report Generation**: Comprehensive analysis report creation

## 🎯 User Experience Features

### Navigation System
- **Tabbed Interface**: Easy navigation between different sections
- **Contextual Help**: Tooltips and help dialogs for each component
- **Step-by-Step Guide**: Clear instructions for new users
- **Component Descriptions**: Detailed explanations of each feature

### Help System
- **Help Button**: Accessible help dialog with comprehensive information
- **Tooltips**: Contextual information on hover
- **Component Guide**: Detailed breakdown of each component's functionality
- **Usage Instructions**: Clear guidance on how to use each feature

## 🚀 Getting Started

### Prerequisites
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- Required Python packages (see backend/requirements.txt)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd 14-7-2025
   ```

2. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Install backend dependencies**
   ```bash
   cd ../backend
   pip install -r requirements.txt
   ```

4. **Start the backend server**
   ```bash
   python main1.py
   ```

5. **Start the frontend development server**
   ```bash
   cd ../frontend
   npm start
   ```

6. **Open your browser**
   Navigate to `http://localhost:3000`

## 📖 How to Use

### 1. Project Overview
- Start at the landing page to understand the project
- Review the component guide to learn about each feature
- Follow the step-by-step guide for detailed instructions

### 2. Upload Documents
- Drag and drop PDF files or click to browse
- Supported formats: PDF documents
- Upload multiple files for comprehensive analysis

### 3. Analyze Documents
- Click "Analyze Files" to start AI-powered analysis
- Monitor progress with real-time updates
- Wait for analysis completion

### 4. Review Results
- View comprehensive reports in the "Report Display" section
- Explore business overview, financial metrics, and key insights
- Use export features to download reports

### 5. Chat with Documents
- Switch to "Chat with the Report" section
- Ask questions about your documents using natural language
- Click on citations to view source material

### 6. View PDFs
- Access uploaded PDFs with citation highlighting
- Navigate between pages while maintaining context
- View exact source of information referenced in analysis

## 🎨 UI/UX Features

### Modern Design
- **Glassmorphism Effects**: Beautiful backdrop blur and transparency
- **Gradient Backgrounds**: Dynamic color schemes
- **Smooth Animations**: Engaging user interactions
- **Responsive Design**: Works on all device sizes

### User Interface
- **Intuitive Navigation**: Clear and logical flow
- **Contextual Help**: Tooltips and information dialogs
- **Progress Indicators**: Real-time feedback on operations
- **Error Handling**: Clear error messages and recovery options

### Accessibility
- **Keyboard Navigation**: Full keyboard support
- **Screen Reader Support**: Proper ARIA labels
- **High Contrast**: Readable text and elements
- **Focus Management**: Clear focus indicators

## 🔧 Technical Stack

### Frontend
- **React.js**: Modern UI framework
- **Material-UI**: Component library
- **React Router**: Navigation
- **Axios**: HTTP client

### Backend
- **Python**: Server-side logic
- **FastAPI**: Web framework
- **AI/ML Libraries**: Document analysis
- **PDF Processing**: Text extraction

## 📁 Project Structure

```
14-7-2025/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadPage.jsx          # Enhanced landing page
│   │   │   ├── FileUpload.jsx          # File upload component
│   │   │   ├── ReportDisplay.jsx       # Report display
│   │   │   ├── ChatBox.jsx             # Chat interface
│   │   │   ├── PDFViewerPage.jsx       # PDF viewer
│   │   │   └── ...
│   │   ├── App.js                      # Main application
│   │   └── App.css                     # Styling
│   └── package.json
├── backend/
│   ├── main1.py                        # Main server
│   ├── endpoint.py                     # API endpoints
│   ├── rag_pipeline.py                 # AI analysis
│   └── requirements.txt
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the help system within the application
- Review the component guide for detailed explanations
- Contact the development team

## 🔮 Future Enhancements

- Enhanced AI capabilities
- Additional export formats
- Mobile app version
- Advanced analytics dashboard
- Integration with external data sources
- Collaborative features

---

**FinanceBot** - Making financial document analysis intelligent and accessible.
=======
# Smart-Document-Based-Chatbox
Built a financial research assistant for PDF-based querying using LangChain’s RAG with inline citations. • Developed key frontend features like file upload, chat UI, and PDF downloads using React, MUI, and Axios. • Integrated FastAPI backend with UUID-based sessions to retain chat context and optimized response time.
>>>>>>> ea0abced7f548cadcac5518382712f3358c12c17
