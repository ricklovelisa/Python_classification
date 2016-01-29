#!/usr/bin/python
#coding: utf-8

from function_module import FunctionModule

class ImportData(object):

    """import stock codes into MySQL


    Attributes:
        no.
    """

    def __init__(self):

        """initiate object


        Attributes:
            no.
        """
        self.func = FunctionModule()
        self.dir = 'D:/stock_list.csv'

    def main(self):

        """main function


        Attributes:
            no.
        """
        file = self.func.get_data_from_text(self.dir, 'r', 'utf8')
        for line in file:
            sql = "INSERT INTO stock_codes (stock_code, stock_name, industry_1_id, industry_1_name, " \
                  "industry_2_id, industry_2_name) VALUES ('%s', '%s','%s', '%s', '%s', '%s')" \
                  % (line['stock_code'], line['stock_name'], line['industry_1_id'],
                     line['industry_1_name'], line['industry_2_id'], line['industry_2_name'])
            self.func.insert_into_mysql(sql)

if __name__ == '__main__':
    Import = ImportData()
    Import.main()

