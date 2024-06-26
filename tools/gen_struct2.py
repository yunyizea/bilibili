# -*- coding: utf-8 -*
import os
import sys


def snake_to_camel(snake_str):
    parts = snake_str.split('_')
    return ''.join(word.title() for word in parts)


head_mapping = {
	'参数名': 'name',
	'字段': 'name',
	'字段名': 'name',
	'项': 'name',
	'类型': 'type',
	'内容': 'content',
	'必要性': 'notnull',
	'备注': 'comment',
}


if __name__ == '__main__':
	while True:
		head = []
		lines = []
		# 从控制台读取输入
		print('请输入Markdown表格，在最后一行之后输入ok表示结束：（退出请输入exit）'.decode("utf-8").encode(sys.stdin.encoding))
		while True:
			line = raw_input()
			line = line.decode(sys.stdin.encoding).encode("utf-8")
			if not line:
				continue
			if line.strip() == 'exit':
				sys.exit(0)
			if line.strip() == 'ok':
				break
			line = line.replace('`', '')
			if len(head) == 0:
				head = line.split('|')
				for i in range(len(head)):
					v = head[i].strip()
					head[i] = head_mapping.get(v, '')
			else:
				l = line.split('|')
				if len(l) != len(head):
					print('列数不一致，无法解析')
					sys.exit(0)
				m = {}
				for i in range(len(l)):
					v = l[i].strip()
					if v.startswith('---'):
						m = None
						break
					m[head[i]] = v
				if not m:
					continue
				lines.append(m)
		# 生成结构体
		print('type T struct {')
		for m in lines:
			name = snake_to_camel(m['name'])
			if m['type'] == 'num':
				m['type'] = 'int'
			elif m['type'] == 'str':
				m['type'] = 'string'
			elif m['type'] == 'bool':
				pass
			elif m['type'] in ('array', 'Array', 'list', 'List', 'array(obj)', 'Array(obj)', 'list(obj)', 'List(obj)'):
				m['type'] = '[]' + (name if not name.endswith('s') else name[:-1])
			elif m['type'] in ('array(num)', 'Array(num)', 'list(num)', 'List(num)'):
				m['type'] = '[]int'
			elif m['type'] in ('array(str)', 'Array(str)', 'list(str)', 'List(str)'):
				m['type'] = '[]string'
			elif m['type'] in ('array(bool)', 'Array(bool)', 'list(bool)', 'List(bool)'):
				m['type'] = '[]bool'
			elif m['type'] == 'obj':
				m['type'] = name
			if m.get('notnull', '必要') in ('必要', '必须', '必填', '√'):
				m['notnull'] = '"'
			else:
				m['notnull'] = ',omitempty" request:"query,omitempty"'
			content = m.get('content', '')
			comment = m.get('comment', '')
			if content or comment:
				sep = '。' if content and comment else ''
				comment = ' // %s%s%s' % (content, sep, comment)
				comment = comment.replace('<br>', '。').replace('<br/>', '。').replace('<br />', '。').replace('\\', '')
				comment = comment.decode("utf-8").encode(sys.stdin.encoding)
			print('\t%s %s `json:"%s%s`%s' % (name, m['type'], m['name'], m['notnull'], comment))
		print('}')

