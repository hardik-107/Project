import { useState, useRef } from "react";
import axios from "axios";
import { Search, Upload, Play, Loader2, Clock, Sparkles, Video, AlignLeft, RotateCcw, X } from "lucide-react";

export default function App() {
  const [file, setFile] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searching, setSearching] = useState(false);
  const [message, setMessage] = useState("");
  
  // DIRECT VIDEO REFERENCE
  const videoRef = useRef(null);

  // --- FUNCTIONS ---
  const handleUpload = async (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;
    setFile(selectedFile);
    
    // Create direct blob URL
    const url = URL.createObjectURL(selectedFile);
    setVideoUrl(url);
    
    setLoading(true);
    setResults([]);
    setQuery("");
    setMessage("Processing video...");
    
    const formData = new FormData();
    formData.append("file", selectedFile);
    try {
      await axios.post("http://127.0.0.1:8000/upload-video", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage("✅ Ready to search.");
    } catch (error) {
      console.error(error);
      setMessage("❌ Error processing video.");
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!query) return;
    setSearching(true);
    setResults([]); // Purane results hatao pehle
    try {
      const res = await axios.get(`http://127.0.0.1:8000/search?query=${query}`);
      setResults(res.data.matches || []);
    } catch (error) {
      console.error(error);
    } finally {
        setSearching(false);
    }
  };

  // --- NEW: CLEAR / REFRESH SEARCH ---
  const handleClearSearch = () => {
    setQuery("");       // Text box khaali karo
    setResults([]);     // Results list saaf karo
  };

  // --- 100% WORKING SEEK FUNCTION ---
  const seekTo = (seconds) => {
    if (videoRef.current) {
      videoRef.current.currentTime = parseFloat(seconds);
      videoRef.current.play();
    } else {
        console.error("Video player not found!");
    }
  };

  // --- UI RENDER ---
  return (
    <div className="min-h-screen bg-[#09090b] text-gray-200 font-sans selection:bg-indigo-500/30">
      
      {/* Header */}
      <div className="border-b border-white/10 bg-black/20 backdrop-blur-lg sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
                <div className="bg-indigo-600 rounded-lg p-1.5 shadow-lg">
                    <Video size={20} className="text-white" />
                </div>
                <h1 className="text-xl font-bold tracking-tight text-white">
                PixelQuery <span className="text-indigo-400 font-normal">AI</span>
                </h1>
            </div>
            <div className="text-sm text-gray-400 flex items-center gap-2 bg-white/5 px-3 py-1.5 rounded-full border border-white/10">
                <Sparkles size={14} className="text-indigo-400" /> Video Search Engine
            </div>
          </div>
      </div>

      <div className="max-w-7xl mx-auto p-6 pt-8 flex flex-col lg:flex-row gap-8">
            
            {/* LEFT SIDE: Native Player */}
            <div className="lg:flex-[2] flex flex-col gap-4">
                <div className="bg-[#121212] border border-white/10 rounded-2xl overflow-hidden shadow-2xl relative group">
                  <div className="relative aspect-video bg-black">
                    {videoUrl ? (
                      <video 
                        ref={videoRef}
                        src={videoUrl}
                        controls
                        className="w-full h-full object-contain"
                      >
                        Your browser does not support the video tag.
                      </video>
                    ) : (
                      <div className="absolute top-0 left-0 w-full h-full flex flex-col items-center justify-center text-gray-500 gap-5 bg-gradient-to-b from-transparent to-black/50">
                        <div className="bg-white/5 p-4 rounded-full ring-1 ring-white/10">
                             <Upload size={32} className="opacity-60" />
                        </div>
                        <p className="text-lg font-medium text-gray-400">Upload video to start</p>
                      </div>
                    )}
                  </div>
                  
                  {/* Upload Button Overlay */}
                  <div className="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-all duration-300 z-10">
                     <input type="file" accept="video/*" onChange={handleUpload} className="hidden" id="v-upload" />
                     <label
                        htmlFor="v-upload"
                        className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg cursor-pointer shadow-lg backdrop-blur-md font-medium text-sm"
                      >
                        {loading ? <Loader2 className="animate-spin w-4 h-4" /> : <Upload className="w-4 h-4" />}
                        <span>{videoUrl ? "Change Video" : "Upload"}</span>
                      </label>
                  </div>
                </div>

                <div className="flex justify-between items-center px-2 h-6">
                    <span className={`text-sm font-medium flex items-center gap-2 ${loading ? 'text-indigo-400' : 'text-emerald-400'}`}>
                        {message && (loading ? <Loader2 size={14} className="animate-spin"/> : <Sparkles size={14}/>)}
                        {message}
                    </span>
                </div>
            </div>

            {/* RIGHT SIDE: Results */}
            <div className="lg:flex-[1] flex flex-col gap-5 h-[calc(100vh-140px)] sticky top-24">
                <div className="bg-[#121212] p-1 rounded-2xl border border-white/10 shadow-sm transition-all focus-within:ring-2 focus-within:ring-indigo-500/50">
                    <div className="relative flex items-center">
                        <Search className={`absolute left-4 ${searching ? 'text-indigo-400 animate-pulse' : 'text-gray-500'}`} size={20} />
                        
                        <input
                        type="text"
                        placeholder="Search 'red car', 'man walking'..."
                        className="w-full bg-transparent border-none text-white rounded-xl px-4 py-3.5 pl-11 pr-10 focus:outline-none text-base transition-all placeholder:text-gray-600"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                        disabled={!videoUrl || loading}
                        />

                        {/* 🔥 REFRESH / CLEAR BUTTON 🔥 */}
                        {query && (
                          <button 
                            onClick={handleClearSearch}
                            className="absolute right-3 p-1.5 hover:bg-white/10 rounded-full text-gray-400 hover:text-white transition-all"
                            title="Clear Search"
                          >
                            <X size={16} />
                          </button>
                        )}
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto pr-1 space-y-2 scrollbar-thin scrollbar-thumb-gray-800">
                    {results.length > 0 ? (
                         <>
                         <div className="flex items-center justify-between mb-2 px-1">
                            <div className="flex items-center gap-2 text-xs uppercase tracking-wider text-gray-500 font-bold">
                                <AlignLeft size={12} /> Found {results.length} Moments
                            </div>
                            <button 
                                onClick={handleClearSearch}
                                className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1 hover:underline"
                            >
                                <RotateCcw size={10} /> Reset
                            </button>
                         </div>
                         
                         {results.map((item, index) => (
                        <button
                            key={index}
                            onClick={() => seekTo(item.timestamp)}
                            className="w-full flex items-center justify-between p-3 bg-[#18181b]/50 hover:bg-[#27272a] border border-white/5 hover:border-indigo-500/50 rounded-xl transition-all group text-left active:bg-indigo-900/20"
                        >
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-full bg-indigo-500/10 flex items-center justify-center text-indigo-500 group-hover:bg-indigo-600 group-hover:text-white transition-all">
                                    <Play size={18} fill="currentColor" className="ml-0.5" />
                                </div>
                                <div>
                                    <h4 className="font-medium text-gray-200 group-hover:text-white">Jump to Scene</h4>
                                    <p className="text-xs text-indigo-400/80 font-medium">Top Match</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-1.5 pl-4 border-l border-white/10">
                                <Clock size={14} className="text-gray-600 group-hover:text-indigo-300" />
                                <span className="font-mono text-lg font-semibold text-gray-300 group-hover:text-white">
                                    {new Date(item.timestamp * 1000).toISOString().substr(14, 5)}
                                </span>
                            </div>
                        </button>
                        ))}
                        </>
                    ) : (
                        <div className={`h-full flex flex-col items-center justify-center text-gray-600 gap-3 border-2 border-dashed border-white/5 rounded-2xl ${!videoUrl && 'opacity-50'}`}>
                             {searching ? (
                                 <p className="text-indigo-400 animate-pulse">Scanning video...</p>
                             ) : (
                                <>
                                <Sparkles size={24} className="opacity-30" />
                                <p className="text-sm">Search results appear here</p>
                                </>
                             )}
                        </div>
                    )}
                </div>
            </div>
      </div>
    </div>
  );
}