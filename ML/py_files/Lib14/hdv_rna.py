
import pandas as pd

# This decorator configuration allow for mutability within objects
# as opposed to @staticmethod. However, @staticmethod should run faster.
def classproperty(func):
   return classmethod(property(func))

class hdv_rna