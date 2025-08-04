-- Enhanced Assessment Tables for LLM-based Analysis
-- Stores detailed responses and AI analysis results

-- Table for assessment sessions
CREATE TABLE IF NOT EXISTS assessment_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    session_type TEXT NOT NULL, -- 'conversational', 'comprehensive', 'traditional'
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    total_questions INTEGER,
    questions_answered INTEGER,
    status TEXT DEFAULT 'in_progress', -- 'in_progress', 'completed', 'abandoned'
    ai_model_used TEXT, -- 'claude', 'gpt4', 'fallback'
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Table for individual responses
CREATE TABLE IF NOT EXISTS assessment_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    question_id TEXT NOT NULL,
    dimension TEXT NOT NULL, -- 'psi', 'rho', 'q', 'f'
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL, -- 'story', 'true_false', 'scale', 'choice'
    response_text TEXT,
    response_value REAL, -- For scales and numeric responses
    response_time_seconds INTEGER, -- How long they took to answer
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES assessment_sessions(id)
);

-- Table for AI analysis results
CREATE TABLE IF NOT EXISTS response_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    response_id INTEGER NOT NULL,
    dimension TEXT NOT NULL,
    overall_score REAL NOT NULL, -- 0.0 to 1.0
    confidence REAL NOT NULL, -- AI confidence in the score
    authenticity_score REAL NOT NULL,
    emotional_tone TEXT,
    analysis_text TEXT, -- AI's explanation
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (response_id) REFERENCES assessment_responses(id)
);

-- Table for sub-dimension scores
CREATE TABLE IF NOT EXISTS subdimension_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id INTEGER NOT NULL,
    subdimension_name TEXT NOT NULL,
    score REAL NOT NULL,
    FOREIGN KEY (analysis_id) REFERENCES response_analyses(id)
);

-- Table for identified indicators
CREATE TABLE IF NOT EXISTS analysis_indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id INTEGER NOT NULL,
    indicator_type TEXT NOT NULL, -- 'key_indicator', 'growth_indicator', 'concern'
    indicator_text TEXT NOT NULL,
    FOREIGN KEY (analysis_id) REFERENCES response_analyses(id)
);

-- Table for dimension summaries
CREATE TABLE IF NOT EXISTS dimension_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    dimension TEXT NOT NULL,
    overall_score REAL NOT NULL,
    pattern_summary TEXT,
    growth_summary TEXT,
    concern_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES assessment_sessions(id)
);

-- Table for final coherence profiles with gradient scores
CREATE TABLE IF NOT EXISTS coherence_profiles_detailed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    session_id INTEGER NOT NULL,
    psi_score REAL NOT NULL,
    rho_score REAL NOT NULL,
    q_score REAL NOT NULL,
    f_score REAL NOT NULL,
    static_coherence REAL NOT NULL,
    coherence_velocity REAL DEFAULT 0.0,
    coherence_level TEXT, -- 'Highly Coherent', 'Moderately Coherent', etc.
    assessment_quality REAL, -- Overall quality/confidence of the assessment
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES assessment_sessions(id)
);

-- Table for personalized insights
CREATE TABLE IF NOT EXISTS assessment_insights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    insight_type TEXT NOT NULL, -- 'strength', 'growth_area', 'pattern', 'recommendation'
    insight_text TEXT NOT NULL,
    priority INTEGER DEFAULT 0, -- Higher = more important
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES coherence_profiles_detailed(id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON assessment_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_responses_session_id ON assessment_responses(session_id);
CREATE INDEX IF NOT EXISTS idx_responses_dimension ON assessment_responses(dimension);
CREATE INDEX IF NOT EXISTS idx_analyses_response_id ON response_analyses(response_id);
CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON coherence_profiles_detailed(user_id);
CREATE INDEX IF NOT EXISTS idx_profiles_created_at ON coherence_profiles_detailed(created_at);

-- View for easy access to complete assessment data
CREATE VIEW IF NOT EXISTS complete_assessment_view AS
SELECT 
    s.id as session_id,
    s.user_id,
    s.session_type,
    s.completed_at,
    p.psi_score,
    p.rho_score,
    p.q_score,
    p.f_score,
    p.static_coherence,
    p.coherence_level,
    p.assessment_quality
FROM assessment_sessions s
JOIN coherence_profiles_detailed p ON s.id = p.session_id
WHERE s.status = 'completed'
ORDER BY s.completed_at DESC;