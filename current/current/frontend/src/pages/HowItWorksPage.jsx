import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { FaCogs, FaSearch, FaCheckDouble, FaLayerGroup } from 'react-icons/fa';

const HowItWorksPage = () => {
  return (
    <div className="d-flex flex-column min-vh-100 bg-light">
      <Navbar />

      <main className="container py-5 flex-grow-1">
        <div className="card app-card p-4 p-md-5 border">
          <h2 className="fw-extrabold text-dark mb-3">How the Fake News Detection Engine Works</h2>
          <p className="lead text-muted mb-5">
            A step-by-step walkthrough of the text ingestion, natural language processing,
            mathematical classification, and dual-engine consensus workflow.
          </p>

          <div className="row g-4">
            <div className="col-md-6">
              <div className="card h-100 p-4 border bg-white shadow-sm">
                <span className="badge bg-primary mb-3" style={{ width: 'fit-content' }}>Step 1: Ingestion &amp; Caching</span>
                <h5 className="fw-bold">Deterministic Hashing</h5>
                <p className="text-muted small">
                  The title and article are normalized, lowercased, and processed through SHA-256.
                  If an exact match was already evaluated by the current active model version, the verified cached result is returned instantly.
                </p>
              </div>
            </div>

            <div className="col-md-6">
              <div className="card h-100 p-4 border bg-white shadow-sm">
                <span className="badge bg-primary mb-3" style={{ width: 'fit-content' }}>Step 2: NLP Preprocessing</span>
                <h5 className="fw-bold">Linguistic Tokenization</h5>
                <p className="text-muted small">
                  Punctuation, URLs, emails, and English stopwords are stripped.
                  Titles receive proportional weight ($2\times$) to amplify the semantic salience of headlines before vectorization.
                </p>
              </div>
            </div>

            <div className="col-md-6">
              <div className="card h-100 p-4 border bg-white shadow-sm">
                <span className="badge bg-primary mb-3" style={{ width: 'fit-content' }}>Step 3: TF-IDF Vectorization</span>
                <h5 className="fw-bold">Sublinear N-Gram Features</h5>
                <p className="text-muted small">
                  The text is projected onto a 5,000-dimensional TF-IDF space with unigrams and bigrams $(1, 2)$.
                  This captures not just individual words, but phrase collocations like <em>"secret tribunal"</em> or <em>"clinical trial"</em>.
                </p>
              </div>
            </div>

            <div className="col-md-6">
              <div className="card h-100 p-4 border bg-white shadow-sm">
                <span className="badge bg-primary mb-3" style={{ width: 'fit-content' }}>Step 4: Calibrated Classification</span>
                <h5 className="fw-bold">Calibrated Linear SVM</h5>
                <p className="text-muted small">
                  A Linear Support Vector Classifier evaluated via <code>CalibratedClassifierCV</code> transforms the hyperplane margin into true posterior probabilities.
                  If the maximum probability falls below 60%, the engine returns <strong>INCONCLUSIVE</strong>.
                </p>
              </div>
            </div>

            <div className="col-12">
              <div className="card p-4 border bg-primary-light shadow-sm">
                <span className="badge bg-dark mb-3" style={{ width: 'fit-content' }}>Step 5: Latest News &amp; Gemini Dual-Engine Consensus</span>
                <h5 className="fw-bold text-primary">LLM Verification &amp; Conflict Resolution</h5>
                <p className="text-dark small mb-0">
                  When analyzing current/latest news, the backend concurrently invokes Google Gemini via the official SDK.
                  Gemini independently analyzes the core claims against its knowledge base.
                  If the ML classifier and Gemini agree, confidence is reinforced.
                  If they disagree, the system alerts the user with an explicit <strong>INCONCLUSIVE / CONFLICT</strong> status,
                  preventing false sense of certainty.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default HowItWorksPage;
