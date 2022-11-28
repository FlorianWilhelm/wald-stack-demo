/* Tutorial 1: Sample queries on TPC-H data

Copyright: Snowflake
 */

SELECT l_returnflag,
       l_linestatus,
       sum(l_quantity)      as sum_qty,
       sum(l_extendedprice) as sum_base_price,
       sum(l_extendedprice * (1 - l_discount))
                            as sum_disc_price,
       sum(l_extendedprice * (1 - l_discount) *
           (1 + l_tax))     as sum_charge,
       avg(l_quantity)      as avg_qty,
       avg(l_extendedprice) as avg_price,
       avg(l_discount)      as avg_disc,
       count(*)             as count_order
FROM sampledb.tpch_sf100.lineitem
WHERE l_shipdate <= dateadd(day, -90, to_date('1998-12-01'))
GROUP BY l_returnflag,
         l_linestatus
ORDER BY l_returnflag,
         l_linestatus