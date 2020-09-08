-- PRIM server
select * from Orders

--insert Orders(total_quantity, total_price, date, productId, customerId)
--values (1, 1500, GETDATE(), 2, 1)

--delete from Orders where status = 0

--delete from Orders where id = 15
--delete from Orders where id = 16

-- trigger
drop trigger tr_trans_repl
go

create trigger tr_trans_repl on Orders for insert as 
	update Orders set status=1 where id in (select inserted.id from inserted)

go