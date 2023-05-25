/*
NOTE: This authentication strategy is not super modern. It would be better to use a third party auth provider. That said, it probably doesn't matter very much since these credentials don't let the user do very much at all.

Articles worth reading: 
- https://levelup.gitconnected.com/secure-frontend-authorization-67ae11953723
- https://nextjs.org/docs/authentication
*/

const AUTH_TOKEN = "_auth_token";

export const storageAvailable = () => {
  try {
    sessionStorage;
    localStorage;
    return true;
  } catch {
    return false;
  }
};

export const getAuthToken = () => {
  if (!storageAvailable()) return;
  const token =
    sessionStorage.getItem(AUTH_TOKEN) || localStorage.getItem(AUTH_TOKEN);

  if (token !== "undefined") return token;
};

export const clearAuthToken = () => {
  sessionStorage.removeItem(AUTH_TOKEN);
  localStorage.removeItem(AUTH_TOKEN);
};

export const setAuthToken = ({ value, keep }) => {
  if (value) {
    if (keep) localStorage.setItem(AUTH_TOKEN, value);
    else sessionStorage.setItem(AUTH_TOKEN, value);
  } else clearAuthToken();
};
