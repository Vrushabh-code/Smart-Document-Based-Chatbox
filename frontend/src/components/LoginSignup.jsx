// import React, { useState } from 'react';
// import { Box, Typography, TextField, Button, Alert, Tabs, Tab } from '@mui/material';
// import { useNavigate } from 'react-router-dom';

// import { Amplify } from 'aws-amplify';
// import { Auth } from 'aws-amplify/auth'; // ✅ FIXED
// import { awsConfig } from '../aws-exports';

// Amplify.configure(awsConfig);


// // Amplify.configure({
// //   Auth: {
// //     region: 'ap-south-1',
// //     userPoolId: 'ap-south-1_AZCS9lsWB', // ✅ from your user pool
// //     userPoolWebClientId: '6pfosklggg4vej9csjmjg862e5', // ✅ your App Client ID
// //   }
// // });
  

// // Amplify.configure(authConfig);

// const LoginSignup = () => {
//   const [activeTab, setActiveTab] = useState('login');
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');
//   const [confirmPassword, setConfirmPassword] = useState('');
//   const [otp, setOtp] = useState('');
//   const [error, setError] = useState(null);
//   const [showOtpField, setShowOtpField] = useState(false);
//   const [isLoading, setIsLoading] = useState(false);
//   const navigate = useNavigate();

//   const handleTabChange = (event, newValue) => {
//     setActiveTab(newValue);
//     setError(null);
//     setEmail('');
//     setPassword('');
//     setConfirmPassword('');
//     setOtp('');
//     setShowOtpField(false);
//   };

//   const handleLogin = async (e) => {
//     e.preventDefault();
//     setError(null);
//     setIsLoading(true);
  
//     try {
//         await Auth.signIn(email, password);
//       navigate('/');
//     } catch (err) {
//       setError('Invalid email or password. Please try again.');
//       console.error('Login error:', err);
//     } finally {
//       setIsLoading(false);
//     }
//   };
  

//   const handleSignup = async (e) => {
//     e.preventDefault();
//     setError(null);
  
//     if (password !== confirmPassword) {
//       setError('Passwords do not match.');
//       return;
//     }
  
//     setIsLoading(true);
//     try {
//         await Auth.signUp({
//             username: email,
//             password,
//             options: {
//               userAttributes: {
//                 email,
//               },
//             },
//           });
          
//       setShowOtpField(true);
//     } catch (err) {
//       setError(err.message || 'Error signing up. Please try again.');
//       console.error('Signup error:', err);
//     } finally {
//       setIsLoading(false);
//     }
//   };
  

//   const handleOtpVerification = async (e) => {
//     e.preventDefault();
//     setError(null);
//     setIsLoading(true);
  
//     try {
//         await Auth.confirmSignUp(email, otp);
//         await Auth.signIn(email, password);
//       navigate('/');
//     } catch (err) {
//       setError('Invalid OTP. Please try again.');
//       console.error('OTP verification error:', err);
//     } finally {
//       setIsLoading(false);
//     }
//   };
  

//   return (
//     <Box
//       sx={{
//         display: 'flex',
//         flexDirection: 'column',
//         alignItems: 'center',
//         justifyContent: 'center',
//         minHeight: '100vh',
//         bgcolor: '#27292D',
//         color: '#ffffff',
//         p: 2,
//       }}
//     >
//       <Typography
//         variant="h1"
//         sx={{
//           mb: 4,
//           fontSize: { xs: '2.5rem', sm: '3.5rem', md: '4.5rem' },
//           fontWeight: 'bold',
//           textAlign: 'center',
//           color: '#b0bec5',
//         }}
//       >
//         FinanceBot
//       </Typography>

//       <Box sx={{ width: '100%', maxWidth: 400, bgcolor: '#2F3135', borderRadius: 3, p: 3 }}>
//         <Tabs
//           value={activeTab}
//           onChange={handleTabChange}
//           centered
//           sx={{
//             mb: 3,
//             '.MuiTab-root': { color: '#b0bec5', textTransform: 'none', fontSize: '1.1rem' },
//             '.Mui-selected': { color: '#42a5f5' },
//             '.MuiTabs-indicator': { backgroundColor: '#42a5f5' },
//           }}
//         >
//           <Tab label="Login" value="login" />
//           <Tab label="Sign Up" value="signup" />
//         </Tabs>

//         {error && (
//           <Alert severity="error" sx={{ mb: 2 }}>
//             {error}
//           </Alert>
//         )}

//         {activeTab === 'login' && (
//           <Box component="form" onSubmit={handleLogin} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
//             <TextField
//               label="Email"
//               type="email"
//               value={email}
//               onChange={(e) => setEmail(e.target.value)}
//               required
//               fullWidth
//               sx={{
//                 input: { color: '#ffffff' },
//                 label: { color: '#b0bec5' },
//                 '& .MuiOutlinedInput-root': {
//                   '& fieldset': { borderColor: '#424242' },
//                   '&:hover fieldset': { borderColor: '#b0bec5' },
//                   '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
//                 },
//               }}
//             />
//             <TextField
//               label="Password"
//               type="password"
//               value={password}
//               onChange={(e) => setPassword(e.target.value)}
//               required
//               fullWidth
//               sx={{
//                 input: { color: '#ffffff' },
//                 label: { color: '#b0bec5' },
//                 '& .MuiOutlinedInput-root': {
//                   '& fieldset': { borderColor: '#424242' },
//                   '&:hover fieldset': { borderColor: '#b0bec5' },
//                   '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
//                 },
//               }}
//             />
//             <Button
//               type="submit"
//               variant="contained"
//               disabled={isLoading}
//               sx={{
//                 bgcolor: '#42a5f5',
//                 '&:hover': { bgcolor: '#1e88e5' },
//                 borderRadius: 3,
//                 textTransform: 'none',
//                 fontSize: '1.1rem',
//                 py: 1,
//               }}
//             >
//               {isLoading ? 'Logging in...' : 'Login'}
//             </Button>
//           </Box>
//         )}

//         {activeTab === 'signup' && !showOtpField && (
//           <Box component="form" onSubmit={handleSignup} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
//             <TextField
//               label="Email"
//               type="email"
//               value={email}
//               onChange={(e) => setEmail(e.target.value)}
//               required
//               fullWidth
//               sx={{
//                 input: { color: '#ffffff' },
//                 label: { color: '#b0bec5' },
//                 '& .MuiOutlinedInput-root': {
//                   '& fieldset': { borderColor: '#424242' },
//                   '&:hover fieldset': { borderColor: '#b0bec5' },
//                   '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
//                 },
//               }}
//             />
//             <TextField
//               label="Password"
//               type="password"
//               value={password}
//               onChange={(e) => setPassword(e.target.value)}
//               required
//               fullWidth
//               sx={{
//                 input: { color: '#ffffff' },
//                 label: { color: '#b0bec5' },
//                 '& .MuiOutlinedInput-root': {
//                   '& fieldset': { borderColor: '#424242' },
//                   '&:hover fieldset': { borderColor: '#b0bec5' },
//                   '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
//                 },
//               }}
//             />
//             <TextField
//               label="Confirm Password"
//               type="password"
//               value={confirmPassword}
//               onChange={(e) => setConfirmPassword(e.target.value)}
//               required
//               fullWidth
//               sx={{
//                 input: { color: '#ffffff' },
//                 label: { color: '#b0bec5' },
//                 '& .MuiOutlinedInput-root': {
//                   '& fieldset': { borderColor: '#424242' },
//                   '&:hover fieldset': { borderColor: '#b0bec5' },
//                   '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
//                 },
//               }}
//             />
//             <Button
//               type="submit"
//               variant="contained"
//               disabled={isLoading}
//               sx={{
//                 bgcolor: '#42a5f5',
//                 '&:hover': { bgcolor: '#1e88e5' },
//                 borderRadius: 3,
//                 textTransform: 'none',
//                 fontSize: '1.1rem',
//                 py: 1,
//               }}
//             >
//               {isLoading ? 'Sending OTP...' : 'Get OTP'}
//             </Button>
//           </Box>
//         )}

//         {activeTab === 'signup' && showOtpField && (
//           <Box component="form" onSubmit={handleOtpVerification} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
//             <TextField
//               label="Enter OTP"
//               value={otp}
//               onChange={(e) => setOtp(e.target.value)}
//               required
//               fullWidth
//               sx={{
//                 input: { color: '#ffffff' },
//                 label: { color: '#b0bec5' },
//                 '& .MuiOutlinedInput-root': {
//                   '& fieldset': { borderColor: '#424242' },
//                   '&:hover fieldset': { borderColor: '#b0bec5' },
//                   '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
//                 },
//               }}
//             />
//             <Button
//               type="submit"
//               variant="contained"
//               disabled={isLoading}
//               sx={{
//                 bgcolor: '#42a5f5',
//                 '&:hover': { bgcolor: '#1e88e5' },
//                 borderRadius: 3,
//                 textTransform: 'none',
//                 fontSize: '1.1rem',
//                 py: 1,
//               }}
//             >
//               {isLoading ? 'Verifying...' : 'Verify OTP'}
//             </Button>
//           </Box>
//         )}
//       </Box>
//     </Box>
//   );
// };

// export default LoginSignup;


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
import React, { useState } from 'react';
import { Box, Typography, TextField, Button, Alert, Tabs, Tab } from '@mui/material';
import { useNavigate } from 'react-router-dom';

import { Amplify } from 'aws-amplify';
import { signIn, signUp, confirmSignUp } from 'aws-amplify/auth';
import { awsConfig } from '../aws-exports';

Amplify.configure({ Auth: awsConfig.Auth }); // ✅ THIS IS THE FIX
// s loginWith error
const LoginSignup = () => {
  const [activeTab, setActiveTab] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [otp, setOtp] = useState('');
  const [error, setError] = useState(null);
  const [showOtpField, setShowOtpField] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
    setError(null);
    setEmail('');
    setPassword('');
    setConfirmPassword('');
    setOtp('');
    setShowOtpField(false);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
  
    try {
      const { username, password } = { username: email, password }; // Explicitly define the object
      console.log('Attempting to sign in with:', { username, password });
      await signIn({ username, password });
      navigate('/');
    } catch (err) {
      console.error('Login error details:', err);
      setError(`Invalid email or password. Details: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setIsLoading(true);
    try {
      await signUp({
        username: email,
        password,
        options: {
          userAttributes: {
            email,
          },
        },
      });

      setShowOtpField(true);
    } catch (err) {
      setError(err.message || 'Error signing up. Please try again.');
      console.error('Signup error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleOtpVerification = async (e) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      await confirmSignUp({ username: email, confirmationCode: otp });
      await signIn({ username: email, password });
      navigate('/');
    } catch (err) {
      setError('Invalid OTP. Please try again.');
      console.error('OTP verification error:', err);
    } finally {
      setIsLoading(false);
    }
  };

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
          mb: 4,
          fontSize: { xs: '2.5rem', sm: '3.5rem', md: '4.5rem' },
          fontWeight: 'bold',
          textAlign: 'center',
          color: '#b0bec5',
        }}
      >
        FinanceBot
      </Typography>

      <Box sx={{ width: '100%', maxWidth: 400, bgcolor: '#2F3135', borderRadius: 3, p: 3 }}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          centered
          sx={{
            mb: 3,
            '.MuiTab-root': { color: '#b0bec5', textTransform: 'none', fontSize: '1.1rem' },
            '.Mui-selected': { color: '#42a5f5' },
            '.MuiTabs-indicator': { backgroundColor: '#42a5f5' },
          }}
        >
          <Tab label="Login" value="login" />
          <Tab label="Sign Up" value="signup" />
        </Tabs>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {activeTab === 'login' && (
          <Box component="form" onSubmit={handleLogin} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              fullWidth
              sx={{
                input: { color: '#ffffff' },
                label: { color: '#b0bec5' },
                '& .MuiOutlinedInput-root': {
                  '& fieldset': { borderColor: '#424242' },
                  '&:hover fieldset': { borderColor: '#b0bec5' },
                  '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
                },
              }}
            />
            <TextField
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              fullWidth
              sx={{
                input: { color: '#ffffff' },
                label: { color: '#b0bec5' },
                '& .MuiOutlinedInput-root': {
                  '& fieldset': { borderColor: '#424242' },
                  '&:hover fieldset': { borderColor: '#b0bec5' },
                  '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
                },
              }}
            />
            <Button
              type="submit"
              variant="contained"
              disabled={isLoading}
              sx={{
                bgcolor: '#42a5f5',
                '&:hover': { bgcolor: '#1e88e5' },
                borderRadius: 3,
                textTransform: 'none',
                fontSize: '1.1rem',
                py: 1,
              }}
            >
              {isLoading ? 'Logging in...' : 'Login'}
            </Button>
          </Box>
        )}

        {activeTab === 'signup' && !showOtpField && (
          <Box component="form" onSubmit={handleSignup} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              fullWidth
              sx={{
                input: { color: '#ffffff' },
                label: { color: '#b0bec5' },
                '& .MuiOutlinedInput-root': {
                  '& fieldset': { borderColor: '#424242' },
                  '&:hover fieldset': { borderColor: '#b0bec5' },
                  '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
                },
              }}
            />
            <TextField
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              fullWidth
              sx={{
                input: { color: '#ffffff' },
                label: { color: '#b0bec5' },
                '& .MuiOutlinedInput-root': {
                  '& fieldset': { borderColor: '#424242' },
                  '&:hover fieldset': { borderColor: '#b0bec5' },
                  '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
                },
              }}
            />
            <TextField
              label="Confirm Password"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              fullWidth
              sx={{
                input: { color: '#ffffff' },
                label: { color: '#b0bec5' },
                '& .MuiOutlinedInput-root': {
                  '& fieldset': { borderColor: '#424242' },
                  '&:hover fieldset': { borderColor: '#b0bec5' },
                  '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
                },
              }}
            />
            <Button
              type="submit"
              variant="contained"
              disabled={isLoading}
              sx={{
                bgcolor: '#42a5f5',
                '&:hover': { bgcolor: '#1e88e5' },
                borderRadius: 3,
                textTransform: 'none',
                fontSize: '1.1rem',
                py: 1,
              }}
            >
              {isLoading ? 'Sending OTP...' : 'Get OTP'}
            </Button>
          </Box>
        )}

        {activeTab === 'signup' && showOtpField && (
          <Box component="form" onSubmit={handleOtpVerification} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Enter OTP"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              required
              fullWidth
              sx={{
                input: { color: '#ffffff' },
                label: { color: '#b0bec5' },
                '& .MuiOutlinedInput-root': {
                  '& fieldset': { borderColor: '#424242' },
                  '&:hover fieldset': { borderColor: '#b0bec5' },
                  '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
                },
              }}
            />
            <Button
              type="submit"
              variant="contained"
              disabled={isLoading}
              sx={{
                bgcolor: '#42a5f5',
                '&:hover': { bgcolor: '#1e88e5' },
                borderRadius: 3,
                textTransform: 'none',
                fontSize: '1.1rem',
                py: 1,
              }}
            >
              {isLoading ? 'Verifying...' : 'Verify OTP'}
            </Button>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default LoginSignup;





