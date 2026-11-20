CREATE TABLE holds (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    event_id UUID NOT NULL
        REFERENCES events(id) ON DELETE CASCADE,

    student_id UUID NOT NULL
        REFERENCES users(id),

    expires_at TIMESTAMPTZ NOT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'confirmed', 'expired', 'cancelled')),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_holds_student_event
ON holds(student_id, event_id);

CREATE INDEX idx_holds_expiry
ON holds(expires_at)
WHERE status = 'active';