-- Shard 1
ALTER TABLE audit_logs_1
ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE audit_logs_1
ADD CONSTRAINT audit_logs_1_pkey PRIMARY KEY (id);

SELECT setval(
    pg_get_serial_sequence('public.audit_logs_1', 'id'),
    COALESCE(MAX(id), 1),
    COUNT(*) > 0
) FROM audit_logs_1;


-- Shard 2
ALTER TABLE audit_logs_2
ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE audit_logs_2
ADD CONSTRAINT audit_logs_2_pkey PRIMARY KEY (id);

SELECT setval(
    pg_get_serial_sequence('public.audit_logs_2', 'id'),
    COALESCE(MAX(id), 1),
    COUNT(*) > 0
) FROM audit_logs_2;


-- Shard 3
ALTER TABLE audit_logs_3
ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE audit_logs_3
ADD CONSTRAINT audit_logs_3_pkey PRIMARY KEY (id);

SELECT setval(
    pg_get_serial_sequence('public.audit_logs_3', 'id'),
    COALESCE(MAX(id), 1),
    COUNT(*) > 0
) FROM audit_logs_3;