import google.generativeai as genai


genai.configure(api_key='AIzaSyCiNIAggCChDvV8W8bXR_kgaEl0Hb7SH2k')
global text_response
# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
  ]
)

# The Gemini 1.5 models are versatile and work with multimodal prompts
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

def file_upload(file_path):
    sample_file = genai.upload_file(path=file_path,
                                    display_name="Sample drawing")
    
    print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

    file = genai.get_file(name=sample_file.name)
    print(f"Retrieved file '{file.display_name}' as: {file.uri}")

    response = model.generate_content([sample_file, '''You have to plan the role of Math lecture, You have to analyze the image and find the solution, You should return only the varibale and the ans'''])

    genai.delete_file(sample_file.name)
    print(f'Deleted {sample_file.display_name}.')

    return response.text


