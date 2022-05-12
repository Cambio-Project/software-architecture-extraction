from source.input.InteractiveInput import InteractiveInput

user_input = InteractiveInput()
print()
print("Found input:")
print(user_input)
print("---------")
model_input = user_input.model_input
trace_input = user_input.trace_input
settings_input = user_input.settings_input

model = None
arch = None
model_file = ''
model_name = ''
