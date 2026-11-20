-- Track whether a booking-seat relationship is currently active
ALTER TABLE booking_seats
ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE;

-- A seat can belong to only one active booking
CREATE UNIQUE INDEX unique_active_booking_per_seat
ON booking_seats(seat_id)
WHERE is_active = TRUE;