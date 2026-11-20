CREATE TABLE seats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    event_id UUID NOT NULL
        REFERENCES events(id) ON DELETE CASCADE,

    seat_number VARCHAR(20) NOT NULL,
    section VARCHAR(50),

    status VARCHAR(20) NOT NULL DEFAULT 'available'
        CHECK (status IN ('available', 'held', 'booked', 'blocked')),

    version INTEGER NOT NULL DEFAULT 1,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_event_seat
        UNIQUE (event_id, seat_number)
);

CREATE INDEX idx_seats_event_status
ON seats(event_id, status);