import { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

function App() {
  const [provider, setProvider] = useState('getimg');
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);

  const [top, setTop] = useState(0);
  const [left, setLeft] = useState(0);
  const [bottom, setBottom] = useState(480);
  const [right, setRight] = useState(800);

  const generateImage = async () => {
    try {
      const response = await fetch('/api/render', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ provider }),
      });
      const result = await response.json();
      console.log(result.message);
    } catch (error) {
      console.error('Error generating image:', error);
    }
  };

  const onDrop = async (acceptedFiles: File[]) => {
    setIsUploading(true); // Set upload in progress
    const formData = new FormData();
    formData.append('file', acceptedFiles[0]);

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round(
            progressEvent.total
              ? (progressEvent.loaded * 100) / progressEvent.total
              : 0,
          );
          setUploadProgress(progress);
        },
      });
      console.log(response.data.message);
    } catch (error) {
      console.error('Error uploading image:', error);
    } finally {
      setUploadProgress(0); // Reset progress after upload
      setIsUploading(false); // Reset upload state
    }
  };

  const renderOverscanGrid = async () => {
    event?.preventDefault(); // Prevent default form behavior

    try {
      const response = await fetch('/api/render_overscan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ top, left, bottom, right }),
      });
      const result = await response.json();
      console.log(result.message);
    } catch (error) {
      console.error('Error generating image:', error);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    disabled: isUploading,
  });

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-2">Frame</h1>
      <h2 className="text-xl mb-6">
        Fetches news headlines, generates AI-based images from summaries, and
        displays them on an Inky e-ink display
      </h2>

      {/* <div className="flex items-center justify-center space-x-8"> */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
        <div className="bg-white p-8 rounded shadow-md  text-center min-h-[200px]">
          <div className="flex flex-col items-center mb-4">
            <label className="mb-2">
              <input
                type="radio"
                value="openai"
                checked={provider === 'openai'}
                onChange={() => setProvider('openai')}
                className="mr-2"
              />
              OpenAI
            </label>
            <label>
              <input
                type="radio"
                value="getimg"
                checked={provider === 'getimg'}
                onChange={() => setProvider('getimg')}
                className="mr-2"
              />
              Stable Diffusion XL
            </label>
          </div>
          <button
            onClick={generateImage}
            className="px-4 py-2 bg-blue-500 text-white rounded w-full"
          >
            Generate Image
          </button>
        </div>

        <div className="bg-white p-8 rounded shadow-md  text-center min-h-[200px] flex flex-col">
          <div
            {...getRootProps()}
            className={`border-2 border-dashed p-8 rounded cursor-pointer flex-1 flex items-center justify-center ${
              isUploading ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            <input {...getInputProps()} disabled={isUploading} />
            {isDragActive ? (
              <p>Drop the image here...</p>
            ) : (
              <p>
                {isUploading
                  ? 'Uploading...'
                  : 'Drag and drop an image here, or click to select'}
              </p>
            )}
          </div>
          {uploadProgress > 0 && (
            <div className="w-full bg-gray-200 rounded-full h-4 mt-4">
              <div
                className="bg-blue-500 h-4 rounded-full"
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
          )}
        </div>

        <div className="bg-white p-8 rounded shadow-md  text-center min-h-[200px]">
          <form onSubmit={renderOverscanGrid} className="space-y-4 ">
            <div className="grid grid-cols-1 gap-4">
              <input
                type="number"
                placeholder="Top"
                value={top}
                onChange={(e) => setTop(Number(e.target.value))}
                className="p-2 border border-gray-300 rounded"
              />
              <input
                type="number"
                placeholder="Right"
                value={right}
                onChange={(e) => setRight(Number(e.target.value))}
                className="p-2 border border-gray-300 rounded"
              />
              <input
                type="number"
                placeholder="Bottom"
                value={bottom}
                onChange={(e) => setBottom(Number(e.target.value))}
                className="p-2 border border-gray-300 rounded"
              />
              <input
                type="number"
                placeholder="Left"
                value={left}
                onChange={(e) => setLeft(Number(e.target.value))}
                className="p-2 border border-gray-300 rounded"
              />
            </div>
            <button className="px-4 py-2 bg-blue-500 text-white rounded mt-4 w-full">
              Render Overscan Frame
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;
