import React from 'react';
import { Link } from 'react-router-dom';
import { FaShieldAlt, FaGithub, FaBook } from 'react-icons/fa';

const Footer = () => {
  return (
    <footer className="bg-white border-top mt-auto py-4 text-muted small">
      <div className="container text-center">
        <div className="d-flex flex-wrap justify-content-center align-items-center gap-3 mb-2">
          <span className="fw-semibold text-dark d-flex align-items-center gap-1">
            <FaShieldAlt className="text-primary" /> AI ML Based Fake News Detection System
          </span>
          <span>&bull;</span>
          <span>MCA Final Year Project</span>
          <span>&bull;</span>
          <Link to="/about" className="text-decoration-none text-muted">Methodology</Link>
          <span>&bull;</span>
          <Link to="/how-it-works" className="text-decoration-none text-muted">Architecture</Link>
        </div>
        <p className="mb-0 text-secondary">
          Trained on Classical NLP (TF-IDF + Calibrated Linear SVM) with Google Gemini Claim Analysis &amp; MySQL Relational Persistence.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
