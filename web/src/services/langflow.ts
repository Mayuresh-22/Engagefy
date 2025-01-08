// Note: Replace **<YOUR_APPLICATION_TOKEN>** with your actual Application token

class LangflowClient {
  private langflowId: string;
  private flowId: string;
  private applicationToken: string;
  private baseURL: string = import.meta.env.VITE_LANGFLOW_API_BASE_URL;

  constructor(applicationToken: string, langflowId: string, flowId: string) {
    this.applicationToken = applicationToken;
    this.langflowId = langflowId;
    this.flowId = flowId;
  }

  async post(
    endpoint: string,
    body: Record<string, string | Record<string, string>>,
    headers: Record<string, string> = { "Content-Type": "application/json" }
  ) {
    headers["Authorization"] = `Bearer ${this.applicationToken}`;
    headers["Content-Type"] = "application/json";
    headers["Access-Control-Allow-Origin"] = "*";
    const url = `${this.baseURL}${endpoint}`;
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(body),
      });

      const responseMessage = await response.json();
      if (!response.ok) {
        throw new Error(
          `${response.status} ${response.statusText} - ${JSON.stringify(
            responseMessage
          )}`
        );
      }
      return responseMessage;
    } catch (error) {
      console.error("Request Error:", error.message);
      throw error;
    }
  }

  async initiateSession(
    flowId: string = this.flowId,
    langflowId: string = this.langflowId,
    inputType = "chat",
    outputType = "chat",
    stream = false,
    tweaks = {}
  ) {
    const endpoint = `/lf/${langflowId}/api/v1/run/${flowId}?stream=${stream}`;
    return this.post(endpoint, {
      input_type: inputType,
      output_type: outputType,
      tweaks: tweaks,
    });
  }

  async runFlow(
    flowIdOrName: string,
    langflowId: string,
    inputType = "chat",
    outputType = "chat",
    tweaks = {}
  ) {
    try {
      const initResponse = await this.initiateSession(
        flowIdOrName,
        langflowId,
        inputType,
        outputType,
        false,
        tweaks
      );
      console.log("Init Response:", initResponse);
      return initResponse;
    } catch (error) {
      console.error("Error running flow:", error);
      console.log("Error running flow:", error);
    }
  }
}

export default LangflowClient;