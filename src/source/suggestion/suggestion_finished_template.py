# -*- coding: utf-8 -*-
from API import BASE_URL,singleSuggestion
from nicegui import ui
from source.webAPI.suggestion import suggestion_single

from source.layout.page_layout import PageLayout

class SuggestionPage(PageLayout):
    def __init__(self,id):
        super().__init__(f'历史记录-{id}-'+'{}')
        self.id = id
        self.res=suggestion_single(singleSuggestion(),id)
        match self.res['data'][0]['sugg_feedback']:
            case 1:
                self.feedback=='非常满意'
            case 2:
                self.feedback=='满意'
            case 3:
                self.feedback=='基本满意'
            case 4:
                self.feedback=='一般'
            case 5:
                self.feedback=='不满意'
            case _:
                self.feedback='未评价'

        if self.res.get('code') == 200 and self.res.get('data'):
            ui.notify(self.res.get('message'), type='info',position='top')
        else:
            ui.notify(self.res.get('message'), type='warning',position='top')
            ui.navigate.to('/suggestion/finished')

    def content(self):
        if self.res.get('data'):
            def preview(res: list):
                with ui.dialog() as dialog,ui.card().style('width:80vh;height:auto;'):
                    if res!=None:
                        with ui.carousel(animated=True, arrows=True, navigation=True).style('width: 60%;height:auto;align-self:center'):
                            for i in res:
                                with ui.carousel_slide().classes('p-0'):
                                    ui.image(BASE_URL[:-1]+i['sugg_media'])
                        ui.button('关闭').on_click(lambda:dialog.close())
                dialog.open()

            columns = [
                {'name': 'name', 'label': '类型', 'field': 'name', 'required': True, 'align': 'left'},
                {'name': 'inf', 'label': '信息', 'field': 'inf','align': 'left'},
            ]
            rows = [
                {'name': '提出人：', 'inf': self.res['data'][0]['sugg_name']},
                {'name': '提出地点：', 'inf': self.res['data'][0]['sugg_site']},
                {'name': '联系电话：', 'inf': self.res['data'][0]['sugg_user_tele']},
                {'name': '提交时间：', 'inf': self.res['data'][0]["sugg_sub_time"].split('T')[0]},
                {'name': '建议内容：', 'inf': self.res['data'][0]['sugg_text']},
                {'name': '用户评价', 'inf': self.feedback},
            ]
            row2 = [
                {'name': '回复人：', 'inf': self.res['data'][0]['sugg_staff_name']},
                {'name': '回复电话：', 'inf': self.res['data'][0]['sugg_staff_tele']},
                {'name': '回复时间：', 'inf': self.res['data'][0]['sugg_handle_time'][:10]},
                {'name': '回复内容：', 'inf': self.res['data'][0]['sugg_content']},
                {'name': '回访总结', 'inf': self.res['data'][0]['sugg_summary']}
            ]
            with ui.card().style('width:100%'):
                with ui.column().style("width:100%;flex-direction:column;align-self:flex-start;height:100%"):
                    table=ui.table(columns=columns, rows=rows, row_key='name').style('width:100%').style('font-size: 1.0rem;')
                    if self.res['data'][0]["suggestionmedia_set"]:
                        with ui.row():
                            ui.label('附件图片：').style('font-size:1.4rem;height:30px;')
                            ui.button("点击查看",on_click=lambda:preview(self.res['data'][0]["suggestionmedia_set"])).style('width:100px;')
                    ui.table(columns=columns,rows=row2,row_key='name').style('width:100%').style('font-size: 1.0rem;')

def suggestion_num_finished_ui(id):
    SuggestionPage(id).show_layout()