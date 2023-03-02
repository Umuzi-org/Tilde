export const GET = "GET";
export const POST = "POST";

export function getNextPageNumberFromUrl({ url }) {
  if (url === null) return null;
  const urlInstance = new URL(url);
  const page = urlInstance.searchParams.get("page");
  return page;
}

function replaceAll(str, find, replace) {
  return str.replace(new RegExp(find, "g"), replace);
}

export const _toCamel = (s) => {
  let arr = s.split("");
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] === "_") {
      arr[i + 1] = arr[i + 1].replace(arr[i + 1], arr[i + 1].toUpperCase());
    }
  }
  arr = arr.join("");
  return replaceAll(arr, "_", "");
};

const _isArray = function (a) {
  return Array.isArray(a);
};

const _isObject = function (o) {
  return o === Object(o) && !_isArray(o) && typeof o !== "function";
};

export const fromSnakeToCamel = function (o) {
  if (_isObject(o)) {
    const n = {};

    Object.keys(o).forEach((k) => {
      n[_toCamel(k)] = fromSnakeToCamel(o[k]);
    });

    return n;
  } else if (_isArray(o)) {
    return o.map((i) => {
      return fromSnakeToCamel(i);
    });
  }

  return o;
};

const camelStringToSnake = function (s) {
  return s
    .replace(/(?:^|\.?)([A-Z])/g, function (x, y) {
      return "_" + y.toLowerCase();
    })
    .replace(/^_/, "");
};

export async function fetchAndClean({ url, method, data, token }) {
  let headers = {
    "Content-Type": "application/json",
  };
  if (token) headers["Authorization"] = `Token ${token}`;

  let params = {
    method,
    headers,
  };

  if (data) {
    let snakeData = {};
    Object.keys(data).forEach((key) => {
      snakeData[camelStringToSnake(key)] = data[key];
    });
    params["body"] = JSON.stringify(snakeData);
  }

  const response = await fetch(url, params);

  const responseData = await response.json();

  return Promise.resolve({
    response,
    status: response.status,
    statusText: response.statusText,
    responseData: fromSnakeToCamel(responseData),
    requestData: data,
  });
}

export function urlJoin({ base, tail }) {
  if (base.endsWith("/")) return `${base}${tail}`;
  return `${base}/${tail}`;
}

export function objectToGetQueryString(obj) {
  var str = "";
  for (var key in obj) {
    if (str !== "") {
      str += "&";
    }
    str += key + "=" + encodeURIComponent(obj[key]);
  }
  return str;
}
