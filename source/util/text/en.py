from util.text.ids import *

TEXT = {
    DEFAULT:                                               '...',

    # Knowledge base
    INTENT_KB_NAME:                                        'KB',

    # Stimulus Responses & Response Measures
    STIMULUS_RESPONSE_TEXTS:                               {
        'Service':   {
            'stimuli':           [
                'Decreased service performance',
                'Service failure'
            ],
            'sources':           [
                'a technical issue',
                'deployment error',
                'a software bug'
            ],
            'environments':      [
                'during deployment',
                'at normal operation'
            ],
            'responses':         [
                'Service should return to normal performance',
                'Service should restart'
            ],
            'response-measures': {
                'normal-time':   ['>10s', '10s', '5s', '3s', '1s', '500ms', '300ms', '100ms', '50ms', '30ms', '10ms',
                                  '<10ms'],
                'normal-cases':  ['100%', '99.99%', '99.9%', '99%', '98%', '97%', '96%', '95%', '<95%'],
                'recovery-time': ['>1h', '1h', '45min', '30min', '15min', '5min', '3min', '1min', '30s', '15s', '10s',
                                  '1s', '<1s']
            }},
        'Operation': {
            'stimuli':           [
                'Spike response times',
                'Response time deviations'
            ],
            'sources':           [
                'a technical issue',
                'deployment error',
                'a software bug'
            ],
            'environments':      [
                'during deployment',
                'at normal operation'
            ],
            'responses':         [
                'Response times should return to normal values.'
            ],
            'response-measures': {
                'normal-time':   ['>10s', '10s', '5s', '3s', '1s', '500ms', '300ms', '100ms', '50ms', '30ms', '10ms',
                                  '<10ms'],
                'normal-cases':  ['100%', '99.99%', '99.9%', '99%', '98%', '97%', '96%', '95%', '<95%'],
                'recovery-time': ['5min', '3min', '1min', '30s', '15s', '10s', '1s']
            }},
    },

    # Fallback
    INTENT_PROCESSING_ERROR:                               'Ops something went wrong.',

    # Default
    INTENT_EMPTY_NAME:                                     'Default-Empty',
    INTENT_CLEAR_NAME:                                     'Default-Clear',
    INTENT_FALLBACK_NAME:                                  'Default-Fallback',
    INTENT_FALLBACK_TEXT:                                  [
        'That doesn\'t compute. Maybe you can rephrase your sentence?',
        'I don\'t know what you mean. Can you elaborate?',
        'I missed what you said. What was that?',
        'Sorry, could you say that in a different way?',
        'Sorry, I didn\'t get that. Can you rephrase?',
        'Sorry, what was that?',
        'I didn\'t get that. Can you try something different?',
        'That doesn\'t really make sense to me.',
        'Maybe try something different?.'
    ],
    INTENT_BYE_NAME:                                       'Default-Bye',
    INTENT_BYE_TEXT:                                       [
        'Nice to work with you! See you around. &#x1F44B;',
        'Okay then! Have a nice day.',
        'Thanks for participating! See you &#x1F44B;'
    ],
    INTENT_BYE_QUESTIONNAIRE:                              str(
        'If you are participating in the study and have finished the study tasks please follow this link '
        'to the Google Forms questionnaire:<br>'
        '<a href="https://docs.google.com/forms/d/e/1FAIpQLSdjMUaYhlVL9ryzBOmulNk1zti2-8-6fjYtUZ-lGOOghY2B2g/'
        'viewform?entry.1314988225={}" target="_blank">'
        '<button type="button" class="btn m-md-1">To the survey</button></a>'),
    INTENT_HELP_NAME:                                      'Default-Help',
    INTENT_HELP_TEXT:                                      [
        str('Hang on, help is on it\'s way!<br><br>'
            'I am a chatbot that helps you to elicit resilience scenarios. '
            'A resilience scenario consists of <b>7</b> parameters '
            '(artifact, stimulus, source, environment, response, response measure, and a description).<br>'
            'A resilience scenario should help resilience engineers or software architects to '
            'test their software systems.')
    ],

    # Guide
    INTENT_GUIDE_NAME:                                     'Default-Guide',
    INTENT_GUIDE_TEXT:                                     str(
        'Select a topic that you want to know more about or ask me about something.<br>'
        'If you are satisfied with the explanations, please tell me to <b>continue</b>.'),
    INTENT_GUIDE_OPTIONS:                                  [
        'Architecture', 'Analysis', 'Artifact', 'Description', 'Stimulus', 'Tracing'
    ],
    INTENT_GUIDE_EXPLANATIONS:                             {
        'Architecture':     {
            'title': 'Architecture',
            'text':  str(
                'An architecture is constructed from the result of a '
                '<a class="link" href="https://en.wikipedia.org/wiki/Tracing_(software)" target="_blank">'
                'tracing tool</a> analysis. This tool can understand and analyze traces from either '
                '<a class="link" href="https://www.jaegertracing.io/" target="_blank">Jaeger</a> or '
                '<a class="link" href="https://zipkin.io/" target="_blank">Zipkin</a>.'),
            'link':  {
                'text': 'Read more here',
                'url':  'https://en.wikipedia.org/wiki/Tracing_(software)'
            },
            'image': 'static/img/guide/arch.png'
        },
        'Analysis':         {
            'title': 'Analysis',
            'text':  str(
                'In the analysis of a trace services and operations are identified. '
                'The relationships between these services and operations is visualized as graph. '
                'You can see the constructed graph on the left.'
            )},
        'Artifact':         {
            'title': 'Artifact',
            'text':  str(
                'In this context an artifact is part of the graph that is constructed during the analysis. '
                'One type of artifact is a node which represents a service of the systems architecture. '
                'Another type of artifact is an edge which represents an operation of the system.'
            )},
        'Description':      {
            'title': 'Description',
            'text':  str(
                'A description in the context of resilience scenarios summarizes the content of the whole '
                'scenario in one short sentence.'
            )},
        'Stimulus':         {
            'title': 'Stimulus',
            'text':  str(
                'A stimulus is responsible for the deviation from the normal behaviour of a software system.'
            )},
        'Source':           {
            'title': 'Source',
            'text':  str(
                'The source describes the occurrence of the stimulus.'
            )},
        'Environment':      {
            'title': 'Environment',
            'text':  str(
                'The environment represents the state that the system is when the stimulus arises.'
            )},
        'Response':         {
            'title': 'Response',
            'text':  str(
                'A response specifies the behaviour the system when the stimulus arises.'
            )},
        'Response Measure': {
            'title': 'Response Measure',
            'text':  str(
                'The response measure quantifies the response. '
                'There are two measures that are used in the response measure. '
                'One describes the normal operating window of a service/operation. '
                'The other describes the recovery time until the service/operation returns to the normal '
                'operation window.'
            )},
        'Tracing':          {
            'title': 'Tracing',
            'link':  {
                'text': 'Learn more about tracing',
                'url':  'https://en.wikipedia.org/wiki/Tracing_(software)'
            },
            'text':  str(
                'In software engineering, tracing involves a specialized use of logging to record information about a '
                'programs execution. This information is typically used by programmers for debugging purposes; and '
                'additionally, depending on the type and detail of information contained in a trace log, by '
                'experienced system administrators or technical-support personnel and by software monitoring tools to '
                'diagnose common problems with software. Tracing is a cross-cutting concern.'
            )},
        'Zipkin':           {
            'title': 'Zipkin',
            'link':  {
                'text': 'Learn more about zipkin',
                'url':  'https://zipkin.io/'},
            'text':  str(
                'Zipkin is a distributed tracing system. It helps gather timing data needed to troubleshoot latency '
                'problems in service architectures. Features include both the collection and lookup of this data.'
            )},
        'Jaeger':           {
            'title': 'Jaeger',
            'link':  {
                'text': 'Learn more about jaeger',
                'url':  'https://www.jaegertracing.io/'
            },
            'text':  str(
                'As on-the-ground microservice practitioners are quickly realizing, the majority of operational '
                'problems that arise when moving to a distributed architecture are ultimately grounded in two areas: '
                'networking and observability. It is simply an orders of magnitude larger problem to network and debug '
                'a set of intertwined distributed services versus a single monolithic application.'
            )},
    },
    INTENT_GUIDE_CONTINUE_TEXT:                            [
        'Do you want to know more?',
        'Do you need more infos?',
        'Anything else you want to know?'
    ],
    INTENT_GUIDE_CONTINUE_CONFIRM_TEXT:                    'I am good, let\'s continue! &#x2714;',
    INTENT_GUIDE_OPTION_NAME:                              'Default-Guide-Option',
    INTENT_GUIDE_CONFIRM_NAME:                             'Default-Guide-Confirm',

    # Welcome
    INTENT_WELCOME_NAME:                                   'Default-Welcome',
    INTENT_WELCOME_TEXT:                                   str(
        'Hey there! &#x1F44B;<br><br>'
        'I am a chatbot and I will help you to elicit <b>resilience scenarios</b>. '
        'For each scenario we will go through the following steps:<br>'
        '<ol>'
        '<li>Select an <b>architecture</b> to analyze</li>'
        '<li>Select an <b>artifact</b> of the architecture</li>'
        '<li>Specify a <b>stimulus</b></li>'
        '<li>Specify a <b>response</b></li>'
        '<li>Specify a <b>response measure</b></li>'
        '<li>Specify a <b>description</b></li>'
        '<li>Save the <b>resilience scenario</b></li>'
        '</ol>'
        'For every step you can choose from options I propose, or you can write to me.<br><br>'
        'In case you get stuck you can tell me at which step you want to continue or ask for help.<br><br>'
        'Everything clear? Are you ready?'
    ),
    INTENT_WELCOME_RESUME_TEXT:                            'Continue where you left. &#x21bb;',
    INTENT_WELCOME_YES_TEXT:                               'Yes, let\'s go! &#x1F44D;',
    INTENT_WELCOME_NO_TEXT:                                'No, I need more information. &#x2753;',
    INTENT_WELCOME_CONFIRM_NAME:                           'Default-Welcome-Confirm',
    INTENT_WELCOME_DECLINE_NAME:                           'Default-Welcome-Decline',
    INTENT_WELCOME_CONTINUE_NAME:                          'Default-Welcome-Continue',

    # Elicitation
    INTENT_ELICITATION_ARCHITECTURE_NAME:                  'Elicitation-Select-Architecture',
    INTENT_ELICITATION_ARCHITECTURE_TEXT:                  {
        'title': '<b>Step 1</b> - Select the <b>architecture</b>',
        'text':  str(
            'Below you are given a list of architectures. '
            'Please select one architecture are tell me which you would like to choose.<br>'
        )
    },
    INTENT_ELICITATION_ARCHITECTURE_FOLLOWUP_NAME:         'Elicitation-Select-Architecture-Followup',
    INTENT_ELICITATION_ARCHITECTURE_DEFAULT_NAME:          'Elicitation-Select-Architecture-Default',
    INTENT_ELICITATION_COMPONENT_NAME:                     'Elicitation-Select-Component',
    INTENT_ELICITATION_COMPONENT_TEXT:                     {
        'title':   '<b>Step 2</b> - Select the <b>artifact</b> from <i>{}</i>',
        'text':    'Please select one artifact from the following options.<br>',
        'spoiler': {
            'title': 'Hints',
            'text':  str(
                '<ul>'
                '<li>You can use the graph on the left to select an artifact if you don\'t find it in the options.</li>'
                '<li>Please make sure to match the name of the artifact to a certain extend in case you write to the '
                'bot. Also, telling the bot if the artifact is a service or an operation usually helps.</li>'
                '</ul>')
        }
    },
    INTENT_ELICITATION_COMPONENT_MISSING_TEXT:             'Try again {} {} is not in the architecture.',
    INTENT_ELICITATION_COMPONENT_SERVICE_TEXT:             'Here are the <b>services</b> to choose from ...',
    INTENT_ELICITATION_COMPONENT_OPERATION_TEXT:           'Here are the <b>operations</b> to choose from ...',
    INTENT_ELICITATION_COMPONENT_FOLLOWUP_NAME:            'Elicitation-Select-Component-Followup',
    INTENT_ELICITATION_COMPONENT_DEFAULT_NAME:             'Elicitation-Select-Component-Default',
    INTENT_ELICITATION_STIMULUS_NAME:                      'Elicitation-Specify-Stimulus',
    INTENT_ELICITATION_STIMULUS_TEXT:                      {
        'title':   '<b>Step 3</b> - Specify the <b>stimulus</b> for {} <i>{}</i>',
        'text':    'What is a potential stimulus for this {}?<br>',
        'spoiler': {
            'title': 'Hint',
            'text':  'A typical stimulus would be "crashed service", "slow responding operation", or "external event".'
        }
    },
    INTENT_ELICITATION_STIMULUS_FOLLOWUP_NAME:             'Elicitation-Specify-Stimulus-Followup',
    INTENT_ELICITATION_STIMULUS_DEFAULT_NAME:              'Elicitation-Specify-Stimulus-Default',
    INTENT_ELICITATION_STIMULUS_SOURCE_NAME:               'Elicitation-Specify-Stimulus-Source',
    INTENT_ELICITATION_STIMULUS_SOURCE_TEXT:               {
        'title':   '<b>Step 3.1</b> - Specify the <b>source</b> of the stimulus <i>{}</i>',
        'text':    'What could be the <b>source</b> of this stimulus?<br>',
        'spoiler': {
            'title': 'Hint',
            'text':  'Typical examples for the source would be "a technical issue", "a bug", or another artifact.'
        }
    },
    INTENT_ELICITATION_STIMULUS_SOURCE_FOLLOWUP_NAME:      'Elicitation-Specify-Stimulus-Source-Followup',
    INTENT_ELICITATION_STIMULUS_SOURCE_DEFAULT_NAME:       'Elicitation-Specify-Stimulus-Source-Default',
    INTENT_ELICITATION_STIMULUS_ENVIRONMENT_NAME:          'Elicitation-Specify-Stimulus-Environment',
    INTENT_ELICITATION_STIMULUS_ENVIRONMENT_TEXT:          {
        'title':   '<b>Step 3.2</b> - Specify the <b>environment</b> of the stimulus <i>{}</i>',
        'text':    'What would be the <b>environment</b> of the system at the time the stimulus occurs?<br>',
        'spoiler': {
            'title': 'Hint',
            'text':  str(
                'The situation in which the system is in can be used as a synonym for the environment. Typical examples'
                ' for the environment would be "during startup", "during normal operation", or "at high workload".')
        }
    },
    INTENT_ELICITATION_STIMULUS_ENVIRONMENT_FOLLOWUP_NAME: 'Elicitation-Specify-Stimulus-Environment-Followup',
    INTENT_ELICITATION_STIMULUS_ENVIRONMENT_DEFAULT_NAME:  'Elicitation-Specify-Stimulus-Environment-Default',
    INTENT_ELICITATION_RESPONSE_NAME:                      'Elicitation-Specify-Response',
    INTENT_ELICITATION_RESPONSE_TEXT:                      {
        'title':   '<b>Step 4</b> - Specify the <b>response</b> for <i>{}</i>',
        'text':    'A response defines what action should be performed against the stimuli.',
        'spoiler': {
            'title': 'Hint',
            'text':  ''
        }
    },
    INTENT_ELICITATION_RESPONSE_FOLLOWUP_NAME:             'Elicitation-Specify-Response-Followup',
    INTENT_ELICITATION_RESPONSE_DEFAULT_NAME:              'Elicitation-Specify-Response-Default',
    INTENT_ELICITATION_MEASURE_NAME:                       'Elicitation-Specify-Response-Measure',
    INTENT_ELICITATION_MEASURE_TEXT:                       {
        'title':   '<b>Step 5</b> - Specify the <b>response measure</b> for <i>{}</i>',
        'text':    'A response measure quantifies the response.',
        'spoiler': {
            'title': '',
            'text':  ''
        }
    },
    INTENT_ELICITATION_MEASURE_NORMAL_NAME:                'Elicitation-Specify-Response-Measure-Normal',
    INTENT_ELICITATION_MEASURE_NORMAL_TEXT:                str(
        'What would be an <b>optimal response time</b>?'
    ),
    INTENT_ELICITATION_MEASURE_NORMAL_FOLLOWUP_NAME:       'Elicitation-Specify-Response-Measure-Normal-Followup',
    INTENT_ELICITATION_MEASURE_NORMAL_DEFAULT_NAME:        'Elicitation-Specify-Response-Measure-Normal-Default',
    INTENT_ELICITATION_MEASURE_CASES_NAME:                 'Elicitation-Specify-Response-Measure-Cases',
    INTENT_ELICITATION_MEASURE_CASES_SERVICE_TEXT:         str(
        'What is the <b>optimal</b> availability of the service?'
    ),
    INTENT_ELICITATION_MEASURE_CASES_OPERATION_TEXT:       str(
        'In <b>how many cases</b> should this hold?'
    ),
    INTENT_ELICITATION_MEASURE_CASES_FOLLOWUP_NAME:        'Elicitation-Specify-Response-Measure-Cases-Followup',
    INTENT_ELICITATION_MEASURE_CASES_DEFAULT_NAME:         'Elicitation-Specify-Response-Measure-Cases-Default',
    INTENT_ELICITATION_MEASURE_RECOVERY_NAME:              'Elicitation-Specify-Response-Measure-Recovery',
    INTENT_ELICITATION_MEASURE_RECOVERY_TEXT:              str(
        'How long is the <b>non-optimal</b> behavior tolerable?'
    ),
    INTENT_ELICITATION_MEASURE_RECOVERY_FOLLOWUP_NAME:     'Elicitation-Specify-Response-Measure-Recovery-Followup',
    INTENT_ELICITATION_MEASURE_RECOVERY_DEFAULT_NAME:      'Elicitation-Specify-Response-Measure-Recovery-Default',
    INTENT_ELICITATION_DESCRIPTION_NAME:                   'Elicitation-Specify-Description',
    INTENT_ELICITATION_DESCRIPTION_TEXT:                   {
        'title':   '<b>Step 6</b> - Add the description',
        'text':    'A description summarizes the scenario.',
        'spoiler': {
            'title': 'Hint',
            'text':  str(
                'The description gives an overview about the scenario. '
                'This has no influence on ... but it might give other engineers a better understanding of the scenario.'
            )
        }
    },
    INTENT_ELICITATION_DESCRIPTION_QUICK_RESPONSE:         '{} of {} {}',
    INTENT_ELICITATION_DESCRIPTION_FOLLOWUP_NAME:          'Elicitation-Specify-Description-Followup',
    INTENT_ELICITATION_DESCRIPTION_DEFAULT_NAME:           'Elicitation-Specify-Description-Default',
    INTENT_ELICITATION_SAVE_SCENARIO_NAME:                 'Elicitation-Save-Scenario',
    INTENT_ELICITATION_SAVE_SCENARIO_TEXT:                 {
        'title': '<b>Step 7</b> - Save the resilience scenario',
        'text':  'The resilience scenario has now all necessary parameters configured.'
    },
    INTENT_ELICITATION_SUMMARY_SERVICE_MEASURE_TEXT:       str(
        'Normal availability is <b>{}</b>.<br>'
        'Within <b>{}</b> after occurrence of the stimuli the service should return to optimal behaviour.'
    ),
    INTENT_ELICITATION_SUMMARY_OPERATION_MEASURE_TEXT:     str(
        'Normal response time is <b>{}</b> (holds in <b>{}</b> of cases).<br>'
        'Within <b>{}</b> after occurrence of the stimuli the response times return to normal values.'
    ),
    INTENT_ELICITATION_SAVE_SCENARIO_CONTINUE_TEXT:        'Here is the summary of your current scenario.',
    INTENT_ELICITATION_SAVE_SCENARIO_SAVE_TEXT:            str(
        'Is the scenario finished, or do you want to modify anything?'
    ),
    INTENT_ELICITATION_SAVE_SCENARIO_SAVE_CONFIRM_TEXT:    'Yes, save the scenario. &#x2714;',
    INTENT_ELICITATION_SAVE_SCENARIO_MODIFY_OPTIONS:       {
        'e-select-component':         'Modify the artifact&#x1F9F1;',
        'e-specify-stimulus':         'Modify the stimulus &#x26A0;',
        'e-specify-response':         'Modify the response &#x27A1;',
        'e-specify-response-measure': 'Modify the response measure &#x1F4C8;',
        'e-specify-description':      'Modify the description &#x1F4DD;'
    },
    INTENT_ELICITATION_SAVE_SCENARIO_CONFIRM_NAME:         'Elicitation-Save-Scenario-Confirm',
    INTENT_ELICITATION_NEXT_STEP_NAME:                     'Elicitation-Next-Step',
    INTENT_ELICITATION_NEXT_STEP_TEXT:                     'Do you want to create another scenario?',
    INTENT_ELICITATION_NEXT_STEP_EXIT_TEXT:                'No &#x274C;',
    INTENT_ELICITATION_NEXT_STEP_CONTINUE_TEXT:            'Yes &#x2714;',
    INTENT_ELICITATION_NEXT_STEP_CONFIRM_NAME:             'Elicitation-Next-Step-Confirm',
    INTENT_ELICITATION_NEXT_STEP_DECLINE_NAME:             'Elicitation-Next-Step-Decline',

    # Extra
    INTENT_FACT_NAME:                                      'Extra-Fact',
    INTENT_FACT_TEXT:                                      [
        'I didn\'t know that one &#x1F446;.',
        'Hm, very interesting.',
        'Who would have thought...'
    ],
    INTENT_JOKE_NAME:                                      'Extra-Joke',
    INTENT_JOKE_TEXT:                                      [
        'Yeah, that\'s a good one &#x1F604;.',
        'Yikes &#x1F923;.',
        'Not so sure about that one &#x1F928;.'
    ]
}
