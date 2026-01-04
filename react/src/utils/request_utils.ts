import type { APIResponse } from '../types/types';

export default {
  requests
};

async function requests(
  url: string,
  method: string,
  headers: Record<string, string>,
  params: unknown
): Promise<APIResponse> {
  if (!headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  console.group("API Request");
  console.log(`[${method}]: ${url}`);
  console.log({ url, method, headers, params });

  let detail;
  if (method === "GET" || method === "DELETE") {
    detail = {
      method,
      headers,
    };
    url = `${url}?${new URLSearchParams(params as Record<string, string>)}`;
  } else {
    detail = {
      method,
      headers,
      body: JSON.stringify(params),
    };
  }

  const res = await fetch(url, detail);
  const result: APIResponse = {
    status: res.status,
    headers: res.headers,
    body: await res.json(),
  };

  console.log(result);
  console.groupEnd();
  return result;
};
