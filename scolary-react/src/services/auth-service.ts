import { LoginResponse } from "@/models/auth";
import { apiRequest } from "./api-client";

const TOKEN_STORAGE_KEY = "scolary_token_value";
const ACCESS_TOKEN_KEY = "token";

const persistAccessToken = (token: LoginResponse) => {
  if (typeof window === "undefined") {
    return;
  }

  try {
    window.localStorage.setItem(TOKEN_STORAGE_KEY, JSON.stringify(token));
    window.localStorage.setItem(ACCESS_TOKEN_KEY, token.access_token);
    window.sessionStorage?.setItem(ACCESS_TOKEN_KEY, token.access_token);
  } catch (error) {
    console.warn("Failed to persist auth token", error);
  }
};

export const clearAuthSession = () => {
  if (typeof window === "undefined") {
    return;
  }

  try {
    window.localStorage.removeItem(TOKEN_STORAGE_KEY);
    window.localStorage.removeItem(ACCESS_TOKEN_KEY);
    window.sessionStorage?.removeItem(ACCESS_TOKEN_KEY);
  } catch (error) {
    console.warn("Failed to clear auth token", error);
  }
};

export const loginWithCredentials = async (email: string, password: string) => {
  const formData = new URLSearchParams();
  formData.set("username", email);
  formData.set("password", password);

  const response = await apiRequest<LoginResponse>("/login/access-token", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: formData.toString()
  });

  persistAccessToken(response);

  return response;
};
