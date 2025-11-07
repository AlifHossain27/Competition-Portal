"use client";

import { Provider } from "react-redux";
import { store } from "@/redux/store";
import LoginForm from "./LoginForm";

export default function LoginPage() {
  return (
    <Provider store={store}>
      <LoginForm />
    </Provider>
  );
}
