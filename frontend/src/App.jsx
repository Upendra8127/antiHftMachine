import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [signals, setSignals] = useState([])
  const [kpis, setKpis] = useState({
    total_active_alerts: 0,
    net_positive_ratio: 0,
    net_negative_ratio: 0,
    overall_ai_accuracy: 0
  })
  
  // Controls
  const [minConfidence, setMinConfidence] = useState(0.5)
  const [targetImpact, setTargetImpact] = useState(0)
  const [hideNeutral, setHideNeutral] = useState(false)
  const [timeframeHours, setTimeframeHours] = useState(24) // Default 24 hours

  const fetchData = async () => {
    try {
      const signalRes = await fetch(`http://localhost:8000/api/signals?min_confidence=${minConfidence}&hide_neutral=${hideNeutral}`)
      const signalData = await signalRes.json()
      
      const now = new Date();
      // Filter by target impact and timeframe locally
      const filteredSignals = signalData.filter(s => {
        const meetsImpact = Math.abs(s.simulated_return_impact) >= targetImpact;
        
        const signalDate = new Date(s.timestamp + 'Z'); // ensure UTC parsing if needed, but backend gives iso
        const hoursDiff = (now - new Date(s.timestamp)) / (1000 * 60 * 60);
        const meetsTimeframe = hoursDiff <= timeframeHours;
        
        return meetsImpact && meetsTimeframe;
      })
      setSignals(filteredSignals)

      const kpiRes = await fetch('http://localhost:8000/api/kpis')
      const kpiData = await kpiRes.json()
      setKpis(kpiData)
    } catch (error) {
      console.error("Failed to fetch data:", error)
    }
  }

  useEffect(() => {
    fetchData()
    // Poll every 10 seconds for updates
    const interval = setInterval(fetchData, 10000)
    return () => clearInterval(interval)
  }, [minConfidence, targetImpact, hideNeutral, timeframeHours])

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleTimeString('en-IN', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    })
  }

  const getSentimentClass = (label) => {
    if (label === 'BUY POSITION') return 'positive';
    if (label === 'SELL POSITION') return 'negative';
    return 'neutral';
  }

  return (
    <div className="app-container">
      <header>
        <h1>antiHftMachine V2</h1>
        <p>Dynamic Market Mover Intelligence</p>
      </header>

      {/* Global KPIs */}
      <section className="kpi-grid">
        <div className="kpi-card glass-panel">
          <span className="kpi-label">Active Alerts</span>
          <span className="kpi-value">{kpis.total_active_alerts}</span>
        </div>
        <div className="kpi-card glass-panel">
          <span className="kpi-label">Buy Signals</span>
          <span className="kpi-value" style={{color: 'var(--positive-color)'}}>{kpis.net_positive_ratio.toFixed(1)}%</span>
        </div>
        <div className="kpi-card glass-panel">
          <span className="kpi-label">Sell Signals</span>
          <span className="kpi-value" style={{color: 'var(--negative-color)'}}>{kpis.net_negative_ratio.toFixed(1)}%</span>
        </div>
        <div className="kpi-card glass-panel">
          <span className="kpi-label">Historical Accuracy</span>
          <span className="kpi-value">{kpis.overall_ai_accuracy.toFixed(1)}%</span>
        </div>
      </section>

      <main className="main-content">
        {/* Control Panel */}
        <aside className="control-panel glass-panel">
          <h2>Filters</h2>
          
          <div className="control-group">
            <label>Timeframe</label>
            <select 
              value={timeframeHours} 
              onChange={(e) => setTimeframeHours(Number(e.target.value))}
              style={{width: '100%', padding: '0.5rem', marginTop: '0.5rem', background: 'var(--bg-lighter)', color: 'white', border: '1px solid #333', borderRadius: '4px'}}
            >
              <option value={1}>Last 1 Hour</option>
              <option value={4}>Last 4 Hours</option>
              <option value={24}>Last 24 Hours</option>
              <option value={168}>Last 7 Days</option>
              <option value={720}>Last 30 Days</option>
            </select>
          </div>

          <div className="control-group">
            <label>
              Min Confidence
              <span>{(minConfidence * 100).toFixed(0)}%</span>
            </label>
            <input 
              type="range" 
              min="0" max="1" step="0.05" 
              value={minConfidence}
              onChange={(e) => setMinConfidence(parseFloat(e.target.value))}
            />
          </div>

          <div className="control-group">
            <label>
              Target Impact
              <span>{targetImpact.toFixed(1)}%+</span>
            </label>
            <input 
              type="range" 
              min="0" max="5" step="0.1" 
              value={targetImpact}
              onChange={(e) => setTargetImpact(parseFloat(e.target.value))}
            />
          </div>

          <label className="checkbox-group">
            <input 
              type="checkbox" 
              checked={hideNeutral}
              onChange={(e) => setHideNeutral(e.target.checked)}
            />
            Hide Neutral Sentiment
          </label>
        </aside>

        {/* Interactive Feed */}
        <section className="feed-container">
          {signals.length === 0 ? (
            <div className="glass-panel" style={{padding: '2rem', textAlign: 'center', color: 'var(--text-secondary)'}}>
              No signals matching criteria.
            </div>
          ) : (
            signals.map(signal => {
              const sentimentClass = getSentimentClass(signal.sentiment_label)
              
              return (
                <div key={signal.id} className={`signal-card glass-panel ${sentimentClass}`}>
                  <div className="signal-header">
                    <div>
                        <span className="signal-ticker">{signal.company_name}</span>
                        {signal.industry && (
                            <span style={{marginLeft: '0.5rem', fontSize:'0.75rem', padding: '0.2rem 0.5rem', background: 'var(--bg-lighter)', borderRadius: '4px', color: 'var(--text-secondary)'}}>
                                {signal.industry}
                            </span>
                        )}
                        {signal.needs_clarification && (
                            <span style={{marginLeft: '0.5rem', fontSize:'0.75rem', padding: '0.2rem 0.5rem', background: '#ff980033', color: '#ff9800', border: '1px solid #ff9800', borderRadius: '4px'}}>
                                ⚠️ See Manually for Clarification
                            </span>
                        )}
                    </div>
                    <span className={`badge ${sentimentClass}`}>{signal.sentiment_label}</span>
                  </div>
                  
                  <p className="signal-headline">{signal.raw_headline}</p>
                  
                  <div className="signal-meta">
                    <span>⏱ {formatDate(signal.timestamp)}</span>
                    <span>
                      Confidence: {(signal.confidence_score * 100).toFixed(0)}%
                      <div className="confidence-bar-bg">
                        <div className="confidence-bar-fill" style={{width: `${signal.confidence_score * 100}%`}}></div>
                      </div>
                    </span>
                    <span>Expected Impact: {signal.simulated_return_impact > 0 ? '+' : ''}{signal.simulated_return_impact.toFixed(2)}%</span>
                    
                    {signal.source_url && (
                        <a href={signal.source_url} target="_blank" rel="noreferrer" style={{color: '#4facfe', textDecoration: 'none', fontWeight: 'bold'}}>
                            Read Source →
                        </a>
                    )}
                    
                    {signal.performance && (
                      <span className={`return-badge ${signal.performance.is_accurate ? 'accurate' : 'inaccurate'}`}>
                        {signal.performance.is_accurate ? '✅' : '❌'} EOD: {signal.performance.actual_return_percentage.toFixed(2)}%
                      </span>
                    )}
                  </div>
                </div>
              )
            })
          )}
        </section>
      </main>
    </div>
  )
}

export default App
