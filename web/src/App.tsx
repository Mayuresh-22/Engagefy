'use client'

import { useState } from 'react'
import langflow_logo from "./assets/langflow.png"
import datastax_logo from "./assets/datastax.png"
import { Input } from "./components/ui/input"
import { Button } from "./components/ui/button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./components/ui/select"
import { Stars } from 'lucide-react'
import LangflowClient from './services/langflow'

export default function SocialMediaAnalysis() {
  const [accountLink, setAccountLink] = useState('')
  const [postType, setPostType] = useState('')

  const handleDoMagic = async () => {
    const flowIdOrName = import.meta.env.VITE_FLOW_ID_OR_NAME;
    const langflowId = import.meta.env.VITE_LANGFLOW_ID;
    const applicationToken = import.meta.env.VITE_LANGFLOW_APPLICATION_TOKEN;
    const langflowClient = new LangflowClient(
      applicationToken,
      langflowId,
      flowIdOrName
    );
  
    try {
      const tweaks = {
        "TextInput-1TC5x": {
          input_value: accountLink,
        },
        "TextInput-uB9VA": {
          input_value: postType,
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
  
        console.log("Final Output:", output.message.text);
      }
    } catch (error) {
      console.error("Main Error", error.message);
    }
  }

  return (
    <div className="min-h-screen p-12 bg-mesh lato-regular">
      <div className="h-[calc(100vh-96px)] w-[calc(100vw-96px)] rounded-3xl backdrop-blur-md bg-white/30 shadow-lg border border-white/40 p-12 flex flex-col justify-center items-center">
        <h1 className="text-3xl  text-gray-800 mb-6">Smarter Social Media Analysis with AI</h1>
        <div className="flex justify-center items-center align-middle mb-8 gap-x-3">
          <h2 className="text-base text-gray-900">Powered By</h2>
          <img src={datastax_logo} alt="Langflow Logo" className="w-30 h-16" />
          <img src={langflow_logo} alt="Langflow Logo" className="w-26 h-10" />
        </div>
        <div className="max-w-md space-y-4 w-full">
          <Input
            type="text"
            placeholder="Enter social media account username/link"
            value={accountLink}
            onChange={(e) => setAccountLink(e.target.value)}
            className="w-full bg-white/70 border-0 placeholder:text-gray-600"
          />
          <div className="flex gap-3">
            <Select onValueChange={setPostType}>
              <SelectTrigger className="bg-white/60 border-0 flex-1">
                <SelectValue placeholder="Select post type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="carousel">Carousel</SelectItem>
                <SelectItem value="reels">Reels</SelectItem>
                <SelectItem value="static">Static Images</SelectItem>
              </SelectContent>
            </Select>

            <Button
              className="bg-gradient-to-r from-pink-500 to-violet-600 text-white hover:opacity-90 px-6 hover:from-pink-600 hover:to-violet-700 hover:scale-105 transition-all ease-in-out duration-300"
              onClick={handleDoMagic}
            >
              Do Magic
              <Stars className="w-4 h-4 ml-2" />
            </Button>
          </div>
        </div>
        <div className="bottom-5 absolute w-full text-center text-gray-600 text-sm">
          <span>by Mayuresh, Devang, Advait</span>
        </div>
      </div>
    </div>
  )
}

