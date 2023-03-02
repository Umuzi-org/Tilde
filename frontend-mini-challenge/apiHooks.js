import useSWR from "swr";
import { fetchAndClean, urlJoin, GET, POST } from "./lib/apiHelpers";
import { REST_AUTH_BASE_URL, API_BASE_URL } from "./config";
import {
  getAuthToken,
  clearAuthToken,
  setAuthToken,
} from "./lib/authTokenStorage";
import { useState } from "react";

// const delay = (ms) => new Promise((res) => setTimeout(res, ms));

export function useLogin() {
  const [data, setData] = useState({});
  const [isLoading, setLoading] = useState(false);
  const { mutate } = useWhoAmI();

  const url = urlJoin({
    base: REST_AUTH_BASE_URL,
    tail: "login/",
  });

  async function call({ email, password }) {
    setLoading(true);
    const data = await fetchAndClean({
      url,
      method: POST,
      data: {
        email,
        password,
      },
    });
    setData(data);
    setLoading(false);
    setAuthToken({ value: data.jsonData.key, keep: true });
    mutate();
  }

  return {
    call,
    isLoading,
    ...data,
  };
}

export function useLogout() {
  const { mutate } = useWhoAmI();
  const [data, setData] = useState({});
  const [isLoading, setLoading] = useState(false);

  const url = urlJoin({
    base: REST_AUTH_BASE_URL,
    tail: "logout/",
  });

  async function call() {
    setLoading(true);
    const token = getAuthToken();
    const data = await fetchAndClean({
      url,
      method: POST,
      token,
    });
    setData(data);
    setLoading(false);
    clearAuthToken();
    mutate();
  }
  return {
    call,
    isLoading,
    ...data,
  };
}

export function useWhoAmI() {
  const url = `${API_BASE_URL}/api/who_am_i/`;

  const token = getAuthToken();

  const { data, error, isLoading, mutate } = useSWR(
    token
      ? {
          url,
          method: GET,
          token,
        }
      : null,
    fetchAndClean
  );

  if (data && data.status === 401) {
    // unauthorized
    clearAuthToken();
  }

  return { error, isLoading, mutate, ...data };

  // async function whoAmI() {
  //     const { response, responseData } = await fetchAndClean({ url });
  //     if (responseData.detail === "Invalid token.") clearAuthToken();
  //     return { response, responseData };
  //   }
}

// export function useLogout() {
//   // const { data: user } = useSWR(url, token}, )
// }

// const AUTH_TOKEN = '_auth_token';

// export const getAuthToken = () => {
//   const token =
//     sessionStorage.getItem(AUTH_TOKEN) || localStorage.getItem(AUTH_TOKEN);

//   if (token !== 'undefined') return token;
// };

// export const clearAuthToken = () => {
//   sessionStorage.removeItem(AUTH_TOKEN);
//   localStorage.removeItem(AUTH_TOKEN);
// };

// export const setAuthToken = ({ value, keep }) => {
//   if (value) {
//     if (keep) localStorage.setItem(AUTH_TOKEN, value);
//     else sessionStorage.setItem(AUTH_TOKEN, value);
//   } else clearAuthToken();
// };
