import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import Cropper, { Area } from 'react-easy-crop';
import axios from 'axios';
import { IMAGE_HEIGHT, IMAGE_WIDTH } from './constants';

// Neither Chrome nor Firefox can decode HEIC/HEIF (iPhones' default photo
// format) into an <img>/canvas at all, so the crop preview and canvas-based
// cropping below would just silently fail on one - converted to JPEG here
// first. file.type is unreliable for HEIC (often "" depending on OS/browser),
// so the extension is checked too.
const isHeic = (file: File) =>
  file.type === 'image/heic' ||
  file.type === 'image/heif' ||
  /\.(heic|heif)$/i.test(file.name);

type GetCroppedImageArgs = {
  imageSrc: string;
  croppedAreaPixels: Area;
  rotation: number;
};

const getCroppedImage = async ({
  imageSrc,
  croppedAreaPixels,
  rotation,
}: GetCroppedImageArgs): Promise<File> => {
  console.log({ imageSrc, croppedAreaPixels, rotation });

  const image = await createImage(imageSrc);
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  if (!ctx) {
    throw new Error('Could not get canvas 2D context');
  }

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
  return new Promise<File>((resolve, reject) => {
    canvas.toBlob(
      (blob) => {
        if (!blob) {
          reject(new Error('Canvas toBlob() returned null'));
          return;
        }
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

function createImage(url: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.crossOrigin = 'anonymous'; // For CORS issues
    image.onload = () => resolve(image);
    image.onerror = (error) => reject(error);
    image.src = url;
  });
}

const readFileAsDataURL = (
  file: Blob,
  onProgress: (percent: number) => void,
): Promise<string> =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    // readAsDataURL below always yields a string result, never ArrayBuffer
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = () => reject(reader.error);
    reader.onprogress = (event) => {
      if (event.lengthComputable) {
        onProgress(Math.round((event.loaded * 100) / event.total));
      }
    };
    reader.readAsDataURL(file);
  });

export const UploadImage = () => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [isConverting, setIsConverting] = useState(false);
  const [imageSrc, setImageSrc] = useState<string | null>(null);

  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [rotation, setRotation] = useState(0);
  const [croppedAreaPixels, setCroppedAreaPixels] = useState<Area | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];

    (async () => {
      let fileToRead: File | Blob = file;

      if (isHeic(file)) {
        setIsConverting(true);
        try {
          // Dynamically imported: heic2any bundles a WASM HEIC decoder
          // (~1.3MB) that most visitors, who never drop a HEIC file, would
          // otherwise download on every page load for nothing.
          const { default: heic2any } = await import('heic2any');
          const converted = await heic2any({
            blob: file,
            toType: 'image/jpeg',
            quality: 0.92,
          });
          fileToRead = Array.isArray(converted) ? converted[0] : converted;
        } catch (error) {
          console.error('Error converting HEIC image:', error);
          setIsConverting(false);
          return;
        }
        setIsConverting(false);
      }

      setIsUploading(true); // Set upload in progress
      try {
        setImageSrc(await readFileAsDataURL(fileToRead, setUploadProgress));
      } catch (error) {
        console.error('Error reading image:', error);
      } finally {
        setUploadProgress(0); // Reset progress after upload
        setIsUploading(false); // Reset upload state
      }
    })();
  }, []);

  const onUpload = async () => {
    if (!imageSrc || !croppedAreaPixels) {
      return;
    }

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

  const isBusy = isUploading || isConverting;

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    disabled: isBusy,
  });

  const onCropComplete = useCallback((_croppedArea: Area, croppedAreaPixels: Area) => {
    setCroppedAreaPixels(croppedAreaPixels);
  }, []);

  const resetImage = () => {
    setCrop({ x: 0, y: 0 });
    setZoom(1);
    setRotation(0);
    setCroppedAreaPixels(null);
    setImageSrc(null);
  };

  return (
    <>
      {!imageSrc && (
        <div
          {...getRootProps()}
          className={`border-2 border-dashed p-8 rounded cursor-pointer flex-1 flex items-center justify-center ${
            isBusy ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          <input {...getInputProps()} disabled={isBusy} />
          {isDragActive ? (
            <p>Drop the image here...</p>
          ) : (
            <p>
              {isConverting
                ? 'Converting HEIC image...'
                : isUploading
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
