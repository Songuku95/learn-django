import { API_ENDPOINT } from 'constants/common';
import CaseConverter from './caseConverter';

const defaultHeaders = {
  Accept: 'application/json',
  'Content-Type': 'application/json',
};

const request = async (url, method, body, customHeaders = {}) => {
  const endpoint = `${API_ENDPOINT}/api${url}`;

  const headers = {
    ...defaultHeaders,
    ...customHeaders,
  };

  const token = localStorage.getItem('token');
  if (token) {
    headers.Authorization = token;
  }

  let data = null;
  if (body) {
    if (headers['Content-Type'] === 'application/json') {
      data = JSON.stringify(CaseConverter.camelCaseToSnakeCase(body));
    } else {
      delete headers['Content-Type'];
      data = body;
    }
  } else {
    delete headers['Content-Type'];
  }

  const fetchOpts = {
    method,
    headers,
  };
  if (method !== 'HEAD' && method !== 'GET') {
    fetchOpts.body = data;
  }

  const response = await fetch(endpoint, fetchOpts);
  let json = await response.json();
  json = CaseConverter.snakeCaseToCamelCase(json);


  if (response.status < 200 || response.status >= 300) {
    if (json) {
      throw new Error(json);
    } else {
      throw new Error(response.statusText);
    }
  }

  return json;
};

export const get = endpoint => (
  request(endpoint, 'GET')
);

export const post = (endpoint, body, headers = {}) => (
  request(endpoint, 'POST', body, headers)
);

export const upload = (file) => {
  const formData = new FormData();
  formData.append('file', file, file.name);
  return post('/upload/image/', formData, {
    'Content-Type': 'multipart/form-data',
  });
};

export default {
  get,
  post,
  upload,
};
