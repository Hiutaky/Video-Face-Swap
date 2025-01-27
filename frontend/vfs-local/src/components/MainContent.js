import React, { useRef, useState } from "react";
import axios from "axios";
import ImageDisplay from "./ImageDisplay";
import GeneratePreview from "./GeneratePreview";

const MainContent = () => {
  const fileInput = useRef(null);
  const [isSuccessUpload, setIsSuccessUpload] = useState(false);
  const [uid, setUid] = useState("641e1a0a-fb9b-41ce-b7d8-60a2d0faec71");
  const [videoPreview, setVideoPreview] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileSelect = () => {
    const file = fileInput.current.files[0];
    if (file) {
      setVideoPreview(URL.createObjectURL(file));
    }
  };

  const handleUpload = async () => {
    setIsLoading(true);
  
    const formData = new FormData();
    formData.append('file', fileInput.current.files[0]);
    try {
      const response = await axios.post('http://localhost:8000/uploadvideo/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert(response.data.message);
      setUid(response.data.uid);
      setIsSuccessUpload(true);
    } catch (error) {
      alert('Failed to upload video. ' + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="text-black bg-gray-400 p-5 min-h-[calc(100vh-100px)]">
      <div className=" text-black font-bold text-4xl">Video Face Swap</div>
      <div className="grid grid-cols-2 gap-3">

        <div className="bg-gray-400 border-2 border-dashed border-gray-300 rounded p-5 my-5">
          <div className="flex justify-between items-start gap-4 w-full">
            {videoPreview && (
              <video
                className="w-full"
                controls
                src={videoPreview}
              ></video>
            )}
          </div>
          <div className="text-center mt-4 flex flex-col items-center w-full">
              <div className="w-3/4 md:w-1/2">
                <label
                  htmlFor="video-file"
                  className="block w-full px-4 py-2 bg-blue-600 text-white rounded cursor-pointer mb-2 transition-colors duration-300 hover:bg-blue-700"
                >
                  Choose Video File
                </label>
                <input
                  id="video-file"
                  type="file"
                  ref={fileInput}
                  className="hidden"
                  accept="video/*"
                  onChange={handleFileSelect}
                />
              </div>
            <button
              className="px-5 py-2.5 bg-green-500 text-white rounded cursor-pointer transition-colors duration-300 hover:bg-green-600"
              onClick={handleUpload}
              disabled={isLoading}
            >
              {isLoading ? "Uploading..." : "Upload"}
            </button>
          </div>
        </div>
        <div className="">
          {true && 
            <>
              <GeneratePreview uid={uid} />
            </>
          }
          <div className="border-t mt-5"></div>
          <h2 className="text-2xl">Generate Complete</h2>
          {
            true &&
            <>
              <ImageDisplay uid={uid} />
            </>
          }
        </div>
      </div>
    </div>
  );
};

export default MainContent;
