create or refresh streaming table ext_cat.demo2.baby_names_raw
as
select year, `First Name` as first_name, County, Sex, Count
from
STREAM(
    read_files(
        '/Volumes/ext_cat/demo2/demo2_vol/',
        format => 'csv',
        header => true,
        mode => 'failfast'
    ) );

create or refresh materialized view ext_cat.demo2.baby_names_prepared (
    constraint valid_first_name expect (first_name is not null),
    constraint valid_count expect (count > 0) on violation fail update
    )
as
select year as year_of_birth,
First_name,
count
from ext_cat.demo2.baby_names_raw;

create or refresh materialized view ext_cat.demo2.top_baby_names_2021
as
 select first_name, sum(count) as total_count
from ext_cat.demo2.baby_names_prepared
where year_of_birth = 2021
group by first_name
order by total_count desc
limit 10;