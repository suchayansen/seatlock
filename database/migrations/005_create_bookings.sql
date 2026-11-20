CREATE TABLE bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    event_id UUID NOT NULL
        REFERENCES events(id),

    student_id UUID NOT NULL
        REFERENCES users(id),

    hold_id UUID NOT NULL
        REFERENCES holds(id),

    booking_reference VARCHAR(30) UNIQUE NOT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'confirmed'
        CHECK (status IN ('confirmed', 'cancelled', 'checked_in')),

    booked_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    cancelled_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_bookings_student
ON bookings(student_id);

CREATE INDEX idx_bookings_event
ON bookings(event_id);