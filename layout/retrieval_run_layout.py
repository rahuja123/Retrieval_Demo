import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from datetime import datetime as dt


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

def populate_camera_dropdown_menu_sets(global_camera_sets):
    values=[{'label':'ALL', 'value':'ALL'},{'label':'SET1', 'value':'SET1'},{'label':'SET2', 'value':'SET2'}, {'label':'SET3', 'value':'SET3'}]
    for c in global_camera_sets:
        for cam in c:
            values.append({'label':cam, 'value':cam})
    return values


def retrieval_run_layout(global_camera_sets,models_dict):
    children=[

        html.Div(
            className="row",
            style={'textAlign':'center'},
            children=[
                html.Div(id='output-image-upload'),
                dcc.Upload(
                    id='upload-image',
                    children=[html.Button('Upload Query Image', className="button-query")],
                    multiple=True,
                ),
            ]
        ),

        html.Br(),
        html.Br(),

        html.Div(
            children=[
                daq.ToggleSwitch(
                    id='offline_toggle',
                    label=['Offline', 'Online'],
                    style={'width': '250px', 'margin': 'auto'},
                    value=False
                ),
            ]
        ),


        html.Div(
            children=[
                html.P("Network Model", className='p-dropdown'),
                dcc.Dropdown(
                    id='network_dropdown_reid',
                    className="div-for-dropdown",
                    options=[{'label': model, 'value': model} for model in list(models_dict.keys())],
                    value= list(models_dict.keys())[0],
                    placeholder="Select a Network...",
                    clearable=False,
                )
            ]
        ),

        html.Div(
            [
                html.P("Network Weights", className='p-dropdown'),
                dcc.Dropdown(
                    id="network_weight_dropdown_reid",
                    className="div-for-dropdown",
                    placeholder="Select weight file...",
                    clearable=False,
                )

            ]
        ),

        html.Div(
            [
                html.P("Device", className='p-dropdown'),
                dcc.Dropdown(
                    id="devices_dropdown_reid",
                    className="div-for-dropdown",
                    options=populate_devices(),
                    placeholder="Select device...",
                    clearable=False,
                    value='cpu'
                )
            ]
        ),

        html.Div(
            children=[
                html.P("Camera:", className="p-dropdown"),
                dcc.Dropdown(
                    id='camera_name_dropdown_reid',
                    className="div-for-dropdown",
                    options=populate_camera_dropdown_menu_sets(global_camera_sets),
                    placeholder="Choose the camera set...",
                    multi=True,
                )
            ]
        ),

        html.Div(
            children=[
                html.P("Number of Frames:", className="p-dropdown"),
                dcc.Dropdown(
                    id='frame_rate',
                    className="div-for-dropdown",
                    options=[
                        {'label': '1', 'value': '1'},
                        {'label': '3', 'value': '3'},
                        {'label': '5', 'value': '5'},
                        {'label': '10', 'value': '10'},
                    ],
                    placeholder="Select the number of frames..",
                    clearable=False,
                    value='5'
                )
            ]
        ),

        html.Br(),

        html.Div(
            id='datetime_class',
            className='datetime_class',
            children=[
                html.Div(
                    className="four columns",
                    children=[
                        html.P('Pick a Date:'),
                        dcc.DatePickerSingle(
                            # className='date-picker',
                            id='date_picker',
                            date=dt.now(),
                            display_format='Y-M-D',
                            style={'background-color':'white','fontSize': 12}
                        ),
                    ],
                    ),

                html.Div(
                    className= "four columns time_class",
                    children=[
                        html.P('Start-time:'),
                        dcc.Input(
                            className='timeinput',
                            id="starttime",
                            value=dt.strftime(dt.now(), '%H:%M'),

                            ),

                    ]),

                html.Div(
                    className= "four columns time_class",
                    children=[
                        html.P('End-time:'),
                        dcc.Input(
                            className='timeinput',
                            id="endtime",

                            value=dt.strftime(dt.now(), '%H:%M'),

                            ),
                    ]
                )
            ]
        ),

        html.Br(),
        html.Div(
            className="row",
            style={'textAlign':'center'},
            children=[
                html.Button('Show Results', id='show_results', className="button_show"),
                html.Button('Show Locations', id='show_locations', className="button_show")
            ]
        )
    ]

    return children
