import { createSlice, PayloadAction } from "@reduxjs/toolkit"

type AuthState = {
  isAuthenticated: boolean;
}

const initialState: AuthState = {
  isAuthenticated: false,
}

export const auth = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logOut: (state) => {
      state.isAuthenticated = false
    },
    logIn: (state, _action: PayloadAction<void>) => {
      state.isAuthenticated = true
    },
  }
})

export const { logIn, logOut } = auth.actions
export default auth.reducer