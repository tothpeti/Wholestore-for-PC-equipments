select * from Orders

--delete from Orders where status = 0
--delete from Orders where id = 15
--delete from Orders where id = 16

-- stored procedure
go
create procedure sp_new_order_process as
declare @status int, @event_type varchar(50), 
        @order_id int, @result int

declare cursor_events cursor forward_only static
	for
	select id, status 
	from Orders where status = 0 -- it shows the new unprocess order/event
set xact_abort on
set nocount on
open cursor_events
fetch next from cursor_events into @order_id, @status
while @@FETCH_STATUS = 0
begin
	print 'Processing Order ID=' + cast(@order_id as varchar(10))
	begin tran
	set @result = null
	if @status = 0 begin
		print '  Processing new order...'
		waitfor delay '00:00:01'
		set @result = 0
	end 
	if @result = 0 begin
		print 'Event processing OK'
		commit tran
	end else begin
		print 'Event processing failed'
		rollback tran
	end
	update Orders set status = 1 where id = @order_id
	fetch next from cursor_events into @order_id, @status
end
close cursor_events deallocate cursor_events
go

exec sp_new_order_process