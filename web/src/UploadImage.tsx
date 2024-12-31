import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import Cropper from 'react-easy-crop';
import axios from 'axios';
import { IMAGE_HEIGHT, IMAGE_WIDTH } from './constants';

const getCroppedImage = async ({ imageSrc, croppedAreaPixels, rotation }) => {
  console.log({ imageSrc, croppedAreaPixels, rotation });

  const image = await createImage(imageSrc);
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');

  canvas.width = croppedAreaPixels.width;
  canvas.height = croppedAreaPixels.height;

  // ctx.translate(canvas.width / 2, canvas.height / 2); // Translate context to center of canvas
  // ctx.rotate((90 * Math.PI) / 180); // Rotate context
  // ctx.translate(-canvas.width / 2, -canvas.height / 2); // Translate back

  // Draw the cropped image onto the canvas
  ctx.drawImage(
    image,
    croppedAreaPixels.x,
    croppedAreaPixels.y,
    croppedAreaPixels.width,
    croppedAreaPixels.height,
    0,
    0,
    croppedAreaPixels.width,
    croppedAreaPixels.height,
  );

  // Convert canvas content to a Blob or File
  return new Promise((resolve) => {
    canvas.toBlob(
      (blob) => {
        const file = new File([blob], 'cropped-image.jpg', {
          type: 'image/jpeg',
        });
        resolve(file);
      },
      'image/jpeg',
      1, // Quality factor (1 = best quality)
    );
  });
};

function createImage(url) {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.crossOrigin = 'anonymous'; // For CORS issues
    image.onload = () => resolve(image);
    image.onerror = (error) => reject(error);
    image.src = url;
  });
}

export const UploadImage = () => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [imageSrc, setImageSrc] = useState(null);

  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [rotation, setRotation] = useState(0);
  const [croppedAreaPixels, setCroppedAreaPixels] = useState(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setIsUploading(true); // Set upload in progress

    const file = acceptedFiles[0];
    const reader = new FileReader();
    reader.onload = () => {
      setImageSrc(reader.result);

      setUploadProgress(0); // Reset progress after upload
      setIsUploading(false); // Reset upload state
    };
    reader.readAsDataURL(file);
    reader.onprogress = (event) => {
      if (event.lengthComputable) {
        const progress = Math.round((event.loaded * 100) / event.total);
        setUploadProgress(progress);
      }
    };
  }, []);

  const onUpload = async () => {
    const croppedImage = await getCroppedImage({
      imageSrc,
      croppedAreaPixels,
      rotation,
    });

    // const blobUrl = URL.createObjectURL(croppedImage);

    // // Automatically trigger download
    // const link = document.createElement('a');
    // link.href = blobUrl;
    // link.download = 'cropped-image.jpg';
    // document.body.appendChild(link);
    // link.click();
    // document.body.removeChild(link);

    setIsUploading(true); // Set upload in progress
    const formData = new FormData();
    formData.append('file', croppedImage);

    console.log({ formData });

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

  const onCropComplete = useCallback((_, croppedAreaPixels) => {
    setCroppedAreaPixels(croppedAreaPixels);
  }, []);

  const rotate90Clockwise = () => {
    setRotation((rotation + 90) % 360);
  };

  const rotate90CounterClockwise = () => {
    setRotation((rotation - 90 + 360) % 360);
  };

  const resetImage = () => {
    setCrop({ x: 0, y: 0 });
    setZoom(1);
    setRotation(0);
    setCroppedAreaPixels(null);
    setImageSrc(null);
  };

  function createImage(url) {
    return new Promise((resolve, reject) => {
      const image = new Image();
      image.crossOrigin = 'anonymous'; // For CORS issues
      image.onload = () => resolve(image);
      image.onerror = (error) => reject(error);
      image.src = url;
    });
  }

  return (
    <>
      {!imageSrc && (
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
      )}
      {imageSrc && (
        <div className=" flex-1 flex flex-col items-stretch justify-stretch">
          <div className="flex-1 mb-4 relative">
            <Cropper
              image={imageSrc}
              crop={crop}
              zoom={zoom}
              rotation={rotation}
              aspect={IMAGE_WIDTH / IMAGE_HEIGHT} // Square aspect ratio
              onCropChange={setCrop}
              onZoomChange={setZoom}
              objectFit="cover"
              onCropComplete={onCropComplete}
            />
          </div>
          <div className="flex">
            <button
              onClick={resetImage}
              className="px-4 py-2 bg-gray-200 rounded mr-2"
            >
              ❌
            </button>
            {/* <button
              onClick={rotate90CounterClockwise}
              className="px-4 py-2 bg-gray-200 rounded mr-2"
            >
              ↪️
            </button>
            <button
              onClick={rotate90Clockwise}
              className="px-4 py-2 bg-gray-200 rounded mr-4"
            >
              ↩️
            </button> */}
            <button
              onClick={onUpload}
              className="px-4 py-2 bg-blue-500 text-white rounded flex-1"
            >
              Upload
            </button>
          </div>
        </div>
      )}
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
