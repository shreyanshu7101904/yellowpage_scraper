from lib.DataFliter import DataFilter




if __name__ == '__main__':
    ob = DataFilter("yellowpages_info", "level_one", "Final_Data")
    ob.pullAndPushData()