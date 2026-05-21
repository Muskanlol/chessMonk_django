// const BASE_URL = 'http://127.0.0.1:8000/api/users';

// // Fix browser autofill overriding dark background
// // Chrome ignores CSS for autofill, so we re-apply styles via JS after fill
// document.addEventListener('animationstart', (e) => {
//   if (e.animationName === 'onAutoFillStart') {
//     e.target.style.setProperty('background', 'rgba(255,236,204,0.04)', 'important');
//     e.target.style.setProperty('color', '#FFECCC', 'important');
//   }
// });

// // ─── TAB SWITCHING ────────────────────────────────────────────────────────────
// function switchTab(tab) {
//   const loginForm = document.getElementById('login-form');
//   const registerForm = document.getElementById('register-form');
//   const tabs = document.querySelectorAll('.tab');

//   // Hide both, then show the selected one
//   loginForm.classList.add('hidden');
//   registerForm.classList.add('hidden');
//   tabs.forEach(t => t.classList.remove('active'));

//   if (tab === 'login') {
//     loginForm.classList.remove('hidden');
//     tabs[0].classList.add('active');
//   } else {
//     registerForm.classList.remove('hidden');
//     tabs[1].classList.add('active');
//   }

//   clearMessage();
// }

// // ─── MESSAGE BOX ─────────────────────────────────────────────────────────────
// function showMessage(text, type = 'error') {
//   const box = document.getElementById('message-box');
//   box.textContent = text;
//   box.className = `message-box ${type}`;
// }

// function clearMessage() {
//   const box = document.getElementById('message-box');
//   box.className = 'message-box hidden';
// }

// // ─── REGISTER ─────────────────────────────────────────────────────────────────
// async function handleRegister() {
//   const name     = document.getElementById('reg-name').value.trim();
//   const age      = document.getElementById('reg-age').value;
//   const gender   = document.getElementById('reg-gender').value;
//   const email    = document.getElementById('reg-email').value.trim();
//   const password = document.getElementById('reg-password').value;
//   const picFile  = document.getElementById('reg-pic').files[0];

//   // ── Frontend validation ──
//   if (!name || !email || !password) {
//     return showMessage('Name, email and password are required.');
//   }
//   if (password.length < 8) {
//     return showMessage('Password must be at least 8 characters.');
//   }

//   /*
//     Why FormData and not JSON.stringify?
//     Files (images) cannot be serialized into JSON.
//     FormData creates a multipart/form-data request that can carry
//     both text fields and binary files in one request.
//     Django reads text fields via request.data and files via request.FILES.
//   */
//   const formData = new FormData();
//   formData.append('full_name', name);
//   formData.append('age', age);
//   formData.append('gender', gender);
//   formData.append('email', email);
//   formData.append('password', password);
//   if (picFile) formData.append('profile_pic', picFile);

//   try {
//     const response = await fetch(`${BASE_URL}/register/`, {
//       method: 'POST',
//       body: formData,
//       // DO NOT set Content-Type header when using FormData
//       // The browser sets it automatically with the correct boundary string
//     });

//     const data = await response.json();

//     if (response.ok) {
//       // Save tokens to localStorage
//       saveTokens(data.tokens);
//       // Save user info for dashboard use
//       localStorage.setItem('user', JSON.stringify(data.user));
//       // Redirect to dashboard
//       window.location.href = 'dashboard.html';
//     } else {
//       // DRF returns errors as { field: [messages] }
//       const errors = Object.values(data).flat().join(' ');
//       showMessage(errors);
//     }
//   } catch (err) {
//     showMessage('Network error. Is Django running?');
//   }
// }

// // ─── LOGIN ────────────────────────────────────────────────────────────────────
// async function handleLogin() {
//   const email    = document.getElementById('login-email').value.trim();
//   const password = document.getElementById('login-password').value;

//   if (!email || !password) {
//     return showMessage('Email and password are required.');
//   }

//   try {
//     const response = await fetch(`${BASE_URL}/login/`, {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       // Login sends JSON (no file), so JSON.stringify is fine here
//       body: JSON.stringify({ email, password }),
//     });

//     const data = await response.json();

//     // if (response.ok) {
//     //   saveTokens(data.tokens);
//     //   localStorage.setItem('user', JSON.stringify(data.user));
//     //   window.location.href = 'dashboard.html';
//     // } else {
//     //   const errors = Object.values(data).flat().join(' ');
//     //   showMessage(errors);
//     // }

//     if(res.ok){
//   localStorage.setItem('access_token',data.tokens.access);
//   localStorage.setItem('refresh_token',data.tokens.refresh);
//   localStorage.setItem('user',JSON.stringify(data.user));
//   window.location.href='dashboard.html';  // no setTimeout, no slash
// }
//   } catch (err) {
//     showMessage('Network error. Is Django running?');
//   }
// }

// // ─── TOKEN HELPERS ────────────────────────────────────────────────────────────
// function saveTokens(tokens) {
//   localStorage.setItem('access_token', tokens.access);
//   localStorage.setItem('refresh_token', tokens.refresh);
// }

// /*
//   Use this function in ALL future API calls that need authentication.
//   It attaches the access token to the Authorization header.
//   If you get a 401 back, call refreshAccessToken() then retry.
// */
// function getAuthHeaders() {
//   const token = localStorage.getItem('access_token');
//   return {
//     'Content-Type': 'application/json',
//     'Authorization': `Bearer ${token}`
//   };
// }

// // ─── TOKEN REFRESH ────────────────────────────────────────────────────────────
// async function refreshAccessToken() {
//   const refresh = localStorage.getItem('refresh_token');
//   if (!refresh) {
//     // No refresh token → force logout
//     logout();
//     return null;
//   }

//   const response = await fetch(`${BASE_URL}/token/refresh/`, {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ refresh }),
//   });
 
//   if (response.ok) {
//     const data = await response.json();
//     localStorage.setItem('access_token', data.access);
//     return data.access;
//   } else {
//     logout();
//     return null;
//   }
// }


// function logout() {
//   localStorage.removeItem('access_token');
//   localStorage.removeItem('refresh_token');
//   localStorage.removeItem('user');
//   window.location.href = 'index.html';
// }