from search.models import BookQuery, Result
BookQuery.objects.all()
q = BookQuery(title='Oi', isbn='3423434', author='Joao da Silva', pages=123, publisher='DaMae', language='PTBR', coverType='capa dura')
q = BookQuery(title='Crime e Castigo', author='Dostoievsky', isbn='324893764395', publisher='Intrinseca', language='Portugues')