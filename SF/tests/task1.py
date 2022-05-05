import lxml.html
from lxml import etree
html = ''' <html>
 <head> <title> Some title </title> </head>
 <body>
  <tag1> some text
     <tag2> MY TEXT </tag2>
   </tag1>
 </body>
</html>
'''

tree = lxml.html.document_fromstring(html)


title = tree.xpath('/html/body/tag1/tag2/text()')

print(title)
