CREATE UNIQUE INDEX unique_active_hold_per_student_event
ON holds(student_id, event_id)
WHERE status = 'active';