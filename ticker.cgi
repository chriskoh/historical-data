#!/usr/bin/env python3

import cgi
import cgitb
cgitb.enable()

print("Content-type: text/html")
print()
print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
print("<!DOCTYPE html>")
print("<html>")
print("<head>")
print("<title>Stock Data</title>")
print("<body>")
print("<h1>Intraday Data Analysis</h1>")
print("<form action='/cgi-bin/historical-data/percentchange.py' method='post'>")
print("Ticker: <input type='text' name='ticker'><br>")
print("<input type='submit' value='Search'>")
print("<form>")
print("</body>")
print("</html>")
