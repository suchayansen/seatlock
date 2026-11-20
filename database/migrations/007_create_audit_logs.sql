CREATE TABLE audit_logs_0 (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event_id UUID REFERENCES events(id),
    actor_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    details JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE audit_logs_1 (
    LIKE audit_logs_0 INCLUDING DEFAULTS INCLUDING CONSTRAINTS
);

CREATE TABLE audit_logs_2 (
    LIKE audit_logs_0 INCLUDING DEFAULTS INCLUDING CONSTRAINTS
);

CREATE TABLE audit_logs_3 (
    LIKE audit_logs_0 INCLUDING DEFAULTS INCLUDING CONSTRAINTS
);

CREATE INDEX idx_audit_logs_0_event ON audit_logs_0(event_id);
CREATE INDEX idx_audit_logs_1_event ON audit_logs_1(event_id);
CREATE INDEX idx_audit_logs_2_event ON audit_logs_2(event_id);
CREATE INDEX idx_audit_logs_3_event ON audit_logs_3(event_id);

CREATE INDEX idx_audit_logs_0_actor ON audit_logs_0(actor_id);
CREATE INDEX idx_audit_logs_1_actor ON audit_logs_1(actor_id);
CREATE INDEX idx_audit_logs_2_actor ON audit_logs_2(actor_id);
CREATE INDEX idx_audit_logs_3_actor ON audit_logs_3(actor_id);