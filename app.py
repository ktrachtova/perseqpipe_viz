import streamlit as st
from viz.tabs import read_statistics_viewer, sncrna_counts_viewer, de_analysis_viewer

def main():

    # Set up layout and menu items
    menu_dict = {
        "Get help": "mailto:karolina.trachtova@ceitec.muni.cz",
        "Report a bug": "https://github.com/ktrachtova/perseqpipe_viz/issues",
        "About": "https://github.com/ktrachtova/perseqpipe_viz"
    }
    st.set_page_config("PerSeqPIPE VIZ", menu_items=menu_dict)

    # Switch top logo based on theme - dark VS light
    # When theme switched in Settings menu this does not work -> https://github.com/streamlit/streamlit/issues/11920
    # Keeping for future when it hopefully will work
    if st.context.theme.type == "light":
        st.image("docs/images/perseqpipe_viz_logo_light.png")
    else:
        st.image("docs/images/perseqpipe_viz_logo_dark.png")

    tab1, tab2, tab3 = st.tabs(["Read Statistics Viewer", "sncRNA Counts Viewer", "DE Analysis Viewer"])

    with tab1:
        read_statistics_viewer.render_tab()
    
    with tab2:
        sncrna_counts_viewer.render_tab()

    with tab3:
        de_analysis_viewer.render_tab()


if __name__ == "__main__":
    main()