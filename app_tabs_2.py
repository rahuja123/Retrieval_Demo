import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go
import random
from datetime import datetime
from dash.exceptions import PreventUpdate
import re
from camera.retrieval import retrieval
from camera.offline_retrieval import offline_retrieval
import cv2
from plotting.floormap_cross_stickman import floormap_cross_numbers
import base64
import os
from layout.feature_extractor_layout_sets import feature_extractor_layout_sets
from layout.feature_extractor_layout_2 import feature_extractor_layout
from layout.retrieval_run_layout import retrieval_run_layout
import itertools


#path to save the image that you upload on the server.
UPLOAD_DIRECTORY = "static/query"
# external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True
server = app.server

SET1= ["S2-B4b-R-TR","S2-B4b-R-TL","S2-B4b-R-BR","S2-B4b-R-BL","S2-B4b-L-TR","S2-B4b-L-TL","S2-B4b-L-BR","S2-B4b-L-BL"]
SET2= ["S21-B3-L-T", "S21-B3-R-B","S22-B3-L-T", "S22-B3-R-B", "S21-B4-L-T", "S21-B4-R-B","S22-B4-L-T", "S22-B4-R-B"]
SET3= ["S1-B4b-L-BL","S1-B4b-L-BR", "S1-B4b-R-BL","S1-B4b-R-BR","S1-B3b-L-TL","S1-B3b-L-TR", "S1-B3b-R-TL","S1-B3b-R-TR", "S1-B4b-L-TL","S1-B4b-L-TR", "S1-B4b-R-TL","S1-B4b-R-TR","S1-B3b-L-BL","S1-B3b-L-BR", "S1-B3b-R-BL","S1-B3b-R-BR"]
SET4= ["S1-B4b-d-BL"] #change it
global_camera_sets= [SET1, SET2, SET3, SET4]

global_camera_names= ["S2-B4b-L-B","S2-B4b-L-BR","S1-B4b-L-BL","S1-B4b-R-B","S21-B4-T","S22-B4-T"]
cams_map_testing= ["S2-B4b-L-B","S2-B4b-L-BR","S1-B4b-L-BL","S1-B4b-R-B","S21-B4-T","S22-B4-T"]
models_dict={'ResNet50':['ResNet50_Market.pth'],'ResNet101':['ResNet101_Market.pth'],'SE_ResNet50':['SE_ResNet50_Market.pth'],'SE_ResNet101':['SE_ResNet101_Market.pth']}
image_value_list=[]
output_result=[]

count=0

app.layout= html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                html.Div(
                    [
                        html.Div(
                            [
                                html.Img(
                                    src= app.get_asset_url("NTU_Logo.png"), className="logo"
                                ),
                                # html.Img(
                                #     src= app.get_asset_url("rose_lab_logo.png"), className="logo"
                                # )
                            ],className="logo_section"
                        ),

                        html.H1(children=["NTU ReID Demo"]),
                        html.P(
                            """Select feature extractor to run detection code and Retreival run to find the person from a query. """
                        ),

                        dcc.Tabs(id="tabs",
                            className="custom-tabs-container",
                            value='tab1',
                            children=[
                                dcc.Tab(
                                    label='Extractor/Set',
                                    value='tab1',
                                    className='custom-tab',
                                    selected_className='custom-tab--selected',
                                    children=[
                                        html.Div(
                                            className="row",
                                            children=feature_extractor_layout_sets(global_camera_sets, models_dict)
                                        )
                                    ]),

                                dcc.Tab(
                                    label='Extractor/Single',
                                    value='tab2',
                                    className='custom-tab',
                                    selected_className='custom-tab--selected',

                                    children=[
                                        html.Div(
                                            className="row",
                                            children=feature_extractor_layout(global_camera_names, models_dict)
                                        )
                                    ]),

                                dcc.Tab(
                                    label='Retrieval',
                                    value='tab3',
                                    className='custom-tab',
                                    selected_className='custom-tab--selected',
                                    children=[
                                        html.Div(
                                            className="row",
                                            children=retrieval_run_layout(global_camera_sets, models_dict)
                                        )
                                    ]),

                            ]),


                    ], className="four columns div-user-controls"
                ),
                html.Div(
                    [
                        html.Div(
                            id='state_container',
                            style={'display': 'none'},
                            children=[
                                html.Div(id='state_container_{}'.format(x)) for set in global_camera_sets for x in set
                                ]
                        ),
                        html.Br(),
                        dcc.Loading(id="loading-1", children=[html.Div(id="loading-output-1")], type="default"),
                        html.Div(id="camera_outputs", style={'margin-top':50,}),
                        html.Br(),
                        html.Div(id="floormaps_output", className='floormaps_output'),
                        html.Br(),
                        html.Br(),
                        html.Div(id="experimental_section"),

                    ], className="eight columns div-for-charts bg-grey"
                )

            ]

        )


    ]
)

@app.callback(
    Output('network_weight_dropdown', 'options'),
    [Input('network_dropdown', 'value')])
def update_weight_dropdown(name):
    return [{'label': i, 'value': i} for i in models_dict[name]]

@app.callback(
    Output('network_weight_dropdown_sets', 'options'),
    [Input('network_dropdown_sets', 'value')])
def update_weight_dropdown(name):
    return [{'label': i, 'value': i} for i in models_dict[name]]


@app.callback(
    Output('network_weight_dropdown_reid', 'options'),
    [Input('network_dropdown_reid', 'value')])
def update_weight_dropdown(name):
    return [{'label': i, 'value': i} for i in models_dict[name]]





@app.callback(
    Output('camera_run_result_run', 'children'),
    [Input('run_button', 'n_clicks')],
    [State('network_dropdown','value'),
     State('network_weight_dropdown', 'value'),
     State('camera_name_dropdown_1', 'value'),
     State('devices_dropdown_1','value')]
)
def run_camera_run(n_clicks, reid_model, reid_weight,cam_name, reid_device):

        if n_clicks is None:
            raise PreventUpdate
        else:
            if 'ALL' in cam_name:
                cam_name= global_camera_names

            from camera.camera_run_2 import Camera_Process
            globals()['p'] = Camera_Process(cam_list=cam_name, rtsp=True, reid_model=reid_model,reid_weight=reid_weight, reid_device=reid_device)
            p.start()

            # camera_run(cam_name=cam_name, rtsp=False, skip_frame=10,reid_model=reid_model,reid_weight=reid_weight, reid_device=reid_device)
            # print("Done Donaaa Done")
            # from camera.camera_run import camera_run
            # camera_run(cam_name=cam_name, rtsp=False, skip_frame=10,reid_model=reid_model,reid_weight=reid_weight, reid_device=reid_device)
            # print("Done Donaaa Done")
            # return [html.P("Done!")]




@app.callback(
    Output('camera_run_result_stop', 'children'),
    [Input('stop_button', 'n_clicks')],
)
def stop_camera_run(n_clicks):

        if n_clicks is None:
            raise PreventUpdate
        else:
            global p
            p.stop()


@app.callback(
    Output('camera_run_result_1_sets', 'children'),
    [Input('camera_run_1_sets', 'n_clicks')],
    [State('network_dropdown_sets','value'),
     State('network_weight_dropdown_sets', 'value'),
     State('camera_name_dropdown_1_sets', 'value'),
     State('devices_dropdown_1_sets','value')]
)
def run_camera_run_sets(n_clicks, reid_model, reid_weight,cam_name, reid_device):

    if n_clicks is None:
        raise PreventUpdate
    else:
        # print("working1")
        if 'ALL' in cam_name:
            cam_name= global_camera_sets[0]

        from camera.camera_run_2 import Camera_Process
        globals()['p1'] = Camera_Process(cam_list=cam_name, rtsp=True, reid_model=reid_model,reid_weight=reid_weight, reid_device=reid_device)
        p1.start()


@app.callback(
    Output('camera_stop_result_1_sets', 'children'),
    [Input('camera_stop_1_sets', 'n_clicks')],
)
def stop_camera_run_sets(n_clicks):

        if n_clicks is None:
            raise PreventUpdate
        else:
            print("stopped")
            global p1
            p1.stop()



@app.callback(
    Output('camera_run_result_2_sets', 'children'),
    [Input('camera_run_2_sets', 'n_clicks')],
    [State('network_dropdown_sets','value'),
     State('network_weight_dropdown_sets', 'value'),
     State('camera_name_dropdown_2_sets', 'value'),
     State('devices_dropdown_2_sets','value')]
)
def run_camera_run_sets(n_clicks, reid_model, reid_weight,cam_name, reid_device):

    if n_clicks is None:
        raise PreventUpdate
    else:
        # print("working2")
        if 'ALL' in cam_name:
            cam_name= global_camera_sets[1]

        from camera.camera_run_2 import Camera_Process
        globals()['p2'] = Camera_Process(cam_list=cam_name, rtsp=True, reid_model=reid_model,reid_weight=reid_weight, reid_device=reid_device)
        p2.start()

@app.callback(
    Output('camera_stop_result_2_sets', 'children'),
    [Input('camera_stop_2_sets', 'n_clicks')],
)
def stop_camera_run_sets(n_clicks):

        if n_clicks is None:
            raise PreventUpdate
        else:

            print("stopped")
            global p2
            p2.stop()


@app.callback(
    Output('camera_run_result_3_sets', 'children'),
    [Input('camera_run_3_sets', 'n_clicks')],
    [State('network_dropdown_sets','value'),
     State('network_weight_dropdown_sets', 'value'),
     State('camera_name_dropdown_3_sets', 'value'),
     State('devices_dropdown_3_sets','value')]
)
def run_camera_run_sets(n_clicks, reid_model, reid_weight,cam_name, reid_device):

    if n_clicks is None:
        raise PreventUpdate
    else:
        # print("working3")
        if 'ALL' in cam_name:
            cam_name= global_camera_sets[2]

        from camera.camera_run_2 import Camera_Process
        globals()['p3'] = Camera_Process(cam_list=cam_name, rtsp=True, reid_model=reid_model,reid_weight=reid_weight, reid_device=reid_device)
        p3.start()


@app.callback(
    Output('camera_stop_result_3_sets', 'children'),
    [Input('camera_stop_3_sets', 'n_clicks')],
)
def stop_camera_run_sets(n_clicks):

        if n_clicks is None:
            raise PreventUpdate
        else:
            print("stopped")
            global p3
            p3.stop()

@app.callback(
    Output('camera_run_result_4_sets', 'children'),
    [Input('camera_run_4_sets', 'n_clicks')],
    [State('network_dropdown_sets','value'),
     State('network_weight_dropdown_sets', 'value'),
     State('camera_name_dropdown_4_sets', 'value'),
     State('devices_dropdown_4_sets','value')]
)
def run_camera_run_sets(n_clicks, reid_model, reid_weight,cam_name, reid_device):

    if n_clicks is None:
        raise PreventUpdate
    else:
        # print("working3")
        if 'ALL' in cam_name:
            cam_name= global_camera_sets[2]

        from camera.camera_run_2 import Camera_Process
        globals()['p4'] = Camera_Process(cam_list=cam_name, rtsp=True, reid_model=reid_model,reid_weight=reid_weight, reid_device=reid_device)
        p4.start()


@app.callback(
    Output('camera_stop_result_4_sets', 'children'),
    [Input('camera_stop_4_sets', 'n_clicks')],
)
def stop_camera_run_sets(n_clicks):

        if n_clicks is None:
            raise PreventUpdate
        else:
            print("stopped")
            global p4
            p4.stop()




@app.callback(
    Output('camera_run_result_5_sets', 'children'),
    [Input('camera_run_5_sets', 'n_clicks')],
    [State('network_dropdown_sets','value'),
     State('network_weight_dropdown_sets', 'value'),
     State('camera_name_dropdown_5_sets', 'value'),
     State('devices_dropdown_5_sets','value')]
)
def run_camera_run_sets(n_clicks, reid_model, reid_weight,cam_name, reid_device):

    if n_clicks is None:
        raise PreventUpdate
    else:
        # print("working3")
        if 'ALL' in cam_name:
            cam_name= global_camera_sets[2]

        from camera.camera_run_2 import Camera_Process
        globals()['p5'] = Camera_Process(cam_list=cam_name, rtsp=True, reid_model=reid_model,reid_weight=reid_weight, reid_device=reid_device)
        p5.start()


@app.callback(
    Output('camera_stop_result_5_sets', 'children'),
    [Input('camera_stop_5_sets', 'n_clicks')],
)
def stop_camera_run_sets(n_clicks):

        if n_clicks is None:
            raise PreventUpdate
        else:
            print("stopped")
            global p5
            p5.stop()




def parse_contents(contents):
    return html.Div([
        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents, style={
        'width':'105px',
        'height':'225px',
        }),
    ])


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents')])
def update_output(images):
    if not images:
        return

    global image_value_list
    image_value_list=[]                   #every time show results button is clicked, this empties the list.


    for i, image_str in enumerate(images):
        image = image_str.split(',')[1]
        data = base64.decodestring(image.encode('ascii'))
        with open(os.path.join(UPLOAD_DIRECTORY,"query.png"), "wb") as f:
            f.write(data)

    children = [parse_contents(i) for i in images]
    return children


def update_options(camera_name , frame_rate, images_timestamp):
    option=[{'label':'None', 'value':'None'}]
    for i in range(int(frame_rate)):
        option.append({'label':'Rank {}'.format(i+1), 'value':camera_name + ' Rank{}_'.format(i+1) + str(images_timestamp[i])})

    return option

def parse_gallery(camera_name, frame_rate, image_list):
    children=[]
    children1=[]
    MIN_NUM= min(int(frame_rate),len(image_list))
    images_timestamp=[]
    if MIN_NUM > 5:
        children2=[]
    for i in range(int(MIN_NUM)):
        image_src= image_list[i]
        image_id= "{}".format(camera_name)+ " "+ "Rank {}".format(i+1)
        image_path_list = os.path.split(image_src)[1]
        time_stamp= image_path_list.split('.')[0].split('_')[0]
        time_stamp= datetime.strptime(time_stamp, '%Y-%m-%d-%H-%M-%S-%f')
        images_timestamp.append(time_stamp)

        if i<5:
            children1.append(
                    html.Div([
                        html.Img(id=image_id,src=image_src, className="img_style"),
                        html.P("Rank {}".format(i+1), className="p_style"),
                    ],style={'float':'left',
                    'padding-left':'10px',
                    'padding-top':'10px',})
                    )
        else:
            children2.append(
                    html.Div([
                        html.Img(id=image_id,src=image_src, className="img_style"),
                        html.P("Rank {}".format(i+1), className="p_style"),
                    ],style={'float':'left',
                    'padding-left':'10px',
                    'padding-top':'10px',})
                    )
    if MIN_NUM > 5:
        children= [
                html.Div(children= children1, className="row"),
                html.Div(children= children2, className="row"),
        ]
    else:
        children = children1
    return html.Div([
            html.Div([
                html.A([html.P(str(camera_name))], href='assets/maps/{}.png'.format("-".join(x for x in camera_name.split("-")[0:-1])), target='_blank'),
                dcc.Dropdown(
                    id="{}".format(camera_name),
                    options= update_options(camera_name, MIN_NUM, images_timestamp),
                    value= 'None',
                    style= {'display':'inline-block','margin-top':'40px', 'width':'100px'},
                    searchable=False,
                    clearable=False,
                    )
            ], style={'textAlign':'center'},className='two columns'),
            html.Div(children=children, className="ten columns"),
        ],className="row", style={'margin-top':50})


@app.callback([Output('camera_outputs', 'children'),
                Output('loading-output-1','children'),
                Output('floormaps_division','style')],
              [Input('show_results', 'n_clicks')],
              [State('camera_name_dropdown_reid', 'value'),
               State('frame_rate','value'),
               State('network_dropdown_reid','value'),
               State('network_weight_dropdown_reid', 'value'),
               State('devices_dropdown_reid','value'),
               State('offline_toggle', 'value'),
               State('date_picker','date'),
               State('starttime','value'),
               State('endtime','value')])

def update_output2(n_clicks, camera_dropdown_values, frame_rate, reid_model, reid_weight, reid_device,toggle,  date, starttime, endtime):
    if n_clicks is None:
        raise PreventUpdate
    else:

        if 'ALL' in camera_dropdown_values:
            camera_dropdown_values=[]
            for set_list in global_camera_sets:
                for cam_name in set_list:
                    camera_dropdown_values.append(cam_name)
            camera_dropdown_values= set(camera_dropdown_values)

        if 'SET1' in camera_dropdown_values:
            for cam_name in global_camera_sets[0]:
                camera_dropdown_values.append(cam_name)
            camera_dropdown_values= set(camera_dropdown_values)
            camera_dropdown_values.remove('SET1')

        if 'SET2' in camera_dropdown_values:
            for cam_name in global_camera_sets[1]:
                camera_dropdown_values.append(cam_name)
            camera_dropdown_values= set(camera_dropdown_values)
            camera_dropdown_values.remove('SET2')

        if 'SET3' in camera_dropdown_values:
            for cam_name in global_camera_sets[2]:
                camera_dropdown_values.append(cam_name)
            camera_dropdown_values= set(camera_dropdown_values)
            camera_dropdown_values.remove('SET3')

        if 'SET4' in camera_dropdown_values:
            for cam_name in global_camera_sets[3]:
                camera_dropdown_values.append(cam_name)
            camera_dropdown_values= set(camera_dropdown_values)
            camera_dropdown_values.remove('SET4')



        output_array=[]
        path= "ROSE LAB "

        cam_name_list = []
        for camera in camera_dropdown_values:
            if os.path.exists(os.path.join('static',camera)):
                if len(os.listdir(os.path.join('static',camera))) > 0:
                    cam_name_list.append(camera)

        offline_cam_name_list = []
        for camera in camera_dropdown_values:
            offline_cam_name_list.append(camera)

        img_path= os.path.join('static','query','query.png')
        if toggle==False:
            image_dict = offline_retrieval(img_path,offline_cam_name_list,int(frame_rate),reid_model, reid_weight, reid_device,date,starttime,endtime)
        else:
            image_dict = retrieval(img_path,cam_name_list,int(frame_rate),reid_model, reid_weight, reid_device )

        for camera in image_dict:
            output_array.append(parse_gallery(camera, int(frame_rate), image_dict[camera]))
            path = path + "<-- "+ str(camera)+" "

        hidden_divs=[]
        for counter, name in enumerate(camera_dropdown_values):
            hidden_divs.append(html.Div(id="state_container_{}".format(name), style={'display':'none'}))


        final_output= html.Div(children=output_array)

        return  final_output, [], {'display':'none'}


def update_state_container(camera_value):
    global image_value_list
    image_value_list.append(camera_value)
    # print("hi,", camera_value)
    return camera_value

for camera_set in global_camera_sets:
    for counter,name in enumerate(camera_set):
        app.callback(Output('state_container_{}'.format(name), 'children'),
                        [Input('{}'.format(name), 'value')]
                        )(update_state_container)



def calculate_line_trace(camera_dict_list):
    final_trace={'S1':{'x':[], 'y':[], 'customdata':[]}, 'S2':{'x':[], 'y':[], 'customdata':[]}, 'S21':{'x':[],'y':[], 'customdata':[]}, 'S22':{'x':[],'y':[], 'customdata':[]}}
    # final_trace={}
    final_cameras_list=[]
    for tuple in camera_dict_list:
        camera_name= tuple[0]
        final_cameras_list.append(camera_name)
        building_name= camera_name.split('-')[0]
        floor_name= camera_name.split('-')[1][:2]
        time= tuple[1]

        final_trace[building_name]['x'].append(time)
        final_trace[building_name]['y'].append(floor_name)
        final_trace[building_name]['customdata'].append(camera_name)

    return final_trace, final_cameras_list



@app.callback(Output('floormaps_output', 'children'),
                [Input('show_locations','n_clicks')])
def update_floormaps(n_clicks):

    camera_dict= dict.fromkeys(x for set in global_camera_sets for x in set)
    if n_clicks is None:
        raise PreventUpdate
    else:

        global image_value_list
        image_value_list = list(filter(lambda a: a !='None', image_value_list))

        print( "image_value_list",image_value_list)
        for name in image_value_list:
            name_split= name.split('_')
            time_stamp= name_split[1]
            camera_name= name_split[0].split()[0]
            camera_dict[camera_name]=time_stamp

        camera_dict_list= list({k: v for k, v in camera_dict.items() if v is not None}.items())
        camera_dict_list=sorted(camera_dict_list, key=lambda x: x[1])

        camera_sorted_list,x = zip(*camera_dict_list)


        line_traces, final_camera_list= calculate_line_trace(camera_dict_list)

        img_path= "./assets/images/overview_B3_cluster_1.png"
        floormap_cross_numbers(img_path, final_camera_list)

        df_line_traces= line_traces

        trace_s1= go.Scatter(x= df_line_traces['S1']['x'], y= df_line_traces['S1']['y'], hovertext=df_line_traces['S1']['customdata'] ,name='S1', mode= 'lines+markers', line=dict(width=10), marker=dict(size=20, line=dict(
                color='Black',width=2)), showlegend=True)
        trace_s2= go.Scatter(x= df_line_traces['S2']['x'], y= df_line_traces['S2']['y'], hovertext=df_line_traces['S2']['customdata'] , name='S2', mode= 'lines+markers', line=dict(width=10),  marker=dict(size=20, line=dict(
                color='Black',width=2)), showlegend=True)
        trace_s21=go.Scatter(x= df_line_traces['S21']['x'], y= df_line_traces['S21']['y'], hovertext=df_line_traces['S21']['customdata'] , name='S2.1', mode= 'lines+markers', line=dict(width=10),  marker=dict(size=20,line=dict(
                color='Black',width=2)), showlegend=True)
        trace_s22=go.Scatter(x= df_line_traces['S22']['x'], y= df_line_traces['S22']['y'], hovertext=df_line_traces['S22']['customdata'] , name='S2.2', mode= 'lines+markers', line=dict(width=10),  marker=dict(size=20,line=dict(
                color='Black',width=2)), showlegend=True)

        final_trace= [trace_s1, trace_s2, trace_s21, trace_s22]

        GRAPH = dcc.Graph(
            id="floormaps_graph",
            figure={"data":final_trace,
                    "layout": go.Layout(
                        height=300, title="Person Identification track",
                        paper_bgcolor="#f3f3f3",
                        xaxis= {"title":'Time Stamp'},
                        yaxis= {'categoryorder':'array', 'categoryarray':['B6','B5','B4','B3','B2', 'B1'], "title": "Floors" },
                       # "zaxis": {'categoryorder':'array', 'categoryarray':global_camera_floors,"title": "Floors" }
                       )
                    },
            style={'display':'block'},
                    )
        return html.Div(id='floormaps_division', children=[GRAPH], style={'display':'block'})



@app.callback(Output('experimental_section', 'children'),
                        [Input('floormaps_graph', 'hoverData')])
def update_experiments(hoverData):
    map_name= hoverData['points'][0]['hovertext']
    # image_1= random.choice(["marker_s2_B4_L.png","marker_s2_B4_R.png", "marker_s2.1_B4_R.png", "marker_s2.1_B4_T.png"])
    return html.Div(html.Img(src='static/output_number_cross.png?t='+str(datetime.now()), style={'max-width':'750px',
    'max-height':'750px'}), style={'textAlign':'center'})

@app.callback(Output('console-out','srcDoc'),
    [Input('interval', 'n_intervals')])
def update_console_output(n):
    data=''
    if os.path.exists('log.txt'):
        file = open('log.txt', 'r')

        lines = file.readlines()
        if lines.__len__()<=8:
            last_lines=lines
        else:
            last_lines = lines[-8:]
        for line in last_lines:
            data=data+line + '<BR>'
        file.close()
    return data


@app.callback(Output('datetime_class', 'style'),
                [Input('offline_toggle', 'value')])
def toggle_datetime(value):
    if value==False:
        return {'display': 'block'}
    else:
        return {'display':'none'}


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
