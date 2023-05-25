const AUTH_TOKEN = "_auth_token";

export const setAuthToken = ({ value, keep }) => {
  if (value) {
    if (keep) localStorage.setItem(AUTH_TOKEN, value);
    else sessionStorage.setItem(AUTH_TOKEN, value);
  } else clearAuthToken();
};

export const getAuthToken = () => {
    const token =
    sessionStorage.getItem(AUTH_TOKEN) || localStorage.getItem(AUTH_TOKEN);

  if (token !== "undefined") return token;
};

export const clearAuthToken = () => {
  sessionStorage.removeItem(AUTH_TOKEN);
  localStorage.removeItem(AUTH_TOKEN);
};
