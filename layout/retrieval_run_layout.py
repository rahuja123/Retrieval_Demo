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


def retrieval_run_layout(global_camera_names,models_dict):
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
                html.P("Network Model", className='p-dropdown'),
                dcc.Dropdown(
                    id='network_dropdown_reid',
                    className="div-for-dropdown",
                    options=[{'label': model, 'value': model} for model in list(models_dict.keys())],
                    value= list(models_dict.keys())[1],
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
                    options=populate_camera_dropdown_menu(global_camera_names),
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
                        {'label': '5', 'value': '5'},
                        {'label': '10', 'value': '10'},
                    ],
                    placeholder="Select the number of frames..",
                    clearable=False,
                    value='5'
                )
            ]
        ),

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