from API import replycomplaint
from nicegui import ui
from source.layout.head import header
from source.webAPI.complaint import complaint_single,reply_complaint
# from niceguiToolkit.layout import inject_layout_tool
# inject_layout_tool()

def __handle_reply(getid,content,way,name,tel,status):
    url = replycomplaint()
    res = reply_complaint(url,getid,content,way,name,tel,status)
    if res['code']==200:
        ui.notify(res['msg'],position='top',type='info')
        ui.timer(1.0,lambda:ui.navigate.to('/complaint/untreated'))
    else:
        ui.notify(res['msg'],position='top',type='warning')

def complaint_num(id):
    try:
        res = complaint_single(replycomplaint(),id)
    except:
        ui.notify('网络错误',position='top',type='warning')
        ui.navigate.to('/complaint/untreated')
    with ui.column().style("font-size:1.5rem;width:100%;height:auto"):
        header()
        if res['code']==200 and res['data'][0]['comp_status']==False:
            columns = [
                {'name': 'name', 'label': '类型', 'field': 'name', 'required': True, 'align': 'left'},
                {'name': 'inf', 'label': '信息', 'field': 'inf','align': 'left'},
            ]
            rows = [
                {'name': '建议人：', 'inf': res['data'][0]['comp_name']},
                {'name': '建议地点：', 'inf': res['data'][0]['comp_site']},
                {'name': '联系电话：', 'inf': res['data'][0]['comp_user_tele']},
                {'name': '提交时间：', 'inf': res['data'][0]["comp_sub_time"].split('T')[0]},
                {'name': '建议内容：', 'inf': res['data'][0]['comp_text']},
            ]
            ui.table(columns=columns, rows=rows, row_key='name').style('width:100%;font-size:1.4rem')
            if res['data'][0]["complaintmedia_set"]:
                ui.label('附件图片：')
                with ui.row():
                    for i in res['data'][0]["complaintmedia_set"]:
                        ui.image(i["comp_media"]).style('weight:auto;height:200px')
            with ui.card():
                with ui.row():
                    name=ui.input(label='回复人',validation={'人名不能为空': lambda value: len(value) >= 0})
                    tele=ui.input(label='联系电话',validation={'请正确填写电话号码': lambda value: len(value) == 11 and value.isdigit()})
                    way=ui.input(label='解决方式',validation={'解决方式不能为空': lambda value: len(value) >= 0})
                    switch = ui.switch('是否解决', value=True)
            with ui.card().style("width:100%"):
                content=ui.textarea(label='回复内容',validation={'回复内容不能为空': lambda value: len(value) >= 0}).style('width:100%')
            with ui.row():
                ui.button('提交',on_click=lambda: __handle_reply(id,content.value,way.value,name.value,tele.value,switch.value))
        else:
            ui.notify(res['message'],position='top',type='warning')
            ui.navigate.to('/complaint/untreated')