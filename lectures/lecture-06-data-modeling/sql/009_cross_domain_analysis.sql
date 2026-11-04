SELECT
    dd.full_date,
    ROUND(AVG(fw.temperature_c), 1)                          AS avg_temp_tbilisi,
    ROUND(AVG(fc.rate) FILTER (WHERE dc.code = 'USD'), 4)    AS usd_rate,
    COUNT(DISTINCT fs.fact_id)                               AS earthquake_count
FROM analytics.dim_date dd
LEFT JOIN analytics.fact_weather fw  ON fw.date_key = dd.date_key
LEFT JOIN analytics.fact_currency fc ON fc.date_key = dd.date_key
LEFT JOIN analytics.dim_currency dc  ON dc.currency_key = fc.currency_key
LEFT JOIN analytics.fact_seismic fs  ON fs.date_key = dd.date_key
WHERE dd.full_date = '2026-08-27'
GROUP BY dd.full_date;
