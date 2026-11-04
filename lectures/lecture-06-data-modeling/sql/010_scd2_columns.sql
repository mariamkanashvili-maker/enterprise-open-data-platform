-- dim_location-ის SCD Type 2 ვერსია — 3 დამატებითი სვეტი ისტორიისთვის
ALTER TABLE analytics.dim_location
ADD COLUMN IF NOT EXISTS valid_from DATE NOT NULL DEFAULT CURRENT_DATE,
ADD COLUMN IF NOT EXISTS valid_to DATE,
ADD COLUMN IF NOT EXISTS is_current BOOLEAN NOT NULL DEFAULT TRUE;
