from scrap_sources import DataParsing
import dbtools
import type_definition

dbtools.server.start()

dp = DataParsing()
dp.scrap_source0()
dp.scrap_source1()
dp.scrap_source2()
dp.scrap_source3()
dbtools.set_geocode()
type_definition.define_types()

dbtools.server.stop()