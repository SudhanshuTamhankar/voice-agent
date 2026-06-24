import React from 'react';
import './Widgets.css';

export default function TargetPercentileWidget({ data }) {
  if (!data) return null;

  const { institute, target_range, academic_gap_percentage, required_cat_score, target_composite } = data;

  return (
    <div className="glass-panel widget-container percentile-widget fade-in">
      <h2 className="widget-title">Target Percentile: {institute}</h2>
      
      <div className="percentile-display">
        <span className="percentile-value">{target_range}</span>
        <span className="percentile-label">%ile</span>
      </div>
      
      <div className="stats-grid">
        <div className="stat-box">
          <span className="stat-label">Academic Gap</span>
          <span className="stat-value">{academic_gap_percentage}%</span>
        </div>
        <div className="stat-box">
          <span className="stat-label">Req. CAT Score</span>
          <span className="stat-value">{required_cat_score}</span>
        </div>
        <div className="stat-box">
          <span className="stat-label">Target Composite</span>
          <span className="stat-value">{target_composite}</span>
        </div>
      </div>
      
      <div className="range-bar-container">
        <div className="range-bar">
          <div className="range-fill" style={{ width: '80%', marginLeft: '10%' }}></div>
        </div>
        <div className="range-labels">
          <span>Safe</span>
          <span>Target</span>
          <span>Reach</span>
        </div>
      </div>
    </div>
  );
}
