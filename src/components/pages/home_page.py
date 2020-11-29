import base64
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import speech_recognition as sr
from app import app
from dash.dependencies import Input, Output
from components.util.call_model import call_model

page = html.Div([html.Div(
    [
        dbc.Row([
            dbc.Card([
                dbc.CardHeader("Upload speech (.wav files only)"),
                dcc.Upload(dbc.Button("Upload your speech",

                                      color='danger',
                                      id='recordButton'),
                           className='recordButton',
                           id='upload-speech',
                           accept='.wav')
            ],

                className='cardSpeech'),
            dbc.Card([
                dbc.CardHeader("Result (English)"),
                html.Div(id='speech', className='speechResult')
            ],
                className='cardSpeech',
                id='result',
                style={'display': 'none'}),

            dbc.Card([
                dbc.CardHeader("Continue ?"),
                dbc.Row([
                    dbc.Button("Translate", id='continue',
                               color='primary',
                               className='button-continue'),
                    dbc.Button("Hide", id='cancel',
                               color='secondary',
                               className='button-continue')
                ])
            ],
                className='cardSpeech',
                id='continue_card',
                style={'display': 'none'})
        ]),
        dbc.Row([
            dbc.Card([
                dbc.CardHeader("Translation (Dutch)"),
                html.Div(id='translation', className='speechResult')
            ],
                id='translation_card',
                className='cardSpeech',
                style={'display': 'none'})
        ])
    ]
)])


# App callbacks are Python functions that are automatically called by Dash whenever an input component's property
# changes : https://dash.plotly.com/basic-callbacks
@app.callback([Output(component_id='speech', component_property='children'),
               Output(component_id='result', component_property='style')],
              [Input(component_id='recordButton', component_property='n_clicks'),
               Input(component_id='upload-speech', component_property='contents')])
def speech_result(value, contents):
    # If we clicked on the button and the chosen file is accepted (.wav) -> continue operations
    if value is not None and contents is not None:
        r = sr.Recognizer()
        content_type, content_string = contents.split(',')

        # Empty/Initialize our translation text file
        translation = open("/var/www/FlaskApp/FlaskApp/data/speech/translation.txt", 'w')
        translation.close()

        # Write the supplied .wav file to a local .wav file to later use as input
        with open('/var/www/FlaskApp/FlaskApp/myfile.wav', mode='wb+') as f:
            f.write(base64.b64decode(content_string))
            f.close()

        with sr.AudioFile('/var/www/FlaskApp/FlaskApp/myfile.wav') as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source, duration=5)

            try:
                text = r.recognize_google(audio)
                return text, {'display': 'inline'}

            except sr.UnknownValueError or sr.WaitTimeoutError or sr.RequestError:
                return "I didn't hear that correctly. Could you try again?", {'display': 'inline'}
    else:
        return None, {'display': 'none'}


# App callbacks are Python functions that are automatically called by Dash whenever an input component's property
# changes : https://dash.plotly.com/basic-callbacks
@app.callback(Output(component_id='continue_card', component_property='style'),
              [Input(component_id='speech', component_property='children')])
def continue_card(value):
    if value:
        if value != "I didn't hear that correctly. Could you try again?":
            return {'display': 'inline'}
    return {'display': 'none'}


# App callbacks are Python functions that are automatically called by Dash whenever an input component's property
# changes : https://dash.plotly.com/basic-callbacks
@app.callback([Output(component_id='translation', component_property='children'),
               Output(component_id='translation_card', component_property='style'), ],
              [Input(component_id='continue', component_property='n_clicks_timestamp'),
               Input(component_id='cancel', component_property='n_clicks_timestamp'),
               Input(component_id='speech', component_property='children')])
def translation_card(continue_ts, cancel_ts, speech):
    # If our continue button is clicked more recently than cancel -> show translation else hide
    if not cancel_ts and continue_ts or continue_ts and continue_ts > cancel_ts:
        file_to_write = open("/var/www/FlaskApp/FlaskApp/data/speech/test.txt", "w")
        file_to_write.write(str(speech))
        file_to_write.close()

        call_model()

        f_to_read = open("/var/www/FlaskApp/FlaskApp/data/speech/translation.txt")
        translation = f_to_read.read()

        f_to_read.close()

        return translation, {'display': 'inline' if translation else "none"}

    return '', {'display': 'none'}
