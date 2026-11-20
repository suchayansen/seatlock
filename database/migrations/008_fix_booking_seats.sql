-- Remove the unconditional uniqueness restriction
ALTER TABLE booking_seats
DROP CONSTRAINT IF EXISTS one_active_booking_per_seat;

-- Add indexes for efficient booking lookups
CREATE INDEX IF NOT EXISTS idx_booking_seats_seat_id
ON booking_seats(seat_id);

CREATE INDEX IF NOT EXISTS idx_booking_seats_booking_id
ON booking_seats(booking_id);