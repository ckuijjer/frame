import { useState } from 'react';

export const GenerateImage = () => {
  const [provider, setProvider] = useState('getimg');

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

  return (
    <>
      <div className="flex flex-col flex-1 items-center mb-4">
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
    </>
  );
};
