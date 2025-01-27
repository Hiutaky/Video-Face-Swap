import axios from "axios";
import { useState } from "react";

const GeneratePreview = ({ uid }) => {
    const [cropped, setCropped] = useState(false);
    const [imageGroups, setImageGroups] = useState([0]);
    const [uploadedImages, setUploadedImages] = useState({});
    const [uploadedGroups, setUploadedGroups] = useState(new Set());
    const [previewVideo, setPreviewVideo] = useState(false)
    const groupKeys = Object.keys(imageGroups);
    const currentGroup = groupKeys[0];


    const handleFileChange = (event, group) => {
        setUploadedImages({
          ...uploadedImages,
          [group]: event.target.files[0],
        });
      };

    const uploadImage = async (group) => {
        const formData = new FormData();
        formData.append("file", uploadedImages[group]);
    
        try {
          const response = await fetch(
            `http://localhost:8000/uploadnewfaces/${uid}/${group}`,
            {
              method: "POST",
              body: formData,
            }
          );
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          setUploadedGroups(new Set(uploadedGroups.add(group)));
          // fetchImages();
        } catch (error) {
          console.error("Could not upload image:", error);
        }
    };

    const previewCropFaces = async () => {
        const response = await axios.get(
            `http://localhost:8000/preview-crop-faces/${uid}`
        );
        console.log(response.status)
        if( response.status ) {
            setCropped(true);
            const images = await axios.get(`http://localhost:8000/get-preview-images/${uid}`)
            console.log(images.data);
            setImageGroups(images.data)

        }
    }

    const generatePreview = async (preview = false) => {
        const groupIdsArray = Array.from(uploadedGroups).map(Number);
        const response = await fetch(
            `http://localhost:8000/faceswap/${uid}`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(
                    { 
                        group_ids: groupIdsArray,
                        preview: preview
                    }
                )
            }
        )
        alert('Completed');
        setPreviewVideo(true);
    }


    return (
        <div className=" flex flex-col gap-3">
            <div className="flex flex-col gap-3">
                <h2 className="text-2xl">Generate Preview</h2>
                <button
                    onClick={previewCropFaces}
                >
                    Crop Preview Faces
                </button>
                {true && (
                    <div className="space-y-2">
                        <h3 className="font-semibold">Group {currentGroup}</h3>
                        <label
                            htmlFor="new-face"
                            className="block w-full px-4 py-2 bg-blue-600 text-white rounded cursor-pointer mb-2 transition-colors duration-300 hover:bg-blue-700"
                        >
                            Choose New Face
                        </label>
                        <input
                            id="new-face"
                            className="hidden"
                            type="file"
                            onChange={(event) => handleFileChange(event, currentGroup)}
                        />
                        <button
                            className="ml-2 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition duration-300"
                            onClick={() => uploadImage(currentGroup)}
                        >
                            Upload Image
                        </button>
                    </div>
                )}
                {Array.from(uploadedGroups).length ?
                <button
                    onClick={() => generatePreview(true)}
                >
                    Generate Preview
                </button> 
                : ''}
                {
                    previewVideo ?
                    <>
                    <video autoPlay controls>
                        <source src={`http://localhost:8000/preview_result_video/${uid}`} type="video/mp4" />
                    </video>
                    </>
                    : ''
                }
            </div>
        </div>
    )
}

export default GeneratePreview