CREATE PROCEDURE `receipt_month`()
begin
truncate table receipt_report;
truncate table post_report;
truncate TABLE not_receive_report;

insert into receipt_report (community_name, company, count, my_month)
select community.`name`, company, count(*) , DATE_FORMAT(delivery_time,'%Y-%m')
from receipt inner join community
ON community.id = receipt.community_id
group by community.`name`,company, DATE_FORMAT(delivery_time,'%Y-%m');

insert into post_report (community_name, company, my_month,count,weight, amount)
select community.`name`, company, DATE_FORMAT(send_time,'%Y-%m'),count(*),sum(`weight`),sum(amount)
from `post` inner join community
ON community.id = post.community_id
group by community.`name`,company, DATE_FORMAT(send_time,'%Y-%m');

insert into not_receive_report (community_name, company, count, my_month)
select community.`name`, company, count(*) , DATE_FORMAT(delivery_time,'%Y-%m')
from receipt inner join community
ON community.id = receipt.community_id
where is_sign = 0
group by community.`name`,company, DATE_FORMAT(delivery_time,'%Y-%m');
end

use kuaidi;
insert into role(name, description) values('admin', 'administrator');
insert into role(name, description) values('user', 'end user');
insert into user(username, password) values('admin', 'u9ec4u7acb');
insert into roles_users(user_id, role_id) values('1', '1');

DROP EVENT if exists daily_report;
CREATE EVENT daily_report
ON SCHEDULE EVERY '1' DAY
STARTS '2016-06-06 23:00:00'
DO  call kuaidi.receipt_month();

show events;

