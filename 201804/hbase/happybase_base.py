#coding:utf-8
import happybase

# 要先在hbase某个节点上开启thrift服务
# hbase thrift -p 9090 start

connection = happybase.Connection('yn-vm-test-202-71', autoconnect=False)
connection.open()
#
# print所有的表名
print('All tables: ', connection.tables(), '\n')


# 操作testtable表
# 这个操作是一个提前声明-我要用到这个表了-但不会提交给thrift server做操作
table = connection.table(b'testtable')

# 检索某一行
row = table.row(b'myrow-2')
print('a row:', row, '\n')

# right
print(row[b'colfam1:q1'])
print(row[b'colfam1:q2'])

# wrong
# print(row['colfam1:q1'])
# print(row['colfam1:q2'])

# 显示所有列族
print('所有列族', table.families(), '\n')

# 输出两列
print('print two rows:')
rows = table.rows([b'myrow-1', b'myrow-2'])
for key, data in rows:
    print(key, data)

# 字典输出两列
print('\n', 'print two dict rows')
rows_as_dict = dict(table.rows([b'myrow-1', b'myrow-2']))
print(rows_as_dict)

# 输入row的一个列族所有值
row = table.row(b'myrow-2', columns=[b'colfam1'])
print('\n', '输出一个列族', row)

# scan操作
print('\n', 'do scan')
for key, data in table.scan():
    print(key, data)