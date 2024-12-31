import { useState } from 'react';
import { IMAGE_WIDTH, IMAGE_HEIGHT } from './constants';

export const OverscanImage = () => {
  const [top, setTop] = useState(0);
  const [left, setLeft] = useState(0);
  const [bottom, setBottom] = useState(IMAGE_HEIGHT);
  const [right, setRight] = useState(IMAGE_WIDTH);

  const renderOverscan = async () => {
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

  return (
    <form onSubmit={renderOverscan} className="space-y-4 ">
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
        Render Overscan
      </button>
    </form>
  );
};
