import dash
import dash_core_components as dcc
import dash_html_components as html



def populate_devices():
    options= [{'label':'CPU', 'value':'cpu'}]
    for i in range(8):
        options.append({'label':'GPU {}'.format(i),'value':'cuda:{}'.format(i)})

    return options

def populate_camera_dropdown_menu(global_camera_names):
    values=[{'label':'ALL', 'value':'ALL'}]
    for c in global_camera_names:
        values.append({'label':c, 'value':c})

    return values

def populate_camera_dropdown_menu_all(global_camera_sets):
    global_camera_names= [x for set in global_camera_sets for x in set]
    values=[{'label':'ALL', 'value':'ALL'}]
    for c in global_camera_names:
        values.append({'label':c, 'value':c})

    return values




def feature_extractor_layout_sets(global_camera_sets,models_dict):
    children=[
        html.Div(
            children=[
                html.P("Network Model", className='p-dropdown'),
                dcc.Dropdown(
                    id='network_dropdown_sets',
                    className="div-for-dropdown",
                    options=[{'label': model, 'value': model} for model in list(models_dict.keys())],
                    value= list(models_dict.keys())[0],
                    placeholder="Select a Network...",
                )
            ]
        ),

        html.Div(
            [
                html.P("Network Weights", className='p-dropdown'),
                dcc.Dropdown(
                    id="network_weight_dropdown_sets",
                    className="div-for-dropdown",
                    placeholder="Select weight file...",
                )

            ]
        ),

        html.Br(),
        html.Br(),


        html.Div(
            className='twelve rows',
            children=[
                html.Div(
                    className='four rows',
                    children=[
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Set 1:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id='camera_name_dropdown_1_sets',
                                    options=populate_camera_dropdown_menu(global_camera_sets[0]),
                                    placeholder="Camera...",
                                    multi=True,
                                    style={'fontSize': 12}
                                )
                            ]
                        ),
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Device:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id="devices_dropdown_1_sets",
                                    options=populate_devices(),
                                    placeholder="Select device...",
                                )
                            ]
                        ),
                        html.Div(
                            className='two columns',
                            children=[
                                html.Button(
                                    "Run", id="camera_run_1_sets", className="button_submit"
                                ),
                            ]
                        ),

                        html.Div(
                            className='two columns',
                            children=[
                                html.Button(
                                    "Stop", id="camera_stop_1_sets", className="button_submit"
                                ),
                            ]
                        ),



                    ]
                ),



                html.Div(
                    className='four rows',
                    children=[
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Set 2:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id='camera_name_dropdown_2_sets',
                                    options=populate_camera_dropdown_menu(global_camera_sets[1]),
                                    placeholder="Camera...",
                                    multi=True,
                                    style={'fontSize': 12}
                                )
                            ]
                        ),
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Device:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id="devices_dropdown_2_sets",
                                    options=populate_devices(),
                                    placeholder="Select device...",
                                )
                            ]
                        ),
                        html.Div(
                            className='two columns',
                            children=[
                                html.Button(
                                    "Run", id="camera_run_2_sets", className="button_submit"
                                ),
                            ]
                        ),

                        html.Div(
                            className='two columns',
                            children=[
                                html.Button(
                                    "Stop", id="camera_stop_2_sets", className="button_submit"
                                ),
                            ]
                        ),

                    ]
                ),

                

                html.Div(
                    className='four rows',
                    children=[
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Set 3:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id='camera_name_dropdown_3_sets',
                                    options=populate_camera_dropdown_menu(global_camera_sets[2]),
                                    placeholder="Camera...",
                                    multi=True,
                                    style={'fontSize': 12}
                                )
                            ]
                        ),
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Device:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id="devices_dropdown_3_sets",
                                    options=populate_devices(),
                                    placeholder="Select device...",
                                )
                            ]
                        ),
                        html.Div(
                            className='two columns',
                            children=[
                                html.Button(
                                    "Run", id="camera_run_3_sets", className="button_submit"
                                ),
                            ]
                        ),

                        html.Div(
                            className='two columns',
                            children=[
                                html.Button(
                                    "Stop", id="camera_stop_3_sets", className="button_submit"
                                ),
                            ]
                        ),


                    ]
                ),
                html.Br(),

                html.Div(
                    className='four rows',
                    children=[
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Set 4:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id='camera_name_dropdown_4_sets',
                                    options=populate_camera_dropdown_menu(global_camera_sets[3]),
                                    placeholder="Camera...",
                                    multi=True,
                                    style={'fontSize': 12}
                                )
                            ]
                        ),
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Device:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id="devices_dropdown_4_sets",
                                    options=populate_devices(),
                                    placeholder="Select device...",
                                )
                            ]
                        ),
                        html.Div(
                            className='two columns',
                            children=[
                                html.Button(
                                    "Run", id="camera_run_4_sets", className="button_submit"
                                ),
                            ]
                        ),

                        html.Div(
                            className='two columns',
                            children=[
                                html.Button(
                                    "Stop", id="camera_stop_4_sets", className="button_submit"
                                ),
                            ]
                        ),


                    ]
                ),

                html.Div(
                    className='four rows',
                    children=[
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Set 5:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id='camera_name_dropdown_5_sets',
                                    options=populate_camera_dropdown_menu(global_camera_sets[4]),
                                    placeholder="Camera...",
                                    multi=True,
                                    style={'fontSize': 12}
                                )
                            ]
                        ),
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Device:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id="devices_dropdown_5_sets",
                                    options=populate_devices(),
                                    placeholder="Select device...",
                                )
                            ]
                        ),
                        html.Div(
                            className='two columns',
                            children=[
                                html.Button(
                                    "Run", id="camera_run_5_sets", className="button_submit"
                                ),
                            ]
                        ),

                        html.Div(
                            className='two columns',
                            children=[
                                html.Button(
                                    "Stop", id="camera_stop_5_sets", className="button_submit"
                                ),
                            ]
                        ),


                    ]
                ),

                 html.Div(
                    className='four rows',
                    children=[
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("All:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id='camera_name_dropdown_6_sets',
                                    options=populate_camera_dropdown_menu_all(global_camera_sets),
                                    placeholder="Camera...",
                                    multi=True,
                                    style={'fontSize': 12}
                                )
                            ]
                        ),
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Device:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id="devices_dropdown_6_sets",
                                    options=populate_devices(),
                                    placeholder="Select device...",
                                )
                            ]
                        ),
                        html.Div(
                            className='two columns',
                            children=[
                                html.Button(
                                    "Run", id="camera_run_6_sets", className="button_submit"
                                ),
                            ]
                        ),

                        html.Div(
                            className='two columns',
                            children=[
                                html.Button(
                                    "Stop", id="camera_stop_6_sets", className="button_submit"
                                ),
                            ]
                        ),


                    ]
                ),
            ]
        ),

        html.Div([
            html.Div(id='camera_run_result_{}_sets'.format(i+1), style={'display':'none'}) for i in range(5)
        ]),
        html.Div([
            html.Div(id='camera_stop_result_{}_sets'.format(i+1), style={'display':'none'}) for i in range(5)
        ]),

        html.Iframe(id='console-out',className="console-out", srcDoc=' '),
        dcc.Interval(id="interval", interval=500, n_intervals=0),



    ]

    return children
