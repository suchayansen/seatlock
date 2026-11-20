CREATE TABLE hold_seats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    hold_id UUID NOT NULL
        REFERENCES holds(id) ON DELETE CASCADE,

    seat_id UUID NOT NULL
        REFERENCES seats(id),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_seat_per_hold
        UNIQUE (hold_id, seat_id)
);

CREATE INDEX idx_hold_seats_seat
ON hold_seats(seat_id);

CREATE INDEX idx_hold_seats_hold
ON hold_seats(hold_id);