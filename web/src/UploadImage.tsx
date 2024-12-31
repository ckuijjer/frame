import { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

export const UploadImage = () => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);

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

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    disabled: isUploading,
  });

  return (
    <>
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
    </>
  );
};
