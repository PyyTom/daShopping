import datetime,sqlite3,os
meses= {'ENERO':31, 'FEBRERO':28, 'MARZO':31, 'ABRIL':30, 'MAYO':31, 'JUNO':30, 'JULIO':31, 'AGOSTO':31, 'SEPTIEMBRE':30, 'OCTUBRE':31, 'NOVIEMBRE':30,'DICIEMBRE':31}
if os.path.isdir('ARCHIVO')==False:os.mkdir('ARCHIVO')
db=sqlite3.connect('ARCHIVO/'+str(datetime.datetime.today().year)+'.db')
db.execute('create table if not exists COMPRAS(MES,DIA,ARTICULO,CANTITAD integer,PARTIAL float,TOTAL float)')
db.close()
from flet import *
def main(page:Page):
    def activa_meses(e):
        d_mes.disabled=False
        db = sqlite3.connect('ARCHIVO/' + d_año.value + '.db')
        try:r_tot.controls = [Text('TOTAL DE '+ d_año.value + ': €.' + str(round(db.execute('select SUM(TOTAL) from COMPRAS').fetchone()[0], 2)), size=30)]
        except:pass
        db.close()
        page.update()
    def muestra_mes(e):
        t_articulo.disabled, t_precio.disabled, t_cantitad.disabled, b_guarda.disabled = True, True, True, True
        d_dia.value, t_articulo.value, t_precio.value, t_cantitad.value = '', '', '', ''
        d_dia.disabled=False
        d_dia.options=[dropdown.Option(str(dia)) for dia in range(1,meses[d_mes.value]+1)]
        try:
            c_datos.controls=[Row([Text('DIA',width=100),Text('ARTICULO',width=200),Text('CANTITAD',width=100),Text('PRECIO',width=100),Text('TOTAL',width=100)])]
            db = sqlite3.connect('ARCHIVO/' + d_año.value + '.db')
            for dia in db.execute('select * from COMPRAS where MES=? order by DIA', (d_mes.value,)).fetchall():c_datos.controls.append(Container(content=Row([Text(dia[1],width=100),Text(str(dia[2]),width=200),Text(str(dia[3]),width=100),Text(str(dia[4]),width=100),Text(str(dia[5]),width=100)]),on_click=borra))
            r_tot.controls=[Text('TOTAL DE '+d_mes.value+' '+d_año.value+': €.'+str(round(db.execute('select SUM(TOTAL) from COMPRAS where MES=?',(d_mes.value,)).fetchone()[0],2)),size=30)]
            db.close()
        except:c_datos.controls,r_tot.controls=[],[]
        page.update()
    def muestra_dia(e):
        t_articulo.disabled,t_precio.disabled,t_cantitad.disabled,b_guarda.disabled=False,False,False,False
        try:
            c_datos.controls=[Row([Text('ARTICULO',width=200),Text('CANTITAD',width=100),Text('PRECIO',width=100),Text('TOTAL',width=100)])]
            db = sqlite3.connect('ARCHIVO/' + d_año.value + '.db')
            for dia in db.execute('select * from COMPRAS where MES=? and DIA=? order by DIA', (d_mes.value,d_dia.value,)).fetchall():c_datos.controls.append(Container(content=Row([Text(str(dia[2]),width=200),Text(str(dia[3]),width=100),Text(str(dia[4]),width=100),Text(str(dia[5]),width=100)]),on_click=borra))
            r_tot.controls=[Text('TOTAL DE '+d_dia.value+' '+d_mes.value+' '+d_año.value+': €.'+str(round(db.execute('select SUM(TOTAL) from COMPRAS where MES=? and DIA=?',(d_mes.value,d_dia.value,)).fetchone()[0],2)),size=30)]
            db.close()
        except:c_datos.controls,r_tot.controls=[],[]
        page.update()
    def guarda(e):
        if t_articulo.value=='' or t_precio.value=='' or t_cantitad.value=='':alerta.title=Text('FALTA ALGO')
        else:
            if t_cantitad.value==1:precio=t_precio.value
            else:precio=float(t_precio.value)*int(t_cantitad.value)
            db=sqlite3.connect('ARCHIVO/'+d_año.value+'.db')
            db.execute('insert into COMPRAS values(?,?,?,?,?,?)',(d_mes.value,d_dia.value,(t_articulo.value).upper(),t_cantitad.value,t_precio.value,round(precio,2)))
            db.commit()
            muestra_mes('')
            alerta.title=Text('EXITO')
        page.update()
    def borra(e):
        l=[]
        for i in e.control.content.controls:l.append(i.value)
        if len(l)==5:dia=l[0]
        else:dia=d_dia.value
        db=sqlite3.connect('ARCHIVO/'+d_año.value+'.db')
        db.execute('delete from COMPRAS where MES=? and DIA=? and ARTICULO=? and CANTITAD=?',(d_mes.value,dia,l[-4],l[-3],))
        db.commit()
        muestra_mes('')
        alerta.title = Text('EXITO')
        page.update()
    page.window_full_screen=True
    page.theme_mode='LIGHT'
    alerta=AlertDialog(title=Text(''))
    d_año=Dropdown(label='AÑO',options=[dropdown.Option(año[:-3]) for año in os.listdir('ARCHIVO')],on_change=activa_meses,width=100)
    d_mes=Dropdown(label='MES',options=[dropdown.Option(mes) for mes in meses],on_change=muestra_mes,width=150,disabled=True)
    d_dia=Dropdown(label='DIA',on_change=muestra_dia,disabled=True,width=80)
    t_articulo=TextField(label='ARTICULO',disabled=True)
    t_precio=TextField(label='PRECIO',disabled=True)
    t_cantitad=TextField(label='CANTITAD',disabled=True)
    b_guarda=ElevatedButton('GUARDA',disabled=True,on_click=guarda)
    c_datos=Column(width=600,height=600,scroll=ScrollMode.ALWAYS)
    c_edit=Column([t_articulo,t_precio,t_cantitad,b_guarda],height=600,scroll=ScrollMode.ALWAYS)
    r_tot=Row(alignment=MainAxisAlignment.CENTER)
    page.add(alerta,
             Row([IconButton(icon=icons.EXIT_TO_APP,icon_size=50,icon_color='red',on_click=lambda _:page.window_destroy())],alignment=MainAxisAlignment.END),
             Row([Text(width=250),d_año,d_mes,d_dia]),
             Row([Text(width=1000),Text('EDITAR',size=20)]),
             Row([c_datos,VerticalDivider(),c_edit],alignment=MainAxisAlignment.CENTER,height=600),Divider(),r_tot)
app(target=main)