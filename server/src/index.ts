import { Hono } from "hono";
import LangflowClient from "./services/langflow";

type Bindings = {
  FLOW_ID_OR_NAME: string;
  LANGFLOW_APPLICATION_TOKEN: string;
  LANGFLOW_BASE_URL: string;
  LANGFLOW_ID: string;
  GROQ_API_KEY: string;
  GROQ_LLM: string;
};

const app = new Hono<{ Bindings: Bindings }>();

app.get("/", (c) => {
  return c.text("Hello Engagefy!");
});

app.get("/my-engagefy", async (c) => {
  const username = c.req.query("username");
  const postType = c.req.query("post_type");

  const SUPPORTED_POST_TYPES = ["carousel", "static_image", "reel"];

  if (!username || username === "") {
    return c.json({ status: "error", message: "Username is required" });
  }

  if (username.startsWith("@")) {
    return c.json({
      status: "error",
      message: "Username should not start with @",
    });
  }

  if (postType && postType === "") {
    return c.json({ status: "error", message: "Post type is required" });
  }

  if (postType && !SUPPORTED_POST_TYPES.includes(postType as string)) {
    return c.json({
      status: "error",
      message: `Post type ${postType} is not supported`,
    });
  }

  const baseURL = c.env.LANGFLOW_BASE_URL;
  const flowIdOrName = c.env.FLOW_ID_OR_NAME;
  const langflowId = c.env.LANGFLOW_ID;
  const applicationToken = c.env.LANGFLOW_APPLICATION_TOKEN;

  const langflowClient = new LangflowClient(
    baseURL,
    applicationToken,
    langflowId,
    flowIdOrName
  );

  try {
    const tweaks = {
      "TextInput-1TC5x": {
        input_value: username,
      },
      "TextInput-uB9VA": {
        input_value: postType || "",
      }
    };
    const response = await langflowClient.runFlow(
      flowIdOrName,
      langflowId,
      "chat",
      "chat",
      tweaks
    );
    if (response && response.outputs) {
      const flowOutputs = response.outputs[0];
      const firstComponentOutputs = flowOutputs.outputs[0];
      const output = firstComponentOutputs.outputs.message;
      const parsedOutput = JSON.parse(output.message.text as string);
      console.log("Parsed Output", parsedOutput);
      return c.json({ ...parsedOutput });
    }
  } catch (error) {
    if (error instanceof Error) {
      console.error("Main Error", error.message);
      return c.json({ status: "error", message: error.message });
    }
  }
  return c.json({
    status: "error",
    message:
      "An error occurred, make sure username/link is correct and account is public.",
  });
});

export default app;
