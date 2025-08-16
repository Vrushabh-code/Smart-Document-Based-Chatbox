// import React from 'react';
// import ReactDOM from 'react-dom/client';
// import { ThemeProvider } from '@mui/material/styles';
// import theme from './theme';
// import App from './App';
// import './App.css';
// import { BrowserRouter } from 'react-router-dom';

// // Make openPDF globally accessible
// window.openPDF = function (pdfName, page) {
//   const viewerUrl = `/pdf-viewer?file=${encodeURIComponent(pdfName)}&page=${page}`;
//   window.open(viewerUrl, "_blank");
// };

// const root = ReactDOM.createRoot(document.getElementById('root'));
// root.render(
//   <ThemeProvider theme={theme}>
//     <BrowserRouter>
//       <App />
//     </BrowserRouter>
//   </ThemeProvider>
// );

//////////////////////////////////////////////////////////////grok/////////////////////////////////////////////////////////////////////

import React from 'react';
import ReactDOM from 'react-dom/client';
import { ThemeProvider } from '@mui/material/styles';
import theme from './theme';
import App from './App';
import './App.css';
import { BrowserRouter } from 'react-router-dom';
// import { Amplify } from 'aws-amplify';
// import { awsConfig } from './aws-exports';

// // Configure Amplify
// Amplify.configure({ Auth: awsConfig.Auth });

// Make openPDF globally accessible
window.openPDF = function (pdfName, page) {
  const viewerUrl = `/pdf-viewer?file=${encodeURIComponent(pdfName)}&page=${page}`;
  window.open(viewerUrl, '_blank');
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <ThemeProvider theme={theme}>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </ThemeProvider>
);








