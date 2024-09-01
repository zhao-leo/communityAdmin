# -*- coding: utf-8 -*-
from API import replysuggestion,BASE_URL,suggestionhandle
from nicegui import ui
from source.webAPI.suggestion import suggestion_single,handle_suggestion_treat

from source.layout.page_layout import PageLayout

class SuggestionPage(PageLayout):
    def __init__(self,id):
        super().__init__(f'待回访建议-{id}-'+'{}')
        self.id = id
        self.res=suggestion_single(replysuggestion(),id)
        if self.res.get('code') == 200 and self.res.get('data'):
            ui.notify(self.res.get('message'), type='info',position='top')
        else:
            ui.notify(self.res.get('message'), type='warning',position='top')
            ui.navigate.to('/suggestion/untreated')

    def content(self):
        if self.res.get('data'):
            def __handle_reply(doc_id):
                res=handle_suggestion_treat(suggestionhandle(),doc_id)
                if res.get('code') == 200:
                    ui.notify(res.get('message'), type='info',position='top')
                    ui.navigate.to('/suggestion/treated')
                else:
                    ui.notify(res.get('message'), type='warning',position='top')
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
                {'name': '处理状态：', 'inf': '需要回访' if self.res['data'][0]['sugg_treat'] else '不需要回访','slot': 'row_5'},
            ]
            row2 = [
                {'name': '回复人：', 'inf': self.res['data'][0]['sugg_staff_name']},
                {'name': '回复电话：', 'inf': self.res['data'][0]['sugg_staff_tele']},
                {'name': '回复时间：', 'inf': self.res['data'][0]['sugg_handle_time']},
                {'name': '回复内容：', 'inf': self.res['data'][0]['sugg_content']},
            ]
            with ui.card().style('width:100%'):
                with ui.column().style("width:100%;flex-direction:column;align-self:flex-start;height:100%"):
                    table=ui.table(columns=columns, rows=rows, row_key='name').style('width:100%').style('font-size: 1.0rem;')
                    table.add_slot('body-cell-inf', '''
                    <q-td key="row_5" :props="props">
                        <q-badge :color="props.value == '需要回访' ? 'red' : (props.value == '不需要回访' ? 'green' : 'transparent')" style="font-size: 0.9rem; color: black;">
                            {{ props.value }}
                        </q-badge>
                    </q-td>''')
                    if self.res['data'][0]["suggestionmedia_set"]:
                        ui.label('附件图片：')
                        with ui.row().style('flex-wrap:wrap'):
                            for i in self.res['data'][0]["suggestionmedia_set"]:
                                with ui.column().style('width:400px;height:auto;'):
                                    ui.image(BASE_URL[:-1]+i['sugg_media']).style('object-fit:contain;') # .style('height:200px;width:auto;')
                    ui.table(columns=columns,rows=row2,row_key='name').style('width:100%').style('font-size: 1.0rem;')
                    ui.button('提交',on_click=lambda: __handle_reply(self.id)).style('margin-top:10px;')

def suggestion_num_treat_ui(id):
    SuggestionPage(id).show_layout()