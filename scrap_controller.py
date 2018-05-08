from scrap_s1 import DataParsing
import dbtools

dp = DataParsing()
dp.scrap_source0()
dp.scrap_source1()
dp.scrap_source2()
dp.scrap_source3()
dbtools.set_geocode()