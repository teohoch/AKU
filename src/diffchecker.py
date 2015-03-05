__author__ = 'teohoch'

import difflib



def show_differences(newfilename, oldfilename):
	style = '<style type="text/css">' \
			'	table.diff {font-family:Courier; border:medium;}' \
			'	.diff_header {background-color:#e0e0e0}' \
			'	td.diff_header {text-align:right}' \
			'	.diff_next {background-color:#c0c0c0}' \
			'	.diff_add {background-color:#aaffaa}' \
			'	.diff_chg {background-color:#ffff77}' \
			'	.diff_sub {background-color:#ffaaaa}' \
			'</style>'
	legend = '<table class="diff" summary="Legends">' \
			 '        <tr> <th colspan="2"> Legends </th> </tr>' \
			 '        <tr> <td> <table border="" summary="Colors">' \
			 '                      <tr><th> Colors </th> </tr>' \
			 '                      <tr><td class="diff_add">&nbsp;Added&nbsp;</td></tr>' \
			 '                      <tr><td class="diff_chg">Changed</td> </tr>' \
			 '	<tr><td class="diff_sub">Deleted</td> </tr>' \
			 '                  </table></td>' \
			 '             <td> <table border="" summary="Links">' \
			 '                      <tr><th colspan="2"> Links </th> </tr>' \
			 '                      <tr><td>(f)irst change</td> </tr>' \
			 '                      <tr><td>(n)ext change</td> </tr>' \
			 '                      <tr><td>(t)op</td> </tr>' \
			 '                  </table></td> </tr>' \
			 '    </table>'
	new_file = open(newfilename, 'r')
	old_file = open(oldfilename, 'r')
	diff = difflib.HtmlDiff(wrapcolumn=90).make_table(fromlines=old_file.readlines(),tolines=new_file.readlines(),fromdesc=oldfilename,todesc=newfilename,context=True, numlines=1)

	return style + diff + legend



if __name__ == '__main__':

	print show_differences('/home/teohoch/Desktop/ColdCart8-0-new.xml','/home/teohoch/Desktop/ColdCart8-0.xml')