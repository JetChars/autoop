print "hello"

file = open("/Users/JetChars/github/autoop/dashboard/tools/hadoop_server_input.csv").readlines()
print '''<thead>
  <tr>'''
for item in file[0].split(','):
	print "    <th>",item.strip(),"</th>"
print '''  </tr>
</thead>'''
print "<tbody>"
for eachline in file[1:]:
	print "  <tr>"
	for item in eachline.split(','):
		print "    <th>",item.strip(),"</th>"
	print "  </tr>"

print "</tbody>"