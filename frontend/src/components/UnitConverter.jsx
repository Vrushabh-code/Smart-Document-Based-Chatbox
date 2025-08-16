// import React, { useState } from 'react';
// import axios from 'axios';
// import { Box, Typography, TextField, Button, MenuItem, Select, FormControl, InputLabel, Alert, CircularProgress } from '@mui/material';

// const UnitConverter = ({ onReportGenerated, onError }) => {
//   const [conversionProfile, setConversionProfile] = useState('Default');
//   const [customMappings, setCustomMappings] = useState('');
//   const [converting, setConverting] = useState(false);
//   const [success, setSuccess] = useState(null);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     let mappings = null;
//     if (conversionProfile === 'Custom' && customMappings) {
//       try {
//         mappings = JSON.parse(customMappings);
//       } catch {
//         onError('Invalid JSON format for custom mappings.');
//         return;
//       }
//     }

//     setConverting(true);
//     try {
//       const response = await axios.post('http://localhost:8000/api/convert-units', {
//         conversion_profile: conversionProfile,
//         custom_mappings: mappings,
//       });
//       onReportGenerated(response.data);
//       setSuccess('Units converted successfully.');
//     } catch (error) {
//       onError(error.response?.data?.detail || 'Error converting units.');
//     } finally {
//       setConverting(false);
//     }
//   };

//   return (
//     <Box sx={{ mb: 2, bgcolor: '#27292D', p: 2 }}>
//       <Typography variant="h3" gutterBottom color="text.primary" sx={{ mb: 2 }}>
//         Unit Converter
//       </Typography>
//       {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}
//       <form onSubmit={handleSubmit}>
//         <FormControl fullWidth sx={{ mb: 2 }}>
//           <InputLabel>Conversion Profile</InputLabel>
//           <Select
//             value={conversionProfile}
//             onChange={(e) => setConversionProfile(e.target.value)}
//             label="Conversion Profile"
//             sx={{ bgcolor: 'background.paper', borderRadius: 1 }}
//           >
//             <MenuItem value="Default">Default</MenuItem>
//             <MenuItem value="Words to Symbols">Words to Symbols</MenuItem>
//             <MenuItem value="Custom">Custom</MenuItem>
//           </Select>
//         </FormControl>
//         {conversionProfile === 'Custom' && (
//           <TextField
//             fullWidth
//             multiline
//             rows={4}
//             label="Custom Mappings (JSON)"
//             value={customMappings}
//             onChange={(e) => setCustomMappings(e.target.value)}
//             placeholder='{"%": "percent", "$": "USD"}'
//             sx={{ mb: 2, bgcolor: 'background.paper', borderRadius: 1 }}
//           />
//         )}
//         <Button
//           type="submit"
//           variant="contained"
//           color="secondary"
//           disabled={converting}
//           startIcon={converting ? <CircularProgress size={20} /> : null}
//           sx={{ mt: 1 }}
//         >
//           {converting ? 'Converting...' : 'Convert Units'}
//         </Button>
//       </form>
//     </Box>
//   );
// };

// export default UnitConverter;

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


import React, { useState } from 'react';
import axios from 'axios';
import { Box, Typography, TextField, Button, MenuItem, Select, FormControl, InputLabel, Alert, CircularProgress } from '@mui/material';

const UnitConverter = ({ onReportGenerated, onError }) => {
  const [conversionProfile, setConversionProfile] = useState('Default');
  const [customMappings, setCustomMappings] = useState('');
  const [converting, setConverting] = useState(false);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    let mappings = null;
    if (conversionProfile === 'Custom' && customMappings) {
      try {
        mappings = JSON.parse(customMappings);
      } catch {
        onError('Invalid JSON format for custom mappings.');
        return;
      }
    }

    setConverting(true);
    try {
      const response = await axios.post('http://localhost:8000/api/convert-units', {
        conversion_profile: conversionProfile,
        custom_mappings: mappings,
      });
      onReportGenerated(response.data);
      setSuccess('Units converted successfully.');
    } catch (error) {
      onError(error.response?.data?.detail || 'Error converting units.');
    } finally {
      setConverting(false);
    }
  };

  return (
    <Box sx={{ mb: 2, bgcolor: '#27292D', p: 2 }}>
      <Typography variant="h3" gutterBottom color="text.primary" sx={{ mb: 2 }}>
        Unit Converter
      </Typography>
      {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}
      <form onSubmit={handleSubmit}>
        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel>Conversion Profile</InputLabel>
          <Select
            value={conversionProfile}
            onChange={(e) => setConversionProfile(e.target.value)}
            label="Conversion Profile"
            sx={{ bgcolor: 'background.paper', borderRadius: 2, height: '40px' }}
          >
            <MenuItem value="Default">Default</MenuItem>
            <MenuItem value="Words to Symbols">Words to Symbols</MenuItem>
            <MenuItem value="Custom">Custom</MenuItem>
          </Select>
        </FormControl>
        {conversionProfile === 'Custom' && (
          <TextField
            fullWidth
            multiline
            rows={4}
            label="Custom Mappings (JSON)"
            value={customMappings}
            onChange={(e) => setCustomMappings(e.target.value)}
            placeholder='{"%": "percent", "$": "USD"}'
            sx={{ mb: 2, bgcolor: 'background.paper', borderRadius: 2, minHeight: '80px' }}
          />
        )}
        <Button
          type="submit"
          variant="contained"
          color="secondary"
          disabled={converting}
          startIcon={converting ? <CircularProgress size={20} /> : null}
          sx={{ mt: 1 }}
        >
          {converting ? 'Converting...' : 'Convert Units'}
        </Button>
      </form>
    </Box>
  );
};

export default UnitConverter;






