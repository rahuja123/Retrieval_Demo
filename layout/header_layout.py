import dash
import dash_core_components as dcc
import dash_html_components as html
import base64





def header_layout(port):
    children=[
            html.Div(
                children=[
                    html.A(
                        id='ntu-logo',
                        children=[
                            html.Img(
                                src='data:image/png;base64,{}'.format(
                                    base64.b64encode(
                                        open(
                                            './assets/NTU_logo_white.png', 'rb'
                                        ).read()
                                    ).decode()
                                )
                            )],
                        href="http://127.0.0.1:{}/".format(port)
                    ),


                    html.H2(
                        "NTU ReID Demo"
                    ),

            ]),
        ]


    return children
