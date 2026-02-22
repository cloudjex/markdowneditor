import type { APIResponse } from '@/lib/types';


class RequestHandler {
  public idToken: string;
  public apiHost: string;

  constructor(idToken: string = "", apiHost: string = "") {
    this.idToken = idToken;
    this.apiHost = apiHost ? apiHost : import.meta.env.VITE_API_HOST;
  }

  async get<T>(url: string, queryParams: Record<string, unknown> = {}): Promise<APIResponse<T>> {
    return this.send("GET", url, queryParams);
  }

  async put<T>(url: string, body: Record<string, unknown> = {}): Promise<APIResponse<T>> {
    return this.send("PUT", url, body);
  }

  async post<T>(url: string, params: Record<string, unknown> = {}): Promise<APIResponse<T>> {
    return this.send("POST", url, params);
  }

  async delete<T>(url: string, queryParams: Record<string, unknown> = {}): Promise<APIResponse<T>> {
    return this.send("DELETE", url, queryParams);
  }

  private async send<T>(
    method: string,
    url: string,
    params: Record<string, unknown> = {},
  ): Promise<APIResponse<T>> {

    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      "Accept": "application/json",
    };

    if (this.idToken) {
      headers["Authorization"] = `Bearer ${this.idToken}`;
    }

    let apiUrl = `${this.apiHost}${url}`;

    console.group("API Request", `[${method}]: ${apiUrl}`);
    console.log("Headers", headers);

    let detail;
    if (method === "GET" || method === "DELETE") {
      detail = {
        method,
        headers,
      };
      apiUrl = `${apiUrl}?${new URLSearchParams(params as Record<string, string>)}`;
      console.log("Params", params);
    } else {
      detail = {
        method,
        headers,
        body: JSON.stringify(params),
      };
      console.log("Body", params);
    }

    const res = await fetch(apiUrl, detail);
    const result: APIResponse<T> = {
      status: res.status,
      headers: res.headers,
      body: await res.json(),
    };

    console.log("Response", result);
    console.groupEnd();
    return result;
  };
}

export default RequestHandler;
