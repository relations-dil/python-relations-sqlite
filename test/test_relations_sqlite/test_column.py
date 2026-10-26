import unittest
import unittest.mock

import relations
from relations_sqlite import *


class TestCOLUMN(unittest.TestCase):

    maxDiff = None

    def test___init__(self):

        field = relations.Field(bool, name="flag", default=True)
        ddl = COLUMN(field.define())
        self.assertEqual(ddl.migration["default"], 1)

    def test_generate(self):

        field = relations.Field(bool, name="flag")
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, "`flag` INTEGER")
        self.assertEqual(ddl.args, [])

        field = relations.Field(int, name="id")
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, "`id` INTEGER")
        self.assertEqual(ddl.args, [])

        field = relations.Field(int, name="id", auto=True)
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, "`id` INTEGER PRIMARY KEY")
        self.assertEqual(ddl.args, [])

        field = relations.Field(float, "price", store="_price", default=1.25, none=False)
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """`_price` REAL NOT NULL DEFAULT 1.25""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(str, "name", store="_name", default="Willy", none=False)
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """`_name` TEXT NOT NULL DEFAULT 'Willy'""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(dict, "data", store="_data", default={"a": 1}, none=False)
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """`_data` TEXT NOT NULL DEFAULT '{"a": 1}'""")
        self.assertEqual(ddl.args, [])

        ddl = COLUMN(store="data__a__0___1____2_____3", kind="str")

        ddl.generate()
        self.assertEqual(ddl.sql, """`data__a__0___1____2_____3` TEXT AS (json_extract(`data`,'$.a[0][-1]."2"."-3"'))""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(bool, name="flag")
        ddl = COLUMN(field.define(), added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD `flag` INTEGER""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(int, name="id")
        ddl = COLUMN(field.define(), added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD `id` INTEGER""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(float, "price", store="_price", default=1.25, none=False)
        ddl = COLUMN(field.define(), added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD `_price` REAL NOT NULL DEFAULT 1.25""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(str, "name", store="_name", default="Willy", none=False)
        ddl = COLUMN(field.define(), added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD `_name` TEXT NOT NULL DEFAULT 'Willy'""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(dict, "data", store="_data", default={"a": 1}, none=False)
        ddl = COLUMN(field.define(), added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD `_data` TEXT NOT NULL DEFAULT '{"a": 1}'""")
        self.assertEqual(ddl.args, [])

        ddl = COLUMN(store="data__a__0___1____2_____3", kind="str", added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD `data__a__0___1____2_____3` TEXT AS (json_extract(`data`,'$.a[0][-1]."2"."-3"'))""")
        self.assertEqual(ddl.args, [])

        # a string with a length can't be longer, as SQLite doesn't enforce the length of a type

        field = relations.Field(str, "name", store="_name", default="Willy", none=False, length=64)
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """`_name` TEXT NOT NULL DEFAULT 'Willy' CHECK (length(`_name`) <= 64)""")
        self.assertEqual(ddl.args, [])

        ddl = COLUMN(field.define(), added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD `_name` TEXT NOT NULL DEFAULT 'Willy' CHECK (length(`_name`) <= 64)""")
        self.assertEqual(ddl.args, [])

        # no length, no check, and neither for an extracted column or an auto one

        field = relations.Field(str, name="name", store="_name", none=False)
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """`_name` TEXT NOT NULL""")
        self.assertEqual(ddl.args, [])

        ddl = COLUMN(store="data__a", kind="str", length=64)

        ddl.generate()
        self.assertEqual(ddl.sql, """`data__a` TEXT AS (json_extract(`data`,'$.a'))""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(str, name="id", auto=True, length=64)
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """`id` INTEGER PRIMARY KEY""")
        self.assertEqual(ddl.args, [])
