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
import cv2
from plotting.floormap_cross_numbers import floormap_cross_numbers
import base64
import os
from layout.feature_extractor_layout_sets import feature_extractor_layout_sets
from layout.feature_extractor_layout_2 import feature_extractor_layout
from layout.retrieval_run_layout import retrieval_run_layout

#path to save the image that you upload on the server.
UPLOAD_DIRECTORY = "static/query"
# external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True
server = app.server

SET1= ["S2-B4b-R-TR","S2-B4b-R-T","S2-B4b-L-T","S2-B4b-L-TL"]
SET2=["S2-B3b-R-TR", "S2-B3b-R-T","S2-B3b-L-T","S2-B3b-L-TL"]
SET3=["S2.1-B4-T" ,"S2.1-B4-R-T", "S2.1-B4-R-M" ,"S2.1-B4-R-B" , "S2.1-B3-T", "S2.1-B3-R-T","S2.1-B3-R-M","S2.1-B3-R-B"]
global_camera_sets= [SET1, SET2, SET3]

global_camera_names= ["S2-B4b-L-B","S2-B4b-L-BR","S1-B4b-L-BL","S1-B4b-R-B","S21-B4-T","S22-B4-T"]
cams_map_testing= ["S2-B4b-L-B","S2-B4b-L-BR","S1-B4b-L-BL","S1-B4b-R-B","S21-B4-T","S22-B4-T"]
models_dict={'ResNet50':['ResNet50_Market.pth'],'ResNet101':['ResNet101_Market.pth'],'SE_ResNet50':['SE_ResNet50_Market.pth'],'SE_ResNet101':['SE_ResNet101_Market.pth']}
image_value_list=[]
output_result=[]
camera_dict= dict.fromkeys(global_camera_names)
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
                                    src= app.get_asset_url("NTU_logo_new.png"), className="logo"
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
                            parent_className='custom-tabs',
                            children=[
                                dcc.Tab(
                                    label='camera_sets',
                                    value='tab1',
                                    className='custom-tab',
                                    selected_className='custom-tab--selected',
                                    selected_style={'color':'#60b5ab'},
                                    children=[
                                        html.Div(
                                            className="row",
                                            children=feature_extractor_layout_sets(global_camera_sets, models_dict)
                                        )
                                    ]),

                                dcc.Tab(
                                    label='Feature Extractor',
                                    value='tab2',
                                    className='custom-tab',
                                    selected_className='custom-tab--selected',
                                    selected_style={'color':'#60b5ab'},
                                    children=[
                                        html.Div(
                                            className="row",
                                            children=feature_extractor_layout(global_camera_names, models_dict)
                                        )
                                    ]),

                                dcc.Tab(
                                    label='Retrieval Run',
                                    value='tab3',
                                    className='custom-tab',
                                    selected_className='custom-tab--selected',
                                    selected_style={'color':'#60b5ab'},
                                    children=[
                                        html.Div(
                                            className="row",
                                            children=retrieval_run_layout(global_camera_names, models_dict)
                                        )
                                    ]),

                            ]),
                            html.Iframe(id='console-out',className="console-out", srcDoc='Hello'),
                            dcc.Interval(id="interval", interval=500, n_intervals=0),

                    ], className="four columns div-user-controls"
                ),
                html.Div(
                    [
                        html.Div(id='state_container', style={'display': 'none'}),
                        html.Br(),
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


for i in range(3):
    @app.callback(
        Output('camera_run_result_{}_sets'.format(i+1), 'children'),
        [Input('camera_run_{}_sets'.format(i+1), 'n_clicks')],
        [State('network_dropdown_sets','value'),
         State('network_weight_dropdown_sets', 'value'),
         State('camera_name_dropdown_{}_sets'.format(i+1), 'value'),
         State('devices_dropdown_{}_sets'.format(i+1),'value')]
    )
    def run_camera_run_sets(n_clicks, reid_model, reid_weight,cam_name, reid_device):

        if n_clicks is None:
            raise PreventUpdate
        else:

            print("Working")
            # from camera.camera_run_1 import camera_run
            # camera_run(cam_name, True, 10,reid_model,reid_weight, reid_device)
            # print("Done Donaaa Done")
            # return [html.P("Done!")]
    @app.callback(
        Output('camera_stop_result_{}_sets'.format(i+1), 'children'),
        [Input('camera_stop_{}_sets'.format(i+1), 'n_clicks')],
    )
    def stop_camera_run_sets(n_clicks):

            if n_clicks is None:
                raise PreventUpdate
            else:

                print("stopped")
                # global p
                # p.stop()


def parse_contents(contents):
    return html.Div([
        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents, style={
        'max-width':'250px',
        'max-height':'250px',
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

def parse_gallery(folder_name, camera_name, frame_rate,reid_model, reid_weight, reid_device):
    children=[]
    cam_name_list=[camera_name]
    img_path= 'static/query/query.png'
    image_list = retrieval(img_path,cam_name_list,frame_rate,reid_model, reid_weight, reid_device )
    MIN_NUM= min(int(frame_rate),len(image_list))
    images_timestamp=[]
    for i in range(int(MIN_NUM)):
        image_src= image_list[i]
        image_id= "{}".format(camera_name)+ " "+ "Rank {}".format(i+1)
        time_stamp= image_src.split('/')[-1].split('.')[0].split('_')[0]
        time_stamp= datetime.strptime(time_stamp, '%Y-%m-%d-%H-%M-%S-%f')
        images_timestamp.append(time_stamp)

        children.append(
                html.Div([
                    html.Img(id=image_id,src=image_src, className="img_style"),
                    html.P("Rank {}".format(i+1), className="p_style"),
                ],style={'float':'left',
                'padding-left':'10px',
                'padding-top':'10px',})
                )

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
            html.Div(children=children, className='ten columns'),
        ],className="row", style={'margin-top':50})


@app.callback([Output('camera_outputs', 'children'),
                Output('state_container','children')],
              [Input('show_results', 'n_clicks')],
              [State('camera_name_dropdown_reid', 'value'), State('frame_rate','value'),State('network_dropdown_reid','value'), State('network_weight_dropdown_reid', 'value'), State('devices_dropdown_reid','value')])

def update_output2(n_clicks, camera_dropdown_values, frame_rate, reid_model, reid_weight, reid_device):
    if n_clicks is None:
        raise PreventUpdate
    else:

        if 'ALL' in camera_dropdown_values:
            camera_dropdown_values= global_camera_names


        folder_name= "demo"
        output_array=[]
        path= "ROSE LAB "

        for camera in camera_dropdown_values:
            output_array.append(parse_gallery(folder_name, camera, int(frame_rate), reid_model, reid_weight, reid_device))
            path = path + "<-- "+ str(camera)+" "

        hidden_divs=[]
        for counter, name in enumerate(global_camera_names):
            hidden_divs.append(html.Div(id="state_container_{}".format(name), style={'display':'none'}))


        final_output= html.Div(children=output_array)

        return  final_output, hidden_divs



def update_state_container(camera_value):

    global image_value_list
    image_value_list.append(camera_value)
    return camera_value

for counter,name in enumerate(global_camera_names):

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
        floor_name= camera_name.split('-')[1]
        time= tuple[1]

        final_trace[building_name]['x'].append(time)
        final_trace[building_name]['y'].append(floor_name)
        final_trace[building_name]['customdata'].append(camera_name)

    return final_trace, final_cameras_list



@app.callback(Output('floormaps_output', 'children'),
                [Input('show_locations','n_clicks')])
def update_floormaps(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:

        global image_value_list
        image_value_list = list(filter(lambda a: a !='None', image_value_list))
        for name in image_value_list:
            name_split= name.split('_')
            time_stamp= name_split[1]
            camera_name= name_split[0].split()[0]

            global camera_dict
            camera_dict[camera_name]=time_stamp

        camera_dict_list= list({k: v for k, v in camera_dict.items() if v is not None}.items())
        camera_dict_list=sorted(camera_dict_list, key=lambda x: x[1])

        camera_sorted_list,x = zip(*camera_dict_list)


        line_traces, final_camera_list= calculate_line_trace(camera_dict_list)

        img_path= "./assets/images/overview_B3_cluster_1.png"
        floormap_cross_numbers(img_path, final_camera_list)

        df_line_traces= line_traces

        trace_s1= go.Scatter(x= df_line_traces['S1']['x'], y= df_line_traces['S1']['y'], hovertext=df_line_traces['S1']['customdata'] ,name='S1', mode= 'lines+markers', line=dict(width=10), marker=dict(size=20, line=dict(
                color='Black',
                width=2
            )))
        trace_s2= go.Scatter(x= df_line_traces['S2']['x'], y= df_line_traces['S2']['y'], hovertext=df_line_traces['S2']['customdata'] , name='S2', mode= 'lines+markers', line=dict(width=10),  marker=dict(size=20, line=dict(
                color='Black',
                width=2
            )))
        trace_s21=go.Scatter(x= df_line_traces['S21']['x'], y= df_line_traces['S21']['y'], hovertext=df_line_traces['S21']['customdata'] , name='S2.1', mode= 'lines+markers', line=dict(width=10),  marker=dict(size=20,line=dict(
                color='Black',
                width=2
            )), showlegend=True)

        trace_s22=go.Scatter(x= df_line_traces['S22']['x'], y= df_line_traces['S22']['y'], hovertext=df_line_traces['S22']['customdata'] , name='S2.2', mode= 'lines+markers', line=dict(width=10),  marker=dict(size=20,line=dict(
                color='Black',
                width=2
            )), showlegend=True)

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
                    }
                    )
        return GRAPH


@app.callback(Output('experimental_section', 'children'),
                        [Input('floormaps_graph', 'hoverData')])
def update_experiments(hoverData):
    map_name= hoverData['points'][0]['hovertext']
    # image_1= random.choice(["marker_s2_B4_L.png","marker_s2_B4_R.png", "marker_s2.1_B4_R.png", "marker_s2.1_B4_T.png"])
    return html.Div(html.Img(src='static/output_number_cross.png?t='+str(datetime.now()), style={'max-width':'750px',
    'max-height':'750px'}), style={'textAlign':'center'})

@app.callback(dash.dependencies.Output('console-out','srcDoc'),
    [dash.dependencies.Input('interval', 'n_intervals')])
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


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
