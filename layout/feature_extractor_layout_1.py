import dash
import dash_core_components as dcc
import dash_html_components as html


def populate_devices():
    options= [{'label':'CPU', 'value':'cpu'}]
    for i in range(8):
        options.append({'label':'GPU cuda:{}'.format(i),'value':'cuda:{}'.format(i)})

    return options

def populate_camera_dropdown_menu(global_camera_names):
    values=[{'label':'ALL', 'value':'ALL'}]
    for c in global_camera_names:
        values.append({'label':c, 'value':c})

    return values



def feature_extractor_layout(global_camera_names,models_dict):
    children=[
        html.Div(
            children=[
                html.P("Network Model", className='p-dropdown'),
                dcc.Dropdown(
                    id='network_dropdown',
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
                    id="network_weight_dropdown",
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
                    className='three rows row',
                    children=[
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Camera:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id='camera_name_dropdown_1',
                                    options=populate_camera_dropdown_menu(global_camera_names),
                                    placeholder="Camera...",
                                )
                            ]
                        ),
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Device:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id="devices_dropdown_1",
                                    options=populate_devices(),
                                    placeholder="Select device...",
                                )
                            ]
                        ),
                        html.Div(
                            className='three columns',
                            children=[
                                html.Button(
                                    "Run", id="camera_run_1", className="button_submit"
                                ),
                            ]
                        ),

                        html.Div(
                            className="one column camera-run-done",
                            id="camera_run_result_1",
                        )

                    ]
                ),

                html.Br(),

                html.Div(
                    className='three rows row',
                    children=[
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Camera:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id='camera_name_dropdown_2',
                                    options=populate_camera_dropdown_menu(global_camera_names),
                                    placeholder="Camera...",
                                )
                            ]
                        ),
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Device:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id="devices_dropdown_2",
                                    options=populate_devices(),
                                    placeholder="Select device...",
                                )
                            ]
                        ),
                        html.Div(
                            className='three columns',
                            children=[
                                html.Button(
                                    "Run", id="camera_run_2", className="button_submit"
                                ),
                            ]
                        ),

                        html.Div(
                            className="one column camera-run-done",
                            id="camera_run_result_2",
                        )

                    ]
                ),

                html.Br(),

                html.Div(
                    className='three rows row',
                    children=[
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Camera:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id='camera_name_dropdown_3',
                                    options=populate_camera_dropdown_menu(global_camera_names),
                                    placeholder="Camera...",
                                )
                            ]
                        ),
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Device:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id="devices_dropdown_3",
                                    options=populate_devices(),
                                    placeholder="Select device...",
                                )
                            ]
                        ),
                        html.Div(
                            className='three columns',
                            children=[
                                html.Button(
                                    "Run", id="camera_run_3", className="button_submit"
                                ),
                            ]
                        ),

                        html.Div(
                            className="one column camera-run-done",
                            id="camera_run_result_3",
                        )
                    ]
                ),


                html.Br(),


                html.Div(
                    className='three rows row',
                    children=[
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Camera:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id='camera_name_dropdown_4',
                                    options=populate_camera_dropdown_menu(global_camera_names),
                                    placeholder="Camera...",
                                )
                            ]
                        ),
                        html.Div(
                            className='four columns',
                            children=[
                                html.P("Device:", className="p-dropdown"),
                                dcc.Dropdown(
                                    id="devices_dropdown_4",
                                    options=populate_devices(),
                                    placeholder="Select device...",
                                )
                            ]
                        ),
                        html.Div(
                            className='three columns',
                            children=[
                                html.Button(
                                    "Run", id="camera_run_4", className="button_submit"
                                ),
                            ]
                        ),

                        html.Div(
                            className="one column camera-run-done",
                            id="camera_run_result_4",
                        )
                    ]
                )
            ]
        )

    ]

    return children
