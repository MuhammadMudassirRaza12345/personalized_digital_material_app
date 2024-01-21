import streamlit as st
from my_streamlit_app import generate_gpt_turbo, format_text, generate_dalle_image, text_edit_img

def main():
    st.header('Personalized Digital Material Making App',divider='green')
    instructions = """
    How to write prompt:

    e.g1: Create a post for company name Markelytics. In this post write about the job opening for data engineers. 
    Fresh graduates can also apply. Location in Karachi. Job Type: Hybrid. Contact: career@marketlytics.com
    
    e.g2: Love is a beautiful thing in life. Create an image of love and write the best quote about love on the image.
    """
    st.markdown(instructions)


    # Initialize session state variables
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
    if 'content_generated' not in st.session_state:
        st.session_state.content_generated = False

    user_input = st.text_area("Enter your creative prompt:", value=st.session_state.user_input, height=150)

    if st.button("Generate"):
        st.session_state.user_input = user_input
        generate_content_and_images(user_input)
        st.session_state.content_generated = True
    elif st.button("Clear"):
        st.session_state.user_input = ""
        st.session_state.content_generated = False
        st.experimental_rerun()
    elif st.button("Regenerate"):
        generate_content_and_images(st.session_state.user_input)
        st.session_state.content_generated = True

    # Display the content and images if they are available in the session state
    if st.session_state.content_generated:
        display_generated_content()

def generate_content_and_images(user_input):
    if user_input:
        raw_content = generate_gpt_turbo(user_input)
        formatted_content = format_text(raw_content)
        image_result = generate_dalle_image(user_input)
        modified_image_path = "./images/new_img.png"

        # Save to session state
        st.session_state['formatted_content'] = formatted_content
        st.session_state['image_result'] = image_result
        st.session_state['modified_image_path'] = modified_image_path

def display_generated_content():
    st.subheader("Content for post")
    st.write(st.session_state['formatted_content'])

    text_edit_img(st.session_state['formatted_content'], st.session_state['image_result'])

    st.subheader("Image for post")
    st.image(st.session_state['image_result'], use_column_width=True)
    download_image(st.session_state['image_result'], "original_image.png", "Download Original Image", "original_image_download")

    st.subheader("Image for post with text modified")
    st.image(st.session_state['modified_image_path'], use_column_width=True)
    download_image(st.session_state['modified_image_path'], "modified_image.png", "Download Modified Image", "modified_image_download")

def download_image(image_path, filename, button_text, key):
    with open(image_path, "rb") as file:
        file_data = file.read()
        st.download_button(label=button_text, data=file_data, file_name=filename, mime="image/png", key=key)

if __name__ == "__main__":
    main()
  