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

#path to save the image that you upload on the server.
UPLOAD_DIRECTORY = "static/query"

external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True


global_camera_names= ["S21-B4-L-13" , "S21-B4-L-15", "S21-B4-R-10"]
cams_map_testing= ["S2.1-B4-L-B", "S2.1-B4-L-T", "S2.1-B4-R-B"]

models_dict={'ResNet50':['ResNet50_Market.pth', 'ResNet101_Market.pth'], 'Net':['Net_Market.t7'], 'SE_ResNet':['SE_ResNet50_Market.pth', 'SE_ResNet101_Market.pth']}

image_value_list=[]
output_result=[]
camera_dict= dict.fromkeys(global_camera_names)


count=0

img_style_false= {
'max-width':'250px',
'max-height':'250px',
'border': '2px solid',
'border-radius': '4px',
}

img_style_true={
'max-width':'250px',
'max-height':'250px',
'border': '2px solid #00FF00',
'border-radius': '4px',
}

p_style= {
'textAlign':'center',
'margin-top':'5px',
}

def populate_camera_dropdown_menu():
    global global_camera_names
    values=[{'label':'ALL', 'value':'ALL'}]
    for c in global_camera_names:
        values.append({'label':c, 'value':c})

    return values

def populate_devices():
    options= [{'label':'CPU', 'value':'cpu'}]
    for i in range(8):
        options.append({'label':'GPU cuda:{}'.format(i),'value':'cuda:{}'.format(i)})

    return options

app.layout = html.Div([
        dcc.ConfirmDialog(
            id='confirm',
            message='The features have been extracted',
        ),
        html.Div([
            #Division1 for 2 logos
            html.Div([
                html.Img(
                    src="/assets/images/NTU_Logo.png",
                    # className='six columns',
                    style={
                        'display': 'inline-block',
                        'height': '15%',
                        'width': '15%',
                        'position': 'relative',
                        'margin-left': 'auto',
                        'margin-right':'auto',
                        'padding-right': '30px'
                    },
                ),
                html.Img(
                    src="/assets/images/rose_lab_logo.png",
                    # className='six columns',
                    style={
                        'display': 'inline-block',
                        'height': '5%',
                        'width': '10%',
                        'position': 'relative',
                        'margin-left': 'auto',
                        'margin-right':'auto',
                        'padding-left': '30px'

                    },
                ),
            ],className='row',
            style={
            'textAlign':'center',
            },
            ),
            #Division1 end


            #Division2 for Heading
            html.Div([
                html.H3(children='NTU Reid Demo',
                        className='row',
                        style={
                            'textAlign': 'center',
                            'margin-top': 20,
                        }),
            ]),
            #Division2 end

            #Division3 for Image upload and dropdown menu
            html.Div([

                #division for image upload and query image
                html.Div(
                children=[
                    html.Div(id='output-image-upload'),

                    dcc.Upload(id='upload-image',
                    children=[html.Button('Upload Query Image')],
                    style={
                    'width': '100%',
                    'height': '60px',
                    'textAlign': 'center',
                    'margin': '10px'
                    },
                # Allow multiple files to be uploaded
                multiple=True
                ),
                ],
                className='five columns',
                style={
                'textAlign':'center',
                }),


                #division for dropdown menus and other option selection
                html.Div([


                    html.Div([
                        html.P('Run Camera Feature Extractor?', style={'display':'inline-block', 'padding-right':'30px', 'font-weight':'bold'}),
                        html.Div([dcc.RadioItems(
                            id='camera_run_check',
                            options=[
                                {'label': 'Yes', 'value': 'Yes'},
                                {'label': 'No', 'value': 'No'},
                            ],
                            value='No',
                            labelStyle={'display': 'inline-block'}
                        )
                        ], style={'display':'inline-block','padding-right':'140px'}),

                    ], style={'padding-bottom':'10px'}),
                    html.Div([
                        html.Div([
                            html.P("Network:", style={'display':'inline-block','padding-right':'100px', 'font-weight':'bold'}),
                            dcc.Dropdown(
                                id="network_dropdown",
                                options=[{'label': model, 'value': model} for model in list(models_dict.keys())],
                                value= list(models_dict.keys())[0],
                                placeholder="Select a Network...",
                                style={'display':'inline-block','width': '150px'}
                            )
                        ],style={'display':'inline-block', 'padding-right':'20px', 'textAlign':'center'}),

                        html.Div([
                            html.P("Weights:", style={'display':'inline-block','padding-right':'20px', 'font-weight':'bold'}),
                            dcc.Dropdown(
                                id="network_weight_dropdown",
                                placeholder="Select weight file...",
                                style={'display':'inline-block','width': '150px'}
                            )

                        ], style={'display':'inline-block', 'padding-right':'20px', 'textAlign':'center'}),

                        html.Div([
                            html.P("Device:", style={'display':'inline-block','padding-right':'20px', 'font-weight':'bold'}),
                            dcc.Dropdown(
                                id="devices_dropdown",
                                options=populate_devices(),
                                placeholder="Select device...",
                                style={'display':'inline-block','width': '150px'}
                            )

                        ], style={'display':'inline-block', 'textAlign':'center'})
                    ]),

                    html.Div([
                        html.P("Camera:", style={'display':'inline-block','padding-right':'105px', 'font-weight':'bold'}),
                        dcc.Dropdown(
                            id='camera_name_dropdown',
                            options=populate_camera_dropdown_menu(),
                            placeholder="Select a Camera...",
                            multi=True,
                            style={'display':'inline-block',
                                    'width': '650px'}
                        )

                    ],
                    style={
                        'padding-top':10,

                    }),

                    html.Div([
                        html.P("Number of Frames:", style={'display':'inline-block','padding-right':'30px', 'font-weight':'bold'}),
                        dcc.Dropdown(
                            id='frame_rate',
                            options=[
                                {'label': '5', 'value': '5'},
                                {'label': '10', 'value': '10'},
                                {'label': '20', 'value': '20'}
                            ],
                            placeholder="Select the number of frames..",
                            style={'display':'inline-block','width': '650px'}
                        )

                    ], style={
                    'padding-top':10,

                    }),

                    html.Div([
                        html.Div(id="camera_run_area_button", style={'display':'inline-block','padding-right:':'20px'}),
                        html.Div([
                            html.Button('Show Results', id='show_results', className="button-primary"),
                        ], style={
                            'display':'inline-block',
                            'margin-left:':10,
                        }),

                        html.Div([
                            html.Button('Download Results', id='Download_results'),
                        ], style={
                            'display':'none',
                            'margin-left': 10,
                            # 'display':'none',

                        }),

                    ], className="row",
                    style={
                        'textAlign':'center',
                        'margin-top':50,

                    }),

                ], className='seven columns',
                style={
                'padding-down':10,
                }),
            ], className='row', style={'margin-right':'70px', 'margin-top': '30px'}),

            #Division3 ends
            #Division4 for output
            html.Div(id='state_container', style={'display': 'none'}),
            # html.Div([
            #     html.Div(className="ten columns offset-by-one",id='textbox_query_show', style={'margin-top':50, 'font-size':'15px', 'font-weight':'bold'}),
            # ],className="row"),x

            html.Div(id="camera_outputs", style={'margin-top':50,}),


            html.Div(id="submit_button_area", style= {'margin-top':'40px', 'text-align':'center'}),

            html.Div([

            html.Div(id="floormaps_output",  style= {'margin-top':'40px', 'text-align':'center', 'textAlign':'center'} , className="ten columns offset-by-one")
            ],
            className="row"
            ),

            html.Div(id="experimental_section"),
            #Division4 ends
    ], className='row', style={'margin-left':'20px', 'margin-right':'20px'})
    ])




@app.callback(
    Output('camera_run_area_button', 'children'),
    [Input('camera_run_check', 'value')])
def update_camera_run_button(value):
    if value=='Yes':
        return html.Button('Camera Run', id='camera_run_button', className="button-primary", style={'display':'inline-block', 'padding-right:':'20px'})


@app.callback(
    Output('confirm', 'displayed'),
    [Input('camera_run_button', 'n_clicks')],
    [State('network_dropdown','value'),
     State('network_weight_dropdown', 'value'),
     State('devices_dropdown','value')]
)
def run_camera_run(n_clicks, reid_model, reid_weight, reid_device):
    if n_clicks is None:
        raise PreventUpdate
    else:
        print(reid_model)
        print(reid_weight)
        print(reid_device)

        from camera.camera_run import camera_run
        camera_run(cam_names=global_camera_names, rtsp=False, skip_frame=10,reid_model=reid_model,reid_weight=reid_weight, reid_device=reid_device)
        print("Done Donaaa Done")

        return True
@app.callback(
    Output('network_weight_dropdown', 'options'),
    [Input('network_dropdown', 'value')])
def update_weight_dropdown(name):
    return [{'label': i, 'value': i} for i in models_dict[name]]



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
        with open(os.path.join(UPLOAD_DIRECTORY,f"query.png"), "wb") as f:
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
    MIN_NUM= int(frame_rate)
    cam_name_list=[camera_name]
    img_path= 'static/query/query.png'
    image_list = retrieval(img_path,cam_name_list,MIN_NUM,reid_model, reid_weight, reid_device )
    images_timestamp=[]
    for i in range(int(MIN_NUM)):
        image_src= image_list[i]
        print(image_src)
        image_id= "{}".format(camera_name)+ " "+ "Rank {}".format(i+1)
        time_stamp= image_src.split('/')[-1].split('.')[0].split('_')[0]
        time_stamp= datetime.strptime(time_stamp, '%Y-%m-%d-%H-%M-%S-%f')
        images_timestamp.append(time_stamp)

        children.append(
                html.Div([
                    html.Img(id=image_id,src=image_src, style=img_style_false),
                    html.P("Rank {}".format(i+1), style=p_style),
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
                Output('submit_button_area', 'children'),
                Output('state_container','children')],
              [Input('show_results', 'n_clicks')],
              [State('camera_name_dropdown', 'value'), State('frame_rate','value'),State('network_dropdown','value'), State('network_weight_dropdown', 'value'), State('devices_dropdown','value')])

def update_output2(n_clicks, camera_dropdown_values, frame_rate, reid_model, reid_weight, reid_device):
    if n_clicks is None:
        raise PreventUpdate
    else:
        #write a function to get the path of the folder we want to show. So the query image will be stored in the form of a string and then we will show images.

        if 'ALL' in camera_dropdown_values:
            camera_dropdown_values= global_camera_names


        folder_name= "demo"
        output_array=[]
        path= "ROSE LAB "

        for camera in camera_dropdown_values:
            output_array.append(parse_gallery(folder_name, camera, frame_rate, reid_model, reid_weight, reid_device))
            path = path + "<-- "+ str(camera)+" "

        hidden_divs=[]
        for counter, name in enumerate(global_camera_names):
            hidden_divs.append(html.Div(id="state_container_{}".format(name), style={'display':'none'}))


        final_output= html.Div(children=output_array)

        return  final_output, [html.Div(html.Button('Show Locations', id='show_maps_results', className="button-primary"),)], hidden_divs


def create_gantt_chart_df(camera_dict_list):
    df=[]

    camera_name= camera_dict_list[0][0]
    start_time= camera_dict_list[0][1]
    end_time=camera_dict_list[0][1]

    current_basement= camera_name.split()[1].split('-')[1][:2]
    current_building= camera_name.split()[1].split('-')[0]

    for i in range(1, len(camera_dict_list)):
        # print(current_basement,"current_basement")
        # print(current_building,"current_bilding")

        camera_name= camera_dict_list[i][0]
        time_stamp= camera_dict_list[i][1]

        if current_basement!=camera_name.split()[1].split('-')[1] or current_building!=camera_name.split()[1].split('-')[0]:
            df.append(dict(Task=current_basement, Start=start_time, Finish=end_time, Resource=current_building))
            current_basement=camera_name.split()[1].split('-')[1][:2]
            current_building= camera_name.split()[1].split('-')[0]
            start_time= time_stamp
            end_time= time_stamp

        else:
            end_time= time_stamp

    df.append(dict(Task=current_basement, Start=start_time, Finish=end_time, Resource=current_building))


    # print(df)
    return df




#the map will break if the person traces the path back to the same place.

def calculate_line_trace(camera_dict_list):
    final_trace={'S1':{'x':[], 'y':[], 'customdata':[]}, 'S2':{'x':[], 'y':[], 'customdata':[]}, 'S21':{'x':[],'y':[], 'customdata':[]}}
    # final_trace={}
    for tuple in camera_dict_list:
        camera_name= tuple[0]
        building_name= camera_name.split('-')[0]
        floor_name= camera_name.split('-')[1]
        time= tuple[1]

        final_trace[building_name]['x'].append(time)
        final_trace[building_name]['y'].append(floor_name)
        final_trace[building_name]['customdata'].append(camera_name)

    return final_trace

#
# def create_dynamic_callback(name, image_value):
#         print("function was called")
@app.callback(Output('floormaps_output', 'children'),
                [Input('show_maps_results','n_clicks')])
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

        print(camera_dict_list)
        print(camera_sorted_list)

        img_path= "./assets/images/overview_B3_cluster_1.png"
        floormap_cross_numbers(img_path, cams_map_testing)

        line_traces= calculate_line_trace(camera_dict_list)
        # print(line_traces)
        # df_line_traces= {'S1':{'x':['2019-10-02 09:55:25','2019-10-02 10:02:25', '2019-10-02 10:04:25','2019-10-02 10:06:25', '2019-10-02 10:12:25'],'y':['B2','B4','B4','B4', 'B4'], 'customdata':["MLDA S1-B2-R-T", "MLDA S1-B4-R-M", "MLDA S1-B4-R-B","Infinitus S1-B4b-R-TR", "Infinitus S1-B4b-R-T"]}, 'S2':{'x':['2019-10-02 10:21:25', '2019-10-02 10:23:25'],'y':['B4', 'B4'], 'customdata':["Infinitus S2-B4b-R-TR", "Infinitus S2-B4b-R-T"]}, 'S21':{'x':['2019-10-02 10:13:25','2019-10-02 10:15:25', '2019-10-02 10:17:25'],'y':['B4','B4', 'B4'],'customdata':["MLDA S2.1-B4-R-T", "MLDA S2.1-B4-R-M", "MLDA S2.1-B4-R-B"]}}

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

        final_trace= [trace_s1, trace_s2, trace_s21]

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
    print(hoverData)
    map_name= hoverData['points'][0]['hovertext']
    print(map_name)
    image_1= random.choice(["marker_s2_B4_L.png","marker_s2_B4_R.png", "marker_s2.1_B4_R.png", "marker_s2.1_B4_T.png"])

    return html.Div(html.Img(src='/assets/maps_markers/{}'.format(image_1), style={'max-width':'750px',
    'max-height':'750px'}), style={'textAlign':'center'})




"""
#go.figure
go.Figure(data= go.Scatter3d(x=x, y=y, z=z),
                layout= go.Layout(
                    title="Location Map",
                    yaxis= dict( categoryorder='array', categoryarray=global_camera_names, title='Cameras'),
                    xaxis= dict(title='Time')
                )
        )
"""


def update_state_container(camera_value):

    global image_value_list
    image_value_list.append(camera_value)
    return camera_value

for counter,name in enumerate(global_camera_names):

    app.callback(Output('state_container_{}'.format(name), 'children'),
                    [Input('{}'.format(name), 'value')]
                    )(update_state_container)


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
