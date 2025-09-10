import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const API_URL = 'http://localhost:8000/api';

export const loginUser = createAsyncThunk(
  'auth/loginUser',
  async (credentials, { rejectWithValue }) => {
    try {
      const response = await axios.post(`${API_URL}/users/auth/login/`, credentials);
      const { access, refresh } = response.data.payload.tokens;

      const decodedUser = jwtDecode(access);

      return {
        user: {
          id: decodedUser.user_id,
          name: decodedUser.name,
          email: decodedUser.email,
          role: decodedUser.role,
        },
        tokens: { access, refresh },
      };
    } catch (err) {
      return rejectWithValue("Login failed");
    }
  }
);

export const registerUser = createAsyncThunk(
  'auth/registerUser',
  async (formData, { rejectWithValue }) => {
    try {
      const response = await axios.post(`${API_URL}/users/auth/register/`, formData);
      const { access, refresh } = response.data.payload.tokens;

      const decodedUser = jwtDecode(access);

      return {
        user: {
          id: decodedUser.user_id,
          name: decodedUser.name,
          email: decodedUser.email,
          role: decodedUser.role,
        },
        tokens: { access, refresh },
      };
    } catch (err) {
      return rejectWithValue("Registration failed");
    }
  }
);

const initialState = {
  user: null,
  access: localStorage.getItem('access') || null,
  refresh: localStorage.getItem('refresh') || null,
  isAuthenticated: !!localStorage.getItem('access'),
  loading: false,
  error: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: (state) => {
      state.user = null;
      state.access = null;
      state.refresh = null;
      state.isAuthenticated = false;
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
    },
  },
  extraReducers: (builder) => {
    builder
      // LOGIN
      .addCase(loginUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload.user;
        state.access = action.payload.tokens.access;
        state.refresh = action.payload.tokens.refresh;
        state.isAuthenticated = true;

        localStorage.setItem('access', action.payload.tokens.access);
        localStorage.setItem('refresh', action.payload.tokens.refresh);
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // REGISTER
      .addCase(registerUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(registerUser.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload.user;
        state.access = action.payload.tokens.access;
        state.refresh = action.payload.tokens.refresh;
        state.isAuthenticated = true;

        localStorage.setItem('access', action.payload.tokens.access);
        localStorage.setItem('refresh', action.payload.tokens.refresh);
      })
      .addCase(registerUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;
