import React from 'react';
import FormulaWidget from './widgets/FormulaWidget';
import CollegeTableWidget from './widgets/CollegeTableWidget';
import TargetPercentileWidget from './widgets/TargetPercentileWidget';

export default function VisualizerArea({ payload }) {
  if (!payload) {
    return (
      <div className="empty-visualizer fade-in">
        <p style={{ color: 'var(--text-secondary)', textAlign: 'center', marginTop: '2rem' }}>
          Ask me about a college's methodology, your target percentile, or college recommendations!
        </p>
      </div>
    );
  }

  switch (payload.type) {
    case 'formula':
      return <FormulaWidget data={payload.data} />;
    case 'college_recommendations':
      return <CollegeTableWidget data={payload.data} />;
    case 'target_percentile':
      return <TargetPercentileWidget data={payload.data} />;
    default:
      return null;
  }
}
