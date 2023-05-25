export const loadScript = (src, onLoad) => {
  const script = document.createElement("script");
  script.src = src;
  script.async = true;
  document.body.appendChild(script);
  script.onload = onLoad;
};

export const googleAuthAvailable = () => {
  return Boolean(window.gapi);
};
