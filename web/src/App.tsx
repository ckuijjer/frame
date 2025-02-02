import { GenerateImage } from './GenerateImage';
import { UploadImage } from './UploadImage';
import { OverscanImage } from './OverscanImage';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-2">Frame</h1>
      <h2 className="text-xl mb-6">
        Fetches news headlines, generates AI-based images from summaries, and
        displays them on an Inky e-ink display
      </h2>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
        <div className="bg-white p-8 rounded shadow-md text-center min-h-[200px] flex flex-col">
          <GenerateImage />
        </div>

        <div className="bg-white p-8 rounded shadow-md text-center min-h-[400px] flex flex-col">
          <UploadImage />
        </div>

        <div className="bg-white p-8 rounded shadow-md text-center min-h-[200px] flex flex-col">
          <OverscanImage />
        </div>
      </div>
    </div>
  );
}

export default App;
