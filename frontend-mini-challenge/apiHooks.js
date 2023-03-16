import useSWR from "swr";
import { fetchAndClean, urlJoin, GET, POST } from "./lib/apiHelpers";
import { REST_AUTH_BASE_URL, API_BASE_URL } from "./config";
import {
  getAuthToken,
  clearAuthToken,
  setAuthToken,
} from "./lib/authTokenStorage";
import { useState } from "react";

const delay = (ms) => new Promise((res) => setTimeout(res, ms));

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
    setAuthToken({ value: data.responseData.key, keep: true });
    mutate();
  }

  return {
    ...data,
    call,
    isLoading,
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

export function usePasswordReset() {
  const [data, setData] = useState({});
  const [isLoading, setLoading] = useState(false);
  const url = urlJoin({
    base: REST_AUTH_BASE_URL,
    tail: "password/reset/",
  });

  async function call({ email }) {
    setLoading(true);
    const data = await fetchAndClean({
      url,
      method: POST,
      data: { email },
    });
    // await delay(5000);
    setData(data);
    setLoading(false);
  }
  return {
    call,
    isLoading,
    ...data,
  };
}

export function useConfirmPasswordReset() {
  const [data, setData] = useState({});
  const [isLoading, setLoading] = useState(false);
  const url = urlJoin({
    base: REST_AUTH_BASE_URL,
    tail: "password/reset/confirm/",
  });

  async function call({ newPassword1, newPassword2, token, uid }) {
    setLoading(true);
    const data = await fetchAndClean({
      url,
      method: POST,
      data: { newPassword1, newPassword2, token, uid },
    });
    setData(data);
    setLoading(false);
  }
  return {
    call,
    isLoading,
    ...data,
  };
}

export function useChangePassword() {
  const [data, setData] = useState({});
  const [isLoading, setLoading] = useState(false);
  const url = urlJoin({
    base: REST_AUTH_BASE_URL,
    tail: "password/change/",
  });

  async function call({ newPassword1, newPassword2, oldPassword }) {
    const token = getAuthToken();
    setLoading(true);
    const data = await fetchAndClean({
      url,
      method: POST,
      data: { newPassword1, newPassword2, oldPassword },
      token,
    });
    setData(data);
    setLoading(false);
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
}

export function useGetUserActiveChallenges({ user }) {
  const url = `${API_BASE_URL}/api/challenge_registrations/?user=${user}`;
  const token = getAuthToken();

  const { data, error, isLoading, mutate } = useSWR(
    token && user
      ? {
          url,
          method: GET,
          token,
        }
      : null,
    fetchAndClean
  );
  return { error, isLoading, mutate, ...data };
}

export function useGetUserChallengeDetails({ registrationId }) {
  const url = `${API_BASE_URL}/api/challenge_registrations/${registrationId}/`;
  const token = getAuthToken();

  const { data, error, isLoading, mutate } = useSWR(
    registrationId
      ? {
          url,
          method: GET,
          token,
        }
      : null,
    fetchAndClean
  );
  return { error, isLoading, mutate, ...data };
}

export function useRegisterForChallenge() {
  const [data, setData] = useState({});
  const [isLoading, setLoading] = useState(false);
  const url = `${API_BASE_URL}/api/challenge_registrations/`;

  async function call({ user, curriculum }) {
    setLoading(true);
    const token = getAuthToken();
    const data = await fetchAndClean({
      token,
      url,
      method: POST,
      data: { user, curriculum },
    });
    setData(data);
    setLoading(false);
  }
  return {
    call,
    isLoading,
    ...data,
  };
}

export function useStartStep({ registrationId }) {
  const [data, setData] = useState({});
  const [isLoading, setLoading] = useState(false);
  const url = `${API_BASE_URL}/api/challenge_registrations/${registrationId}/start_step/`;

  async function call({ index }) {
    setLoading(true);
    const token = getAuthToken();
    const data = await fetchAndClean({
      token,
      url,
      method: POST,
      data: { index },
    });
    setData(data);
    setLoading(false);
  }
  return {
    call,
    isLoading,
    ...data,
  };
}

export function useFinishStep({ registrationId }) {
  const [data, setData] = useState({});
  const [isLoading, setLoading] = useState(false);
  const url = `${API_BASE_URL}/api/challenge_registrations/${registrationId}/finish_step/`;

  async function call({ index }) {
    setLoading(true);
    const token = getAuthToken();
    const data = await fetchAndClean({
      token,
      url,
      method: POST,
      data: { index },
    });
    setData(data);
    setLoading(false);
  }
  return {
    call,
    isLoading,
    ...data,
  };
}

export function useGetStepDetails({ registrationId, stepIndex }) {
  const url = `${API_BASE_URL}/api/challenge_registrations/${registrationId}/step_details/?index=${stepIndex}`;

  const token = getAuthToken();

  const { data, error, isLoading, mutate } = useSWR(
    token && registrationId && stepIndex !== undefined
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
}

export function useSubmitStepProjectLink({ registrationId }) {
  const [data, setData] = useState({});
  const [isLoading, setLoading] = useState(false);
  const url = `${API_BASE_URL}/api/challenge_registrations/${registrationId}/submit_link/`;

  async function call({ index, linkSubmission }) {
    setLoading(true);
    const token = getAuthToken();
    const data = await fetchAndClean({
      token,
      url,
      method: POST,
      data: { index, linkSubmission },
    });
    setData(data);
    setLoading(false);
  }
  return {
    call,
    isLoading,
    ...data,
  };
}
