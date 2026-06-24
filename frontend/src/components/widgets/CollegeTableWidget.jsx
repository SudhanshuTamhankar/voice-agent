import React from 'react';
import './Widgets.css';

export default function CollegeTableWidget({ data }) {
  if (!data) return null;

  const { strong, realistic, stretch, ambitious, bottleneck, lever } = data;

  const renderList = (title, items, type) => {
    if (!items || items.length === 0) return null;
    return (
      <div className={`college-bucket bucket-${type}`}>
        <h3 className="bucket-title">{title}</h3>
        <div className="bucket-grid">
          {items.map((col, idx) => (
            <div key={idx} className="college-card">{col}</div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="glass-panel widget-container college-widget fade-in">
      <h2 className="widget-title">Target College Buckets</h2>
      
      <div className="buckets-container">
        {renderList('Strong Chances', strong, 'strong')}
        {renderList('Realistic', realistic, 'realistic')}
        {renderList('Stretch', stretch, 'stretch')}
        {renderList('Ambitious', ambitious, 'ambitious')}
      </div>

      <div className="gap-analysis">
        <h3>Gap Analysis</h3>
        <div className="gap-item bottleneck">
          <span className="gap-label">Fixed Bottleneck:</span> {bottleneck}
        </div>
        <div className="gap-item lever">
          <span className="gap-label">Focus Lever:</span> {lever}
        </div>
      </div>
    </div>
  );
}
