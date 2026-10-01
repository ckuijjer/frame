import { useState } from 'react';

export const CurrentImage = () => {
  // Cache-busting query param - the browser would otherwise keep showing
  // a stale cached /api/current_image after a new render/upload, since
  // the URL itself never changes.
  const [cacheBust, setCacheBust] = useState(() => Date.now());
  const [loadFailed, setLoadFailed] = useState(false);

  const refresh = () => {
    setLoadFailed(false);
    setCacheBust(Date.now());
  };

  return (
    <>
      <div className="flex-1 flex items-center justify-center mb-4">
        {loadFailed ? (
          <p className="text-gray-500">Nothing displayed yet</p>
        ) : (
          <img
            src={`/api/current_image?t=${cacheBust}`}
            onError={() => setLoadFailed(true)}
            alt="Current image on the Inky display"
            className="max-w-full max-h-full rounded"
          />
        )}
      </div>
      <button
        onClick={refresh}
        className="px-4 py-2 bg-blue-500 text-white rounded w-full"
      >
        Refresh
      </button>
    </>
  );
};
