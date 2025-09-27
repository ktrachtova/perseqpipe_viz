# Read Statistics Viewer ########

import streamlit as st
import io
import plotly.express as px
from viz.tabs import *
from viz import utils
from viz import settings


def render_tab():

    st.title("Reads Statistics Viewer")

    # Upload a file
    uploaded_stats = st.file_uploader("Upload a CSV/TSV file", type=["csv","tsv"], key='stats', help="CSV/TSV file with comma or tab separator. If visualizing PerSeqPIPE results, import file **read_counts_summary.csv** from `all_stats/` folder.")

    # Try to render content only if file is uploaded
    if uploaded_stats is not None:

        st.header("Reads Table", divider = "grey")

        # Reads a CSV/TSV file -> function from utils.py
        df_stats = utils.safe_read_table(uploaded_stats)

        # Render the table
        st.dataframe(df_stats)

        st.header("Reads Statistics Visualization", divider = "grey")

        # Logic for options of which columns - counts or percentages - to show ----------
    
        # Dault always 'counts'
        columns_to_render_options = ["counts"]

        # Identify count columns (excluding percentage columns)
        count_columns = [col for col in df_stats.columns if col != "sample" and not col.endswith("%")]

        # Try to look for percentage column too
        try:
            percent_columns = [col for col in df_stats.columns if col != "sample" and col.endswith("%")]
            if not percent_columns:
                st.info("ℹ️ Only count columns were found — no percentage columns ending with '%' were detected.")
            else:
                columns_to_render_options.append('percentages')
        except Exception as e:
            st.error(f"❌ An error occurred while identifying percentage columns: {e}, continuing only with counts columns...")
        
        col1, col2 = st.columns(2)

        with col1:
            columns_to_render = st.pills("Columns to visualize:", options = columns_to_render_options, default = "counts")
            if columns_to_render == "counts":
                columns_to_use = count_columns
            else:
                columns_to_use = percent_columns

        col1, col2 = st.columns(2)
        with col1:
            plot_options = st.multiselect(
                "Select plot types to display:",
                options=["Bar Plots", "Pie Charts"],
                default=["Bar Plots"]  # Or empty by default
            )

        barplots_html = {}
        barplots_pdf = {}
        pieplots_html = {}
        pieplots_pdf = {}

        if "Bar Plots" in plot_options:

            st.subheader("Bar Plots", divider="gray")

            # Plots adjustments options
            col1, col2 = st.columns(2)
            with col1:
                text_bars = st.toggle("Show bar text")

                # Colors options
                colors = {}
                with st.expander("Color options:", expanded=False):
                    for category in columns_to_use:
                        colors[category] = st.text_input(category, value="DarkTurquoise", key=category+"_color")

            with col2:
                sync_y_axis = st.checkbox("Use same y-axis range for all plots", value=False)

            # Create range if user wants to sync all the plots
            y_axis_range = None
            if sync_y_axis:
                # Take the first column in the table (which is not 'sample') and use that for creating range
                max_y = df_stats[columns_to_use[0]].max()
                y_axis_range = [0, max_y]
        
            for category in columns_to_use:
                fig = utils.plot_bar_chart(df_stats, category, colors[category], y_axis_range, columns_to_render, text_bars)
                st.plotly_chart(fig)

                buffer = io.StringIO()
                fig.write_html(buffer, include_plotlyjs='cdn')
                html_bytes = buffer.getvalue().encode()
                barplots_html[category] = html_bytes
                barplots_pdf[category] = fig
            
            utils.download_barplots(barplots_html, barplots_pdf, "barplots")

        if "Pie Charts" in plot_options:

            st.subheader("Pie Charts", divider="gray")

            count_columns2 = [col for col in count_columns if col != "sample" and col != "raw_reads"]
        
            selected_palette = st.selectbox(
                "Select color palette for pie charts:",
                options=list(settings.PALLETE_OPTIONS.keys()),
                index=0  # default = Set3
            )

            # Generate pie charts for each sample
            for _, row in df_stats.iterrows():
                sample_name = row["sample"]
                raw_reads = row["raw_reads"]
                    
                values = [(row[col] / raw_reads) * 100 for col in count_columns2]  # Calculate percentage
                labels = count_columns2
                    
                # Create a Pie chart
                fig = px.pie(
                    names=labels,
                    values=values,
                    title=f"{sample_name}",
                    labels={name: f"{name} ({value:.2f}%)" for name, value in zip(labels, values)},
                    color_discrete_sequence=settings.PALLETE_OPTIONS[selected_palette]
                )
                    
                # Display the pie chart in Streamlit
                st.plotly_chart(fig)

                buffer = io.StringIO()
                fig.write_html(buffer, include_plotlyjs='cdn')
                html_bytes = buffer.getvalue().encode()
                pieplots_html[sample_name] = html_bytes
                pieplots_pdf[sample_name] = fig

            utils.download_barplots(pieplots_html, pieplots_pdf, "pieplots")
