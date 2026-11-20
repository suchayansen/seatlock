CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    organizer_id UUID NOT NULL
        REFERENCES users(id),

    title VARCHAR(200) NOT NULL,
    description TEXT,

    venue VARCHAR(255) NOT NULL,
    event_date TIMESTAMPTZ NOT NULL,

    booking_opens_at TIMESTAMPTZ,
    booking_closes_at TIMESTAMPTZ,

    status VARCHAR(20) NOT NULL DEFAULT 'draft'
        CHECK (status IN ('draft', 'published', 'cancelled', 'completed')),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);