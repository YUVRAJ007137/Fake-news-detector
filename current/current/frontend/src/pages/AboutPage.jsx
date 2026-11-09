import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { FaGraduationCap, FaFlask, FaCode, FaBook } from 'react-icons/fa';

const AboutPage = () => {
  return (
    <div className="d-flex flex-column min-vh-100 bg-light">
      <Navbar />

      <main className="container py-5 flex-grow-1">
        <div className="card app-card p-4 p-md-5 border mb-4">
          <div className="d-flex align-items-center gap-2 mb-3 text-primary">
            <FaGraduationCap className="fs-2" />
            <span className="text-uppercase fw-bold small">Master of Computer Applications (MCA) Project</span>
          </div>

          <h2 className="fw-extrabold text-dark mb-4">Project Overview &amp; Research Motivation</h2>

          <p className="lead text-muted">
            The <strong>AI Based Fake News Detection System</strong> is an end-to-end full-stack software application
            and applied machine learning project developed to address the escalating problem of digital misinformation,
            unverified news claims, and sensationalist propaganda across web and social platforms.
          </p>

          <hr className="my-4" />

          <h4 className="fw-bold mb-3 d-flex align-items-center gap-2">
            <FaFlask className="text-primary" /> The Hybrid Dataset Construction Methodology
          </h4>
          <p className="text-muted">
            Existing fake news datasets frequently suffer from domain overfitting, publication bias, or temporal decay.
            This project implements a reproducible <strong>Hybrid Data Engineering Pipeline</strong> combining:
          </p>
          <ul className="text-muted">
            <li><strong>Self-Generated Dataset:</strong> Varied synthetic and verified real-world events across six distinct sectors: Technology, Health, Politics, Business, Education, and Science.</li>
            <li><strong>Kaggle/ISOT Benchmark Dataset:</strong> Provenance-tracked classical news articles from Reuters and documented disinformation archives.</li>
            <li><strong>Harmonization:</strong> SHA-256 deduplication, linguistic cleaning, and stratified 80/20 train-test splitting to prevent data leakage.</li>
          </ul>

          <h4 className="fw-bold mt-4 mb-3 d-flex align-items-center gap-2">
            <FaCode className="text-primary" /> Technology Stack Specification
          </h4>
          <div className="table-responsive">
            <table className="table table-bordered table-custom">
              <thead>
                <tr>
                  <th>Layer</th>
                  <th>Technologies &amp; Libraries</th>
                  <th>Design Rationale</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="fw-bold">Frontend</td>
                  <td>React.js (v18), Vite, Bootstrap 5, Chart.js, React Icons, Axios</td>
                  <td>Ultra-fast bundling, responsive layout, accessible UI, and real-time interactive charts.</td>
                </tr>
                <tr>
                  <td className="fw-bold">Backend</td>
                  <td>Python (3.14/3.12), Flask, Flask-SQLAlchemy, Flask-JWT-Extended</td>
                  <td>Microservice modularity, parameterized SQL operations, and clean REST architecture.</td>
                </tr>
                <tr>
                  <td className="fw-bold">Machine Learning</td>
                  <td>Scikit-learn, TF-IDF Vectorizer, Calibrated Linear SVM, Logistic Regression</td>
                  <td>Linguistic n-gram feature extraction with true Platt-calibrated posterior probabilities.</td>
                </tr>
                <tr>
                  <td className="fw-bold">LLM Intelligence</td>
                  <td>Official <code>google-genai</code> Python SDK (Gemini 2.5 Flash)</td>
                  <td>Real-time semantic claim verification and consensus checking with prompt security.</td>
                </tr>
                <tr>
                  <td className="fw-bold">Database</td>
                  <td>MySQL 8.0+ / SQLite development fallback</td>
                  <td>11 relational tables enforcing primary keys, foreign keys, cascades, and indexes.</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="alert alert-info border mt-4">
            <strong>System Epistemic Boundary:</strong> The application does not claim absolute philosophical certainty of truth.
            It provides calibrated mathematical confidence and structured LLM evidence to assist human judgment.
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default AboutPage;
