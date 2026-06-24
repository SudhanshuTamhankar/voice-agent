import React from 'react';
import './Widgets.css';

export default function FormulaWidget({ data }) {
  if (!data) return null;
  
  const { institute, formula, key_factors } = data;

  return (
    <div className="glass-panel widget-container formula-widget fade-in">
      <h2 className="widget-title">{institute} Methodology</h2>
      
      <div className="formula-box">
        <code className="formula-text">{formula}</code>
      </div>
      
      <div className="factors-list">
        <h3>Key Factors</h3>
        <ul>
          {key_factors && key_factors.map((factor, idx) => (
            <li key={idx} className="factor-pill">{factor}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
