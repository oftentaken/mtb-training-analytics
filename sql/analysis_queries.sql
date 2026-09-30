-- =========================================================
-- MTB Training Analytics — SQL Analysis Queries
-- Run against: data/processed/mtb_analytics.db (table: rides)
-- =========================================================

-- 1. Yearly summary: ride count, total distance, avg heart rate
SELECT
    year,
    COUNT(*) AS rides,
    ROUND(SUM(distance_km), 1) AS total_km,
    ROUND(AVG(avg_heart_rate), 1) AS avg_hr,
    ROUND(AVG(avg_speed_kmh), 1) AS avg_speed_kmh
FROM rides
GROUP BY year
ORDER BY year;


-- 2. Monthly seasonality: which months do I ride most?
SELECT
    month,
    COUNT(*) AS rides,
    ROUND(AVG(distance_km), 1) AS avg_distance_km
FROM rides
GROUP BY month
ORDER BY month;


-- 3. Top 10 longest rides of all time
SELECT
    date,
    distance_km,
    duration_min,
    total_ascent_m,
    avg_heart_rate
FROM rides
ORDER BY distance_km DESC
LIMIT 10;


-- 4. Fitness trend: VAM (vertical ascent per hour) by year
-- Higher VAM at lower heart rate = improved climbing fitness
SELECT
    year,
    ROUND(AVG(avg_heart_rate), 1) AS avg_hr,
    ROUND(AVG(total_ascent_m / (duration_min / 60.0)), 1) AS avg_vam,
    ROUND(AVG(total_ascent_m), 1) AS avg_ascent_per_ride
FROM rides
WHERE avg_heart_rate IS NOT NULL
GROUP BY year
ORDER BY year;


-- 5. Weekday vs weekend ride distribution
SELECT
    CASE
        WHEN day_of_week IN ('Saturday', 'Sunday') THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    COUNT(*) AS rides,
    ROUND(AVG(distance_km), 1) AS avg_distance_km
FROM rides
GROUP BY day_type;