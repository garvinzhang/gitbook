#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import NamedTuple, Tuple, Dict, List

import pymysql


class MysqlConf(NamedTuple):
    """MysqlConf

    mysql 连接所需的参数
    """

    host: str
    user: str
    password: str
    port: int


class Mysql(object):
    """Mysql

    conn和cursor，conn断开时，cursor并不会报错，但是无法查询到数据。

    Args:
        mysqlConf (MysqlConf): asd

    Attributes:
        Select: asfa
        Execute: asd
    """

    def __init__(self, mysqlConf: MysqlConf) -> None:
        self.mysqlConn = pymysql.connect(
            host=mysqlConf.host,
            user=mysqlConf.user,
            password=mysqlConf.password,
            port=mysqlConf.port,
        )

    def Select(self, sqlStr: str) -> Tuple[bool, Tuple, str]:
        """Select

        Args:
            sqlStr (str): asd

        Returns:
            ok (bool): True
            datas (tuple): datas
            err (str): err msg
        """
        ok = False
        err = ""
        datas = ()
        self.mysqlConn.ping(reconnect=True)
        cursor = self.mysqlConn.cursor()
        try:
            cursor.execute(sqlStr)
            self.mysqlConn.commit()
            datas = cursor.fetchall()
            ok = True
        except pymysql.Error as ex:
            self.mysqlConn.rollback()
            err = str(ex)
            return ok, datas, err
        except Exception as ex:
            self.mysqlConn.rollback()
            err = str(ex)
            return ok, datas, err
        finally:
            cursor.close()
        return ok, datas, err

    def Execute(self, sqlStr: str) -> Tuple[bool, str]:
        """Execute

        Args:
            sqlStr (str): asa

        Returns:
            ok (bool): True
            err (str): err msg
        """
        ok = False
        err = ""
        self.mysqlConn.ping(reconnect=True)
        cursor = self.mysqlConn.cursor()
        try:
            cursor.execute(sqlStr)
            self.mysqlConn.commit()
            ok = True
        except pymysql.Error as ex:
            self.mysqlConn.rollback()
            err = str(ex)
            return ok, err
        except Exception as ex:
            self.mysqlConn.rollback()
            err = str(ex)
            return ok, err
        finally:
            cursor.close()
        return ok, err

    def GetConn(self):
        """GetConn

        使用场景是查询数据量太大的时候，使用逐个读取的方式-fetchone，而不是fetchall
        节省内存。或者其他更多的自由使用场景. 使用完之后记得手动关闭此Conn: conn.close()
        还要手动关闭游标 cursor

        Args:
            None

        Returns:
            self.mysqlConn (Connection): asd
        """
        return self.mysqlConn

    def CloseConn(self) -> Tuple[bool, str]:
        """CloseConn

        数据库使用完之后记得手动关闭连接，如果这个conn已经关闭的话，就会报错

        Args:
            None

        Returns:
            ok (bool): True
            err (str): msg
        """
        ok = False
        err = ""
        try:
            self.mysqlConn.close()
            ok = True
        except Exception as ex:
            err = str(ex)
            return ok, err
        return ok, err

    def PingConn(self) -> Tuple[bool, str]:
        ok = False
        err = ""
        try:
            self.mysqlConn.ping(reconnect=False)
            ok = True
        except Exception as ex:
            err = str(ex)
        return ok, err

    def Reconnect(self) -> Tuple[bool, str]:
        ok = False
        err = ""
        try:
            self.mysqlConn.connect()
            ok, err = self.PingConn()
        except Exception as ex:
            err = str(ex)
        return ok, err

    def getInsertSql(self, tableName: str, data: Dict):
        keyList = []
        valueList = []
        for key, value in data.items():
            keyList.append(key)
            if type(value) is str:
                value = (
                    value.replace("\\", "\\\\")
                    .replace("\b", "\\b")
                    .replace("\n", "\\n")
                    .replace("\r", "\\r")
                    .replace("\t", "\\t")
                    .replace("\\x1A", "\\Z")
                    .replace("\\x00", "\\0")
                    .replace("'", "\\'")
                    .replace('"', '\\"')
                )
                valueList.append(f"'{value}'")
            else:
                valueList.append(str(value))
        keyStr = ",".join(keyList)
        valueStr = ",".join(valueList)
        insertSql = f"INSERT INTO {tableName} ({keyStr}) VALUES ({valueStr})"
        return insertSql

    def getUpdateSql(self, data: Dict):
        update_sql_list = []
        for key in data.keys():
            update_sql_list.append(f"{key}=VALUES({key})")
        updateSql = " ON DUPLICATE KEY UPDATE " + ",".join(update_sql_list)
        return updateSql

    def InsertDatas(
        self,
        tableName: str,
        datas: List[Dict],
        update: bool = False,
    ) -> Tuple[bool, List[Dict]]:
        """InsertDatas

        批量插入数据 实际底层不是批量commit的

        Args:
            tableName (str): s
            datas (Tuple[Dict]): s
            update (bool=False): s

        Returns:
            ok (bool): s
            res (List(Dict)): s
        """
        ok = False
        res = []
        updateSql = ""
        if update:
            updateSql = self.getUpdateSql(data=datas[0])
        for data in datas:
            insertSql = self.getInsertSql(tableName=tableName, data=data)
            sqlStr = insertSql + updateSql
            ok, err = self.Execute(sqlStr=sqlStr)
            if not ok:
                errMap = {
                    "sqlStr": sqlStr,
                    "errMsg": err,
                }
                res.append(errMap)
        if len(res) == 0:
            ok = True
        return ok, res
