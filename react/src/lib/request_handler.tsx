import type { APIResponse } from '@/src/lib/types';


class RequestHandler {
  public id_token: string;
  public api_host: string;

  constructor(id_token: string = "", api_host: string = "") {
    this.id_token = id_token;
    this.api_host = api_host ? api_host : import.meta.env.VITE_API_HOST;
  }

  async get<T>(url: string, query_params: Record<string, unknown> = {}): Promise<APIResponse<T>> {
    return this.send("GET", url, query_params);
  }

  async put<T>(url: string, body: Record<string, unknown> = {}): Promise<APIResponse<T>> {
    return this.send("PUT", url, body);
  }

  async post<T>(url: string, params: Record<string, unknown> = {}): Promise<APIResponse<T>> {
    return this.send("POST", url, params);
  }

  async delete<T>(url: string, query_params: Record<string, unknown> = {}): Promise<APIResponse<T>> {
    return this.send("DELETE", url, query_params);
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

    if (this.id_token) {
      headers["Authorization"] = `Bearer ${this.id_token}`;
    }

    let api_url = `${this.api_host}${url}`;

    console.group("API Request", `[${method}]: ${api_url}`);
    console.log("Headers", headers);

    let detail;
    if (method === "GET" || method === "DELETE") {
      detail = {
        method,
        headers,
      };
      api_url = `${api_url}?${new URLSearchParams(params as Record<string, string>)}`;
      console.log("Params", params);
    } else {
      detail = {
        method,
        headers,
        body: JSON.stringify(params),
      };
      console.log("Body", params);
    }

    const res = await fetch(api_url, detail);
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
