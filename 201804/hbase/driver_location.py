#coding:utf-8
import happybase


def connect_hbase(host="yn-vm-test-202-71", port=9090):
    connection = happybase.Connection(host=host, port=port, autoconnect=False)
    connection.open()
    return connection


def process_hbase(client):
    # 操作testtable表
    # 这个操作是一个提前声明-我要用到这个表了-但不会提交给thrift server做操作
    table = client.table(b'realtime_trans:driver_location_track')
    for key, data in table.scan():
        print(key, data)


if __name__ == "__main__":
    hbase_client = connect_hbase()
    process_hbase(hbase_client)