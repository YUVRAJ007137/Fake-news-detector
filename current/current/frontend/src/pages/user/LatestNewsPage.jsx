import React, { useState } from 'react';
import { newsService } from '../../services/newsService';
import PredictionCard from '../../components/PredictionCard';
import { FaRobot, FaSearch, FaEraser, FaBrain, FaExternalLinkAlt, FaCheckCircle, FaExclamationTriangle } from 'react-icons/fa';
import { toast } from 'react-toastify';

const LatestNewsPage = () => {
  const [formData, setFormData] = useState({
    title: '',
    article: '',
    category: 'General',
    source: 'Latest News'
  });
  const [loading, setLoading] = useState(false);
  const [analysisResponse, setAnalysisResponse] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleClear = () => {
    setFormData({
      title: '',
      article: '',
      category: 'General',
      source: 'Latest News'
    });
    setAnalysisResponse(null);
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!formData.title.trim() || !formData.article.trim()) {
      toast.error('Both News Title and News Article text are required.');
      return;
    }

    if (formData.article.trim().length < 20) {
      toast.warning('Article content is too short (minimum 20 characters).');
      return;
    }

    setLoading(true);
    try {
      const res = await newsService.analyzeLatestNews(
        formData.title,
        formData.article,
        formData.category,
        formData.source
      );
      setAnalysisResponse(res);
      toast.success(res.message || 'Dual-engine analysis completed.');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Analysis failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="row justify-content-center">
      <div className="col-lg-10">
        <div className="card app-card border-0 shadow-sm p-4 mb-4 bg-white">
          <div className="mb-4">
            <h4 className="fw-bold text-dark d-flex align-items-center gap-2 mb-1">
              <FaRobot className="text-primary" /> Latest &amp; Current News Analysis (Gemini + ML)
            </h4>
            <p className="text-muted small mb-0">
              Evaluates incoming news using our trained classical classifier combined with Google Gemini claim verification.
            </p>
          </div>

          <form onSubmit={handleAnalyze}>
            <div className="mb-3">
              <label className="form-label small fw-semibold">News Headline / Title *</label>
              <input
                type="text"
                name="title"
                className="form-control"
                placeholder="Enter current news title or breaking headline..."
                value={formData.title}
                onChange={handleChange}
                required
              />
            </div>

            <div className="row g-3 mb-3">
              <div className="col-md-6">
                <label className="form-label small fw-semibold">Domain Category</label>
                <select
                  name="category"
                  className="form-select"
                  value={formData.category}
                  onChange={handleChange}
                >
                  <option value="General">General News</option>
                  <option value="Politics">Politics &amp; Elections</option>
                  <option value="Health">Health &amp; Medicine</option>
                  <option value="Technology">Technology &amp; Artificial Intelligence</option>
                  <option value="Science">Science &amp; Environment</option>
                  <option value="Business">Business &amp; Finance</option>
                </select>
              </div>

              <div className="col-md-6">
                <label className="form-label small fw-semibold">Reported Source / Outlet</label>
                <input
                  type="text"
                  name="source"
                  className="form-control"
                  placeholder="e.g. Wire Service, Social Broadcast, News Portal"
                  value={formData.source}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="mb-4">
              <label className="form-label small fw-semibold">Full News Article Content *</label>
              <textarea
                name="article"
                rows="6"
                className="form-control"
                placeholder="Paste the news article or breaking claims for dual-engine verification..."
                value={formData.article}
                onChange={handleChange}
                required
              ></textarea>
              <div className="form-text small text-end">
                Character count: {formData.article.length}
              </div>
            </div>

            <div className="d-flex gap-2">
              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary px-4 py-2 fw-semibold d-flex align-items-center gap-2"
              >
                <FaSearch /> {loading ? 'Invoking Dual-Engine Verification...' : 'Verify News Authenticity'}
              </button>
              <button
                type="button"
                onClick={handleClear}
                className="btn btn-outline-secondary px-3 py-2 d-flex align-items-center gap-1"
              >
                <FaEraser /> Clear
              </button>
            </div>
          </form>

          {/* Dual-Engine Presentation */}
          {analysisResponse && (
            <div className="mt-4">
              {/* Top Decision Pill */}
              <div className="card app-card border-0 shadow-sm p-4 mb-4 bg-light">
                <div className="d-flex flex-wrap justify-content-between align-items-center gap-2">
                  <div>
                    <span className="text-muted small d-block">CONSENSED VERDICT</span>
                    <h3 className="fw-bold mb-0 text-dark">
                      {analysisResponse.overall_decision}
                    </h3>
                  </div>
                  <div>
                    <span className={`badge fs-6 ${analysisResponse.gemini_analysis?.agreement_status === 'AGREE' ? 'bg-success' : 'bg-warning text-dark'}`}>
                      Agreement: {analysisResponse.gemini_analysis?.agreement_status || 'STANDALONE'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Side-by-Side Dual Breakdown */}
              <div className="row g-4 mb-4">
                {/* Engine 1: Classical ML */}
                <div className="col-md-6">
                  <div className="card app-card h-100 p-4 border bg-white shadow-sm">
                    <div className="d-flex align-items-center gap-2 mb-3 text-primary">
                      <FaBrain className="fs-4" />
                      <h5 className="fw-bold mb-0">Local Machine Learning Engine</h5>
                    </div>
                    <div className="mb-2">
                      <span className="text-muted small">Linguistic Prediction:</span>
                      <h4 className="fw-bold my-1 text-dark">
                        {analysisResponse.ml_prediction?.prediction_label}
                      </h4>
                    </div>
                    <div className="mb-3">
                      <span className="text-muted small">Confidence Score:</span>
                      <strong className="d-block text-dark">
                        {(analysisResponse.ml_prediction?.confidence_score * 100).toFixed(1)}%
                      </strong>
                    </div>
                    <p className="text-muted small mb-0">
                      {analysisResponse.ml_prediction?.explanation}
                    </p>
                  </div>
                </div>

                {/* Engine 2: Google Gemini */}
                <div className="col-md-6">
                  <div className="card app-card h-100 p-4 border bg-white shadow-sm">
                    <div className="d-flex align-items-center gap-2 mb-3 text-primary">
                      <FaRobot className="fs-4" />
                      <h5 className="fw-bold mb-0">Google Gemini LLM Engine</h5>
                    </div>
                    <div className="mb-2">
                      <span className="text-muted small">Factual Assessment:</span>
                      <h4 className="fw-bold my-1 text-dark">
                        {analysisResponse.gemini_analysis?.assessment}
                      </h4>
                    </div>
                    <div className="mb-3">
                      <span className="text-muted small">API Status:</span>
                      <strong className="d-block text-dark">
                        {analysisResponse.gemini_analysis?.available ? 'Configured & Active' : 'Offline / Unconfigured'}
                      </strong>
                    </div>
                    <p className="text-muted small mb-3">
                      {analysisResponse.gemini_analysis?.evidence_summary}
                    </p>
                    {analysisResponse.gemini_analysis?.sources && analysisResponse.gemini_analysis.sources.length > 0 && (
                      <div className="small text-muted border-top pt-2">
                        <strong>Referenced Entities:</strong> {analysisResponse.gemini_analysis.sources.join(', ')}
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Standard PredictionCard with Save button */}
              <PredictionCard
                result={{
                  ...analysisResponse.ml_prediction,
                  overall_decision: analysisResponse.overall_decision,
                  gemini_analysis: analysisResponse.gemini_analysis,
                  news_id: analysisResponse.news_id
                }}
                newsId={analysisResponse.news_id}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LatestNewsPage;
