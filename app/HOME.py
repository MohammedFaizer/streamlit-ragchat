# import streamlit as st
# import streamlit.components.v1 as components

# components.html(
#     """
#     <elevenlabs-convai agent-id="agent_01jy109e1cezfbqwyhdfzwect1"></elevenlabs-convai>
#     <script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
#     """,
#     height=600,  # adjust as needed
# )

# st.markdown(
#     """
#     <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
#         <img src="https://roa-admin-staging.vercel.app/assets/logo.svg" width="200">
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

import streamlit as st
import streamlit.components.v1 as components


st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
        <img src="https://roa-admin-staging.vercel.app/assets/logo.svg" width="200">
    </div>
    """,
    unsafe_allow_html=True,
)

# Embed ElevenLabs widget
components.html(
    """
    <!DOCTYPE html>
    <html>
      <head>
        <script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
      </head>
      <body>
        <elevenlabs-convai agent-id="agent_01jy109e1cezfbqwyhdfzwect1"></elevenlabs-convai>
      </body>
    </html>
    """,
    height=550,
    scrolling=True,
    
)
