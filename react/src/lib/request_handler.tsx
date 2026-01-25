import type { APIResponse } from '@/src/lib/types';


class RequestHandler {
  public id_token: string | null;

  constructor(id_token: string | null = null) {
    this.id_token = id_token;
  }

  async get<T>(url: string, params: Record<string, unknown> = {}): Promise<APIResponse<T>> {
    return this.send("GET", url, params);
  }

  async put<T>(url: string, params: Record<string, unknown> = {}): Promise<APIResponse<T>> {
    return this.send("PUT", url, params);
  }

  async post<T>(url: string, params: Record<string, unknown> = {}): Promise<APIResponse<T>> {
    return this.send("POST", url, params);
  }

  async delete<T>(url: string, params: Record<string, unknown> = {}): Promise<APIResponse<T>> {
    return this.send("DELETE", url, params);
  }

  private async send<T>(
    method: string,
    url: string,
    params: Record<string, unknown> = {},
  ): Promise<APIResponse<T>> {

    const headers = {
      "Content-Type": "application/json",
      "Accept": "application/json",
      "Authorization": this.id_token ? `Bearer ${this.id_token}` : ""
    };

    console.group("API Request", `[${method}]: ${url}`);
    console.log("Headers", headers);

    let detail;
    if (method === "GET" || method === "DELETE") {
      detail = {
        method,
        headers,
      };
      url = `${url}?${new URLSearchParams(params as Record<string, string>)}`;
      console.log("Params", params);
    } else {
      detail = {
        method,
        headers,
        body: JSON.stringify(params),
      };
      console.log("Body", params);
    }

    const res = await fetch(url, detail);
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