from scrap_sources import DataParsing
import dbtools
import type_definition
from datetime import datetime

# while True:
#     now = datetime.now()
#     if now.hour == 10 and now.minute == 0 and now.second == 0:
#
#         dbtools.server.start()
#
#         dp = DataParsing()
#         dp.scrap_source0()
#         dp.scrap_source1()
#         dp.scrap_source2()
#         dp.scrap_source3()
#         dbtools.set_geocode()
#         type_definition.define_types()
#
#         dbtools.server.stop()

dbtools.server.start()

dp = DataParsing()
dp.scrap_source0()
dp.scrap_source1()
dp.scrap_source2()
#dp.scrap_source3()
dp.scrap_source4()
dbtools.set_geocode()
dbtools.set_country_geocode()
type_definition.define_types()

dbtools.server.stop()