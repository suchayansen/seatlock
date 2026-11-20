CREATE TABLE booking_seats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    booking_id UUID NOT NULL
        REFERENCES bookings(id) ON DELETE CASCADE,

    seat_id UUID NOT NULL
        REFERENCES seats(id),

    price NUMERIC(10, 2) NOT NULL DEFAULT 0
        CHECK (price >= 0),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_booking_seat
        UNIQUE (booking_id, seat_id),

    CONSTRAINT one_active_booking_per_seat
        UNIQUE (seat_id)
);