#!/usr/bin/env python
import refine

r = refine.Refine()
p = r.new_project("dates.csv")
p.apply_operations("operations.json")
print(p.export_rows())
p.delete_project()
