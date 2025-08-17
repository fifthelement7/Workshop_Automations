import Link from 'next/link';
import { Upload, FileText, Users, TrendingUp } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-4">
            Mindscribe
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8">
            AI-Powered Coaching Session Analysis
          </p>
          <p className="text-lg text-gray-500 max-w-3xl mx-auto">
            Transform your coaching sessions into actionable insights with advanced AI analysis. 
            Upload transcripts and get detailed summaries, participant engagement metrics, and coaching recommendations.
          </p>
        </div>

        {/* Main CTA */}
        <div className="text-center mb-16">
          <Link
            href="/upload"
            className="inline-flex items-center bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg"
          >
            <Upload className="w-6 h-6 mr-3" />
            Upload Session Transcript
          </Link>
          <p className="text-sm text-gray-500 mt-2">
            Support for .txt and .docx files up to 10MB
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <div className="bg-blue-100 rounded-full p-3 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <FileText className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Easy Upload
            </h3>
            <p className="text-gray-600">
              Simply upload your session transcripts in .txt or .docx format. 
              Our system automatically processes and analyzes the content.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <div className="bg-green-100 rounded-full p-3 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <Users className="w-8 h-8 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Participant Tracking
            </h3>
            <p className="text-gray-600">
              Automatically identifies participants in your sessions and tracks 
              their engagement levels and speaking patterns.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <div className="bg-purple-100 rounded-full p-3 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <TrendingUp className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              AI Insights
            </h3>
            <p className="text-gray-600">
              Get detailed analysis with breakthrough detection, action items, 
              and personalized coaching recommendations.
            </p>
          </div>
        </div>

        {/* Process Steps */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-center text-gray-900 mb-8">
            How It Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center mx-auto mb-4 text-lg font-bold">
                1
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Upload</h3>
              <p className="text-gray-600">
                Upload your session transcript file or paste the text directly into our interface.
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center mx-auto mb-4 text-lg font-bold">
                2
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Process</h3>
              <p className="text-gray-600">
                Our AI analyzes the transcript, identifies participants, and extracts key insights.
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center mx-auto mb-4 text-lg font-bold">
                3
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Analyze</h3>
              <p className="text-gray-600">
                Review detailed summaries, engagement metrics, and actionable coaching recommendations.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}