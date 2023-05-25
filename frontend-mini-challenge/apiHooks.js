import useSWR from "swr";
import { fetchAndClean, urlJoin, GET, POST } from "./lib/apiHelpers";
import { REST_AUTH_BASE_URL, API_BASE_URL } from "./config";
import { STATUS_UNDER_REVIEW } from "./constants";
import {
  getAuthToken,
  clearAuthToken,
  setAuthToken,
} from "./lib/authTokenStorage";
import { useState } from "react";
import { useCookies } from "react-cookie";

export const delay = (ms) => new Promise((res) => setTimeout(res, ms));

export const TOKEN_COOKIE = "token";

export function useLogin() {
  const [data, setData] = useState({});
  const [isLoading, setLoading] = useState(false);
  const [cookie, setCookie] = useCookies([TOKEN_COOKIE]);

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

    setCookie(TOKEN_COOKIE, data.responseData.key, {
      path: "/",
      // maxAge: 3600, // Expires after 1hr
      sameSite: true,
    });

    mutate();
  }

  return {
    ...data,
    call,
    isLoading,
  };
}

export function useLogout() {
  const [data, setData] = useState({});
  const [isLoading, setLoading] = useState(false);
  const [cookie, setCookie, removeCookie] = useCookies([TOKEN_COOKIE]);

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
    removeCookie(TOKEN_COOKIE, {
      path: "/",
    });
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

  async function call({ email, origin }) {
    setLoading(true);
    const data = await fetchAndClean({
      url,
      method: POST,
      data: { email, origin },
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

export async function serverSideWhoAmI({ req }) {
  const token = req.cookies[TOKEN_COOKIE];
  const url = `${API_BASE_URL}/api/zmc/who_am_i/`;
  const data = await fetchAndClean({
    token,
    url,
    method: GET,
  });

  return data;
}

export function useWhoAmI() {
  const [cookie, setCookie] = useCookies([TOKEN_COOKIE]);

  const url = `${API_BASE_URL}/api/zmc/who_am_i/`;

  const token = getAuthToken();

  // sometimes cookie and token dont match. Weird edge case for multiple users.
  // Probably should be fixed in the future

  setCookie(TOKEN_COOKIE, token, {
    path: "/",
    // maxAge: 3600, // Expires after 1hr
    sameSite: true,
  });

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

export async function serverSideGetUserChallengeDetails({
  registrationId,
  req,
}) {
  const token = req.cookies[TOKEN_COOKIE];

  const url = `${API_BASE_URL}/api/challenge_registrations/${registrationId}/`;

  const data = await fetchAndClean({
    token,
    url,
    method: GET,
  });

  return data;
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

export async function serverSideStartStep({ stepIndex, registrationId, req }) {
  const token = req.cookies[TOKEN_COOKIE];
  const url = `${API_BASE_URL}/api/challenge_registrations/${registrationId}/start_step/`;

  const data = await fetchAndClean({
    token,
    url,
    method: POST,
    data: { index: stepIndex },
  });

  return data;
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
  const getUserChallengeDetails = useGetUserChallengeDetails({
    registrationId,
  }); // TODO: Do we need this? Maybe just remove it..
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
    getUserChallengeDetails.mutate();
    setData(data);
    setLoading(false);
  }
  return {
    call,
    isLoading,
    ...data,
  };
}

export async function serverSideGetStepDetails({
  registrationId,
  stepIndex,
  req,
}) {
  const token = req.cookies[TOKEN_COOKIE];
  const url = `${API_BASE_URL}/api/challenge_registrations/${registrationId}/step_details/?index=${stepIndex}`;

  const data = await fetchAndClean({
    token,
    url,
    method: GET,
  });

  return data;
}

export function useGetStepDetails({ registrationId, stepIndex }) {
  const url = `${API_BASE_URL}/api/challenge_registrations/${registrationId}/step_details/?index=${stepIndex}`;

  const token = getAuthToken();

  const { data, error, isLoading, mutate } = useSWR(
    token && registrationId && stepIndex !== undefined
      ? // token && currentStatus === STATUS_UNDER_REVIEW
        {
          url,
          method: GET,
          token,
        }
      : null,
    fetchAndClean
    // { refreshInterval: 20000 }
  );

  if (data && data.status === 401) {
    // unauthorized
    clearAuthToken();
  }

  return { error, isLoading, mutate, ...data };
}

export function useRefreshReviewStepDetails({
  registrationId,
  stepIndex,
  currentStepStatus,
}) {
  const url = `${API_BASE_URL}/api/challenge_registrations/${registrationId}/step_details/?index=${stepIndex}`;

  const token = getAuthToken();

  const { data, error, isLoading, mutate } = useSWR(
    token &&
      registrationId &&
      stepIndex !== undefined &&
      currentStepStatus === STATUS_UNDER_REVIEW
      ? // token && currentStatus === STATUS_UNDER_REVIEW
        {
          url,
          method: GET,
          token,
        }
      : null,
    fetchAndClean,
    { refreshInterval: 5000 }
  );

  if (data && data.status === 401) {
    // unauthorized
    clearAuthToken();
  }

  return { error, isLoading, mutate, ...data };
}

export function useSubmitStepProjectLink({ stepIndex, registrationId }) {
  const [data, setData] = useState({});
  const [isLoading, setLoading] = useState(false);
  const url = `${API_BASE_URL}/api/challenge_registrations/${registrationId}/submit_link/`;

  async function call({ linkSubmission }) {
    setLoading(true);
    const token = getAuthToken();

    const fetcher = fetchAndClean({
      token,
      url,
      method: POST,
      data: { index: stepIndex, linkSubmission },
    });
    const data = await fetcher;
    setData(data);
    setLoading(false);
  }
  return {
    call,
    isLoading,
    ...data,
  };
}
