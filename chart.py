#!/usr/bin/env python3
# chart.py
# library to create charts

import cgi
import cgitb
cgitb.enable()

def createchart(lname, name, values):
	
	print('var ' + name + ' = new CanvasJS.Chart("' + name + 'Container",{')
	print('	title:{')
	print('		text: "' + lname + '"')
	print('	},')
	print('	axisX:{')
	print('		gridThickness: 2,')
	print('		interval:5, ')
	print('		labelAngle: -45')
	print('	},')
	print('	axisY:{')
	print('		valueFormatString:  "#,##0.####",')
	print('		suffix: "%",')
	print('	},')
	print('	data: [{')
	print('		type: "line",')
	print('		dataPoints: [')
	for x in range(len(values)):
		print('		{ x: new Date(2016,0,1,6,30+' + str(x) + ',0,0), y: ' + str(values[x]) + ' },')
#	print('		{ x: new Date(2016,0,1,6,30+0,0,0), y: 1 },')
#	print('		{ x: new Date(2016,0,1,6,30+1,0,0), y: 2 },')
#	print('		{ x: new Date(2016,0,1,6,30+2,0,0), y: 3 },')
	print('		]')
	print('	}]')
	print('});')
	print('' + name + '.render();')
	print('' + name + ' = {};')
	
def displaychart(name):
	
	print('<div id="' + name + 'Container" style="height: 300px; width: 100%;"></div>')
