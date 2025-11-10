import streamlit as st
from viz.tabs import reads_statistics_viewer, sncrna_counts_viewer, de_analysis_viewer, reads_coordinates_extraction


def main():

    # Set up layout and menu items
    menu_dict = {
        "Get help": "mailto:karolina.trachtova@ceitec.muni.cz",
        "Report a bug": "https://github.com/ktrachtova/perseqpipe_viz/issues",
        "About": "https://github.com/ktrachtova/perseqpipe_viz"
    }
    st.set_page_config("PerSeqPIPE VIZ", menu_items=menu_dict)

    # Switch top logo based on theme (dark VS light) https://github.com/streamlit/streamlit/issues/11920 -> DOES NOT WORK!
    # Keeping the note here for future when streamlit developers will fix it
    st.markdown(
    "<style>.stApp { background-color: white; }</style>",
    unsafe_allow_html=True
    )
    st.image("docs/images/perseqpipe_viz_logo_dark.png")

    tab1, tab2, tab3, tab4 = st.tabs(["Reads Statistics Viewer", "sncRNA Counts Viewer", "DE Analysis Viewer", "Reads Coordinates Extraction"])

    with tab1:
        reads_statistics_viewer.render_tab()
    
    with tab2:
        sncrna_counts_viewer.render_tab()

    with tab3:
        de_analysis_viewer.render_tab()
    
    with tab4:
        reads_coordinates_extraction.render_tab()


if __name__ == "__main__":
    main()