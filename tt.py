import pypandoc
DESC = pypandoc.convert('README.md', 'rst')
DESC = DESC.replace("\r", "")
print(DESC)
