Currency_Conversion
===================
This ACL script converts currencies based on today's exchange rates.

The EXECUTE command calls a Python program that parses an RSS feed to get the exchange rates. The Python program creates an ACL script than contains acomputed field that converts to the desired currency.

Prerequisites
=============
 * Python - http://www.python.org/
 * feedparser Python Library - https://pypi.python.org/pypi/feedparser/
