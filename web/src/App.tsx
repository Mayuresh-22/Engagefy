"use client";

import { useState } from "react";
import langflow_logo from "./assets/langflow.png";
import datastax_logo from "./assets/datastax.png";
import { Input } from "./components/ui/input";
import { Button } from "./components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./components/ui/select";
import { Dot, Stars } from "lucide-react";

export default function SocialMediaAnalysis() {
  const [accountUsernameOrLink, setAccountUsernameOrLink] = useState("");
  const [postType, setPostType] = useState("");
  const [result, setResult] = useState<[string] | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleValidation = () => {
    if (!accountUsernameOrLink) {
      setError("Please enter social media account username/link");
      return false;
    }
    return true;
  };

  const handleClear = () => {
    setError("");
    setResult(null);
  };

  const handleDoMagic = async () => {
    setLoading(true);
    try {
      if (!handleValidation()) {
        setLoading(false);
        setError("Please enter valid details");
        return;
      }
      handleClear();
      const url = new URL(
        `${import.meta.env.VITE_APP_SERVER_URL}${import.meta.env.VITE_APP_MY_ENGAGEFY_ENDPOINT
        }`
      );
      url.searchParams.append("username", accountUsernameOrLink);
      postType && url.searchParams.append("post_type", postType);

      const response = await fetch(url.toString());
      const data = await response.json();
      console.log(data);
      if (data?.status === "success") {
        setResult(data?.insights);
      } else if (data?.status === "error") {
        setError(data?.message);
      }
    } catch (error) {
      console.error(error);
      setError("Something went wrong. Please try again later.");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen p-12 bg-mesh lato-regular relative">
      <div className="min-h-[calc(100vh-96px)] w-[calc(100vw-96px)] rounded-3xl backdrop-blur-md bg-white/30 shadow-lg border border-white/40 p-12 flex flex-col justify-center items-center overflow-y-auto relative pb-24">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Engagefy</h2>
        <h1 className="text-xl  text-gray-800 mb-6">
          Smarter Social Media Analysis with AI
        </h1>
        <div className="flex justify-center items-center align-middle mb-8 gap-x-3">
          <h2 className="text-base text-gray-900">Powered By</h2>
          <img src={datastax_logo} alt="Langflow Logo" className="w-30 h-16" />
          <img src={langflow_logo} alt="Langflow Logo" className="w-26 h-10" />
        </div>
        <div className="max-w-lg space-y-4 w-full">
          <Input
            type="text"
            placeholder="Enter Instagram account username/link"
            value={accountUsernameOrLink}
            onChange={(e) => setAccountUsernameOrLink(e.target.value)}
            className="w-full bg-white/70 border-0 placeholder:text-gray-600"
          />
          <div className="flex gap-3">
            <Select onValueChange={setPostType}>
              <SelectTrigger className="bg-white/60 border-0 flex-1">
                <SelectValue placeholder="Select post type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="carousel">Carousel</SelectItem>
                <SelectItem value="reel">Reels</SelectItem>
                <SelectItem value="static_image">Static Images</SelectItem>
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

          {(loading) ? (
            <div className="space-y-2 w-full backdrop-blur-md bg-white/60 p-4 rounded-lg">
              {/* Create shimmer blocks for each paragraph */}
              <div className="h-4 bg-gradient-to-r from-pink-400 to-violet-400 rounded w-5/6 animate-pulse"></div>
              <div className="h-4 bg-gradient-to-r from-pink-400 to-violet-400 rounded w-4/6 animate-pulse"></div>
              <div className="h-4 bg-gradient-to-r from-pink-400 to-violet-400 rounded w-5/6 animate-pulse"></div>
              <div className="h-4 bg-gradient-to-r from-pink-400 to-violet-400 rounded w-3/6 animate-pulse"></div>
              <div className="h-4 bg-gradient-to-r from-pink-400 to-violet-400 rounded w-4/6 animate-pulse"></div>
              <div className="h-4 bg-gradient-to-r from-pink-400 to-violet-400 rounded w-4/6 animate-pulse"></div>
            </div>
          ) : (result || error) && (
            <div className="w-full backdrop-blur-md bg-white/30 p-4 rounded-lg">
              {error && (
                <div className="w-full text-center font-medium text-red-500 text-sm">
                  {error}
                </div>
              )}
              {/* display insights by iterating over result */}
              <ul className="w-full space-y-2">
                {result?.map((insight, index) => (
                  <li
                    key={index}
                    className="w-full text-left font-semibold text-gray-800 text-sm"
                  >
                    <Dot className="w-8 h-8 inline-block" />
                    {insight}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
        <footer className="fixed bottom-0 left-0 right-0 p-4 text-center text-gray-800 text-sm bg-white/5 backdrop-blur-md">
          <p>
            by <span className="font-semibold">Mayuresh, Devang, Advait</span>
          </p>
        </footer>
      </div>
    </div>
  );
}
