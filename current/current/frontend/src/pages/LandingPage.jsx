import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import {
  FaShieldAlt, FaRobot, FaBrain, FaFileUpload,
  FaDatabase, FaCheckCircle, FaArrowRight, FaLock
} from 'react-icons/fa';

const LandingPage = () => {
  return (
    <div className="d-flex flex-column min-vh-100 bg-white">
      <Navbar />

      {/* Hero Section */}
      <section className="py-5 bg-light border-bottom">
        <div className="container py-4 text-center">
          <div className="d-inline-flex align-items-center gap-2 px-3 py-1 mb-3 rounded-pill bg-white border shadow-sm">
            <FaShieldAlt className="text-primary" />
            <span className="small fw-semibold text-dark">Dual-Engine Verification &bull; Classical ML + Google GenAI</span>
          </div>

          <h1 className="display-4 fw-extrabold text-dark mb-3 tracking-tight">
            AI-Powered <span className="text-primary">Fake News Detection</span> System
          </h1>
          <p className="lead text-muted col-lg-8 mx-auto mb-4">
            An academic &amp; enterprise-grade intelligence platform that evaluates news authenticity
            using Calibrated Linear SVMs, TF-IDF linguistic feature vectors, and real-time Gemini LLM claim verification.
          </p>

          <div className="d-flex flex-wrap justify-content-center gap-3">
            <Link to="/register" className="btn btn-primary btn-lg px-4 d-flex align-items-center gap-2 shadow-sm">
              Get Started Free <FaArrowRight />
            </Link>
            <Link to="/how-it-works" className="btn btn-outline-secondary btn-lg px-4">
              Explore Architecture
            </Link>
          </div>
        </div>
      </section>

      {/* Feature Highlights Grid */}
      <section className="py-5">
        <div className="container">
          <div className="text-center mb-5">
            <h2 className="fw-bold text-dark">Engineered for Academic Rigor and Accuracy</h2>
            <p className="text-muted">Multi-layered detection pipeline combining classical and modern AI paradigms.</p>
          </div>

          <div className="row g-4">
            <div className="col-md-4">
              <div className="card app-card h-100 p-4 border">
                <div className="p-3 bg-primary-light rounded-circle text-primary d-inline-block mb-3" style={{ width: 'fit-content' }}>
                  <FaBrain className="fs-3" />
                </div>
                <h5 className="fw-bold">Calibrated Classical ML</h5>
                <p className="text-muted small">
                  Trained on our harmonized hybrid dataset using TF-IDF n-grams (1, 2) and probability-calibrated Linear Support Vector Machines with verified 93%+ accuracy.
                </p>
              </div>
            </div>

            <div className="col-md-4">
              <div className="card app-card h-100 p-4 border">
                <div className="p-3 bg-primary-light rounded-circle text-primary d-inline-block mb-3" style={{ width: 'fit-content' }}>
                  <FaRobot className="fs-3" />
                </div>
                <h5 className="fw-bold">Google Gemini GenAI</h5>
                <p className="text-muted small">
                  Official <code>google-genai</code> backend service evaluating factual claims, context coherence, and citation attribution with safe prompt-injection defenses.
                </p>
              </div>
            </div>

            <div className="col-md-4">
              <div className="card app-card h-100 p-4 border">
                <div className="p-3 bg-primary-light rounded-circle text-primary d-inline-block mb-3" style={{ width: 'fit-content' }}>
                  <FaFileUpload className="fs-3" />
                </div>
                <h5 className="fw-bold">Multi-Format Ingestion</h5>
                <p className="text-muted small">
                  Upload PDF, Word (DOCX), plain text, or batch CSV files. The engine securely extracts news records and runs automated batch inference.
                </p>
              </div>
            </div>

            <div className="col-md-4">
              <div className="card app-card h-100 p-4 border">
                <div className="p-3 bg-primary-light rounded-circle text-primary d-inline-block mb-3" style={{ width: 'fit-content' }}>
                  <FaDatabase className="fs-3" />
                </div>
                <h5 className="fw-bold">MySQL Relational Auditing</h5>
                <p className="text-muted small">
                  11 relational tables storing user history, model versions, candidate training runs, bookmarked articles, and administrator security audit trails.
                </p>
              </div>
            </div>

            <div className="col-md-4">
              <div className="card app-card h-100 p-4 border">
                <div className="p-3 bg-primary-light rounded-circle text-primary d-inline-block mb-3" style={{ width: 'fit-content' }}>
                  <FaLock className="fs-3" />
                </div>
                <h5 className="fw-bold">Role-Based Access Control</h5>
                <p className="text-muted small">
                  Strict cryptographic separation between User and Admin registration workflows, JWT tokens, and secret enrollment enforcement.
                </p>
              </div>
            </div>

            <div className="col-md-4">
              <div className="card app-card h-100 p-4 border">
                <div className="p-3 bg-primary-light rounded-circle text-primary d-inline-block mb-3" style={{ width: 'fit-content' }}>
                  <FaCheckCircle className="fs-3" />
                </div>
                <h5 className="fw-bold">Controlled Model Retraining</h5>
                <p className="text-muted small">
                  Admin portal allows importing new benchmark datasets, reviewing automated schema validation, and retraining candidate models with rollback safety.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default LandingPage;
