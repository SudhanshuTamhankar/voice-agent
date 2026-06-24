import React from 'react';
import './Widgets.css';

export default function ProfileCardWidget({ profile }) {
  if (!profile) return null;

  return (
    <div className="glass-panel widget-container profile-widget fade-in">
      <h3 className="widget-title small">Current Profile</h3>
      
      <div className="profile-grid">
        <div className="profile-item">
          <span className="profile-label">Category:</span>
          <span className="profile-value">{profile.category || '--'}</span>
        </div>
        <div className="profile-item">
          <span className="profile-label">Gender:</span>
          <span className="profile-value">{profile.gender || '--'}</span>
        </div>
        <div className="profile-item">
          <span className="profile-label">10th:</span>
          <span className="profile-value">{profile.tenth_score || '--'}%</span>
        </div>
        <div className="profile-item">
          <span className="profile-label">12th:</span>
          <span className="profile-value">{profile.twelfth_score || '--'}%</span>
        </div>
        <div className="profile-item">
          <span className="profile-label">Grad:</span>
          <span className="profile-value">{profile.grad_score || '--'}%</span>
        </div>
        <div className="profile-item">
          <span className="profile-label">Stream:</span>
          <span className="profile-value">{profile.grad_stream || '--'}</span>
        </div>
        <div className="profile-item">
          <span className="profile-label">Work Ex:</span>
          <span className="profile-value">{profile.work_ex_months ? `${profile.work_ex_months}m` : '--'}</span>
        </div>
        <div className="profile-item highlight">
          <span className="profile-label">CAT %ile:</span>
          <span className="profile-value">{profile.actual_percentile || '--'}</span>
        </div>
      </div>
    </div>
  );
}
